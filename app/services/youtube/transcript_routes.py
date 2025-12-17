"""
YouTube transcript routes.
"""
from fastapi import APIRouter, HTTPException, Query, Request
from typing import Optional

from app.core.rate_limiter import limiter, YOUTUBE_RATE_LIMIT
from app.services.youtube.transcript_client import get_video_transcript

router = APIRouter()


@router.get("/transcript")
@limiter.limit(YOUTUBE_RATE_LIMIT)
async def get_transcript(
    request: Request,
    video: str = Query(
        ...,
        description="YouTube video URL or 11-character video ID"
    ),
    language: Optional[str] = Query(
        default=None,
        description="Preferred language code (e.g., 'en', 'es'). Defaults to English."
    )
):
    """
    Get the transcript/captions for a YouTube video.
    
    Returns the full transcript text and timestamped segments.
    Uses auto-generated captions if manual captions are not available.
    
    Rate limit: 5 requests per minute.
    """
    try:
        result = get_video_transcript(video, language=language)
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting transcript: {str(e)}"
        )



