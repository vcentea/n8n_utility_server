"""
YouTube RSS Feed client for fetching latest videos from a channel.
"""
import requests
import xml.etree.ElementTree as ET
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml"

# XML namespaces used in YouTube RSS feeds
NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/"
}


def get_channel_feed(channel_id: str, max_videos: int = 1) -> Dict[str, Any]:
    """
    Fetch the RSS feed for a YouTube channel and return latest video(s).
    
    Args:
        channel_id: YouTube channel ID (UC...)
        max_videos: Maximum number of videos to return (default: 1)
    
    Returns:
        Dictionary containing channel info and latest videos.
    
    Raises:
        ValueError: If channel ID is invalid or feed cannot be fetched
    """
    if not channel_id:
        raise ValueError("Channel ID is required")
    
    channel_id = channel_id.strip()
    
    if not channel_id.startswith("UC") or len(channel_id) != 24:
        raise ValueError(
            "Invalid channel ID format. Must start with 'UC' and be 24 characters."
        )
    
    url = f"{YOUTUBE_RSS_URL}?channel_id={channel_id}"
    
    logger.info(f"Fetching RSS feed for channel: {channel_id}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Channel not found: {channel_id}")
        raise ValueError(f"Failed to fetch RSS feed: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to connect to YouTube RSS: {str(e)}")
    
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        logger.error(f"Failed to parse RSS XML: {e}")
        raise ValueError("Failed to parse RSS feed")
    
    # Extract channel info
    channel_title = _get_text(root, "atom:title")
    channel_author = _get_text(root, "atom:author/atom:name")
    channel_url = _get_attr(root, "atom:link[@rel='alternate']", "href")
    channel_published = _get_text(root, "atom:published")
    
    # Extract videos (entries)
    entries = root.findall("atom:entry", NAMESPACES)
    
    videos = []
    for entry in entries[:max_videos]:
        video = _parse_video_entry(entry)
        if video:
            videos.append(video)
    
    return {
        "channel_id": channel_id,
        "channel_title": channel_title,
        "channel_url": channel_url or f"https://www.youtube.com/channel/{channel_id}",
        "channel_author": channel_author,
        "channel_published": channel_published,
        "video_count": len(videos),
        "videos": videos,
        "latest_video": videos[0] if videos else None
    }


def _get_text(element: ET.Element, path: str) -> Optional[str]:
    """Get text content from an XML element using a path."""
    found = element.find(path, NAMESPACES)
    return found.text if found is not None else None


def _get_attr(element: ET.Element, path: str, attr: str) -> Optional[str]:
    """Get an attribute value from an XML element using a path."""
    found = element.find(path, NAMESPACES)
    return found.get(attr) if found is not None else None


def _parse_video_entry(entry: ET.Element) -> Optional[Dict[str, Any]]:
    """Parse a single video entry from the RSS feed."""
    try:
        video_id = _get_text(entry, "yt:videoId")
        title = _get_text(entry, "atom:title")
        published = _get_text(entry, "atom:published")
        updated = _get_text(entry, "atom:updated")
        
        # Get video URL
        video_url = _get_attr(entry, "atom:link[@rel='alternate']", "href")
        if not video_url and video_id:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get author info
        author_name = _get_text(entry, "atom:author/atom:name")
        author_url = _get_text(entry, "atom:author/atom:uri")
        
        # Get media info
        media_group = entry.find("media:group", NAMESPACES)
        description = None
        thumbnail_url = None
        views = None
        
        if media_group is not None:
            description = _get_text(media_group, "media:description")
            thumbnail = media_group.find("media:thumbnail", NAMESPACES)
            if thumbnail is not None:
                thumbnail_url = thumbnail.get("url")
            
            # Get view count from statistics
            stats = media_group.find("media:community/media:statistics", NAMESPACES)
            if stats is not None:
                views = stats.get("views")
        
        return {
            "video_id": video_id,
            "title": title,
            "url": video_url,
            "published": published,
            "updated": updated,
            "author": author_name,
            "author_url": author_url,
            "description": description,
            "thumbnail": thumbnail_url,
            "views": int(views) if views else None
        }
        
    except Exception as e:
        logger.error(f"Failed to parse video entry: {e}")
        return None



