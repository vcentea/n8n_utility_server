"""
YouTube transcript extraction using yt-dlp.
"""
import logging
import re
import json
import tempfile
import os
from typing import Dict, Any, Optional, List

import yt_dlp

logger = logging.getLogger(__name__)

VIDEO_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{11}$")
VIDEO_URL_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"),
    re.compile(r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"),
    re.compile(r"youtube\.com/v/([a-zA-Z0-9_-]{11})"),
]


def extract_video_id(url_or_id: str) -> str:
    """
    Extract video ID from a YouTube URL or validate a video ID.
    
    Args:
        url_or_id: YouTube video URL or 11-character video ID
    
    Returns:
        The 11-character video ID
    
    Raises:
        ValueError: If video ID cannot be extracted
    """
    url_or_id = url_or_id.strip()
    
    # Check if it's already a valid video ID
    if VIDEO_ID_PATTERN.match(url_or_id):
        return url_or_id
    
    # Try to extract from URL patterns
    for pattern in VIDEO_URL_PATTERNS:
        match = pattern.search(url_or_id)
        if match:
            return match.group(1)
    
    raise ValueError(
        "Invalid video URL or ID. Provide a valid YouTube URL or 11-character video ID."
    )


def get_video_transcript(
    url_or_id: str,
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the transcript/captions for a YouTube video.
    
    Args:
        url_or_id: YouTube video URL or video ID
        language: Preferred language code (e.g., 'en', 'es'). 
                  If not specified, tries to get English or auto-generated.
    
    Returns:
        Dictionary containing video info and transcript.
    
    Raises:
        ValueError: If transcript cannot be extracted
    """
    video_id = extract_video_id(url_or_id)
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    logger.info(f"Extracting transcript for video: {video_id}")
    
    # Create temp directory for subtitle files
    with tempfile.TemporaryDirectory() as temp_dir:
        subtitle_file = os.path.join(temp_dir, "subtitle")
        
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitlesformat": "json3",
            "outtmpl": subtitle_file,
            "quiet": True,
            "no_warnings": True,
        }
        
        # Set language preferences
        if language:
            ydl_opts["subtitleslangs"] = [language, f"{language}-orig", "en", "en-orig"]
        else:
            ydl_opts["subtitleslangs"] = ["en", "en-orig", "en-US", "a].*"]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                
                video_title = info.get("title", "")
                video_duration = info.get("duration", 0)
                channel_name = info.get("uploader", "")
                channel_id = info.get("channel_id", "")
                
                # Find the downloaded subtitle file
                transcript_text = None
                transcript_segments = []
                subtitle_language = None
                
                # Check for subtitle files
                for ext in ["json3", "vtt", "srt"]:
                    for lang_suffix in ["", ".en", ".en-orig", f".{language}" if language else ""]:
                        possible_file = f"{subtitle_file}{lang_suffix}.{ext}"
                        if os.path.exists(possible_file):
                            subtitle_language = lang_suffix.replace(".", "") or "en"
                            transcript_segments, transcript_text = _parse_subtitle_file(
                                possible_file, ext
                            )
                            break
                    if transcript_text:
                        break
                
                # Also check requested_subtitles from info
                if not transcript_text and info.get("requested_subtitles"):
                    for lang, sub_info in info["requested_subtitles"].items():
                        sub_file = sub_info.get("filepath")
                        if sub_file and os.path.exists(sub_file):
                            subtitle_language = lang
                            ext = sub_file.split(".")[-1]
                            transcript_segments, transcript_text = _parse_subtitle_file(
                                sub_file, ext
                            )
                            break
                
                if not transcript_text:
                    raise ValueError(
                        "No transcript available for this video. "
                        "The video may not have captions enabled."
                    )
                
                return {
                    "video_id": video_id,
                    "video_url": video_url,
                    "title": video_title,
                    "duration": video_duration,
                    "channel": channel_name,
                    "channel_id": channel_id,
                    "language": subtitle_language,
                    "transcript": transcript_text,
                    "segments": transcript_segments
                }
                
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if "Private video" in error_msg:
                raise ValueError("This video is private and cannot be accessed.")
            elif "Video unavailable" in error_msg:
                raise ValueError("This video is unavailable.")
            elif "Sign in" in error_msg:
                raise ValueError("This video requires authentication to access.")
            else:
                logger.error(f"yt-dlp error: {e}")
                raise ValueError(f"Failed to extract video info: {error_msg}")
        except Exception as e:
            logger.error(f"Error extracting transcript: {e}")
            raise ValueError(f"Failed to extract transcript: {str(e)}")


def _parse_subtitle_file(filepath: str, ext: str) -> tuple[List[Dict], str]:
    """
    Parse a subtitle file and return segments and full text.
    
    Args:
        filepath: Path to the subtitle file
        ext: File extension (json3, vtt, srt)
    
    Returns:
        Tuple of (segments list, full transcript text)
    """
    segments = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if ext == "json3":
            segments = _parse_json3(content)
        elif ext == "vtt":
            segments = _parse_vtt(content)
        elif ext == "srt":
            segments = _parse_srt(content)
        
        # Build full text from segments
        full_text = " ".join(seg["text"] for seg in segments if seg.get("text"))
        # Clean up multiple spaces
        full_text = re.sub(r"\s+", " ", full_text).strip()
        
        return segments, full_text
        
    except Exception as e:
        logger.error(f"Error parsing subtitle file: {e}")
        return [], ""


def _parse_json3(content: str) -> List[Dict]:
    """Parse JSON3 subtitle format."""
    segments = []
    try:
        data = json.loads(content)
        events = data.get("events", [])
        
        for event in events:
            if "segs" not in event:
                continue
            
            start_ms = event.get("tStartMs", 0)
            duration_ms = event.get("dDurationMs", 0)
            
            text_parts = []
            for seg in event.get("segs", []):
                text = seg.get("utf8", "")
                if text and text.strip():
                    text_parts.append(text)
            
            if text_parts:
                segments.append({
                    "start": start_ms / 1000.0,
                    "duration": duration_ms / 1000.0,
                    "text": "".join(text_parts).strip()
                })
        
    except json.JSONDecodeError:
        pass
    
    return segments


def _parse_vtt(content: str) -> List[Dict]:
    """Parse WebVTT subtitle format."""
    segments = []
    lines = content.split("\n")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for timestamp line (00:00:00.000 --> 00:00:00.000)
        if "-->" in line:
            times = line.split("-->")
            if len(times) == 2:
                start = _parse_timestamp(times[0].strip())
                end = _parse_timestamp(times[1].strip().split()[0])
                
                # Collect text lines until empty line
                text_lines = []
                i += 1
                while i < len(lines) and lines[i].strip():
                    text_lines.append(lines[i].strip())
                    i += 1
                
                text = " ".join(text_lines)
                # Remove VTT tags
                text = re.sub(r"<[^>]+>", "", text)
                
                if text:
                    segments.append({
                        "start": start,
                        "duration": end - start,
                        "text": text
                    })
        i += 1
    
    return segments


def _parse_srt(content: str) -> List[Dict]:
    """Parse SRT subtitle format."""
    segments = []
    blocks = re.split(r"\n\n+", content.strip())
    
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            # Second line should be timestamp
            time_line = lines[1]
            if "-->" in time_line:
                times = time_line.split("-->")
                start = _parse_timestamp(times[0].strip())
                end = _parse_timestamp(times[1].strip())
                
                text = " ".join(lines[2:])
                
                if text:
                    segments.append({
                        "start": start,
                        "duration": end - start,
                        "text": text
                    })
    
    return segments


def _parse_timestamp(ts: str) -> float:
    """Parse timestamp string to seconds."""
    ts = ts.replace(",", ".")
    parts = ts.split(":")
    
    try:
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        elif len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        else:
            return float(ts)
    except ValueError:
        return 0.0



