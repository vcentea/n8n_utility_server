"""
YouTube RSS Feed routes for monitoring channels.
"""
from fastapi import APIRouter, HTTPException, Query, Request
from typing import Optional

from app.core.rate_limiter import limiter, YOUTUBE_RATE_LIMIT
from app.services.youtube.rss_client import get_channel_feed

router = APIRouter()


@router.get("/latest-video")
@limiter.limit(YOUTUBE_RATE_LIMIT)
async def get_latest_video(
    request: Request,
    channel_id: str = Query(
        ...,
        description="YouTube channel ID (24-character ID starting with 'UC')"
    )
):
    """
    Get the latest video from a YouTube channel using RSS feed.
    
    This endpoint fetches the channel's RSS feed and returns the most recent video
    with its title, URL, thumbnail, published date, and author information.
    
    No API key required - uses public RSS feed.
    
    Rate limit: 5 requests per minute.
    """
    try:
        result = get_channel_feed(channel_id, max_videos=1)
        
        if not result.get("latest_video"):
            raise HTTPException(
                status_code=404,
                detail="No videos found for this channel"
            )
        
        # Return clean response without duplication
        return {
            "channel_id": result["channel_id"],
            "channel_title": result["channel_title"],
            "channel_url": result["channel_url"],
            "latest_video": result["latest_video"]
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching channel feed: {str(e)}"
        )


@router.get("/feed")
@limiter.limit(YOUTUBE_RATE_LIMIT)
async def get_channel_videos(
    request: Request,
    channel_id: str = Query(
        ...,
        description="YouTube channel ID (24-character ID starting with 'UC')"
    ),
    max_videos: int = Query(
        default=15,
        ge=1,
        le=15,
        description="Maximum number of videos to return (1-15, RSS feeds typically have 15)"
    )
):
    """
    Get recent videos from a YouTube channel using RSS feed.
    
    This endpoint fetches the channel's RSS feed and returns recent videos
    with their titles, URLs, thumbnails, published dates, and author information.
    
    No API key required - uses public RSS feed.
    YouTube RSS feeds typically contain the 15 most recent videos.
    
    Rate limit: 5 requests per minute.
    """
    try:
        result = get_channel_feed(channel_id, max_videos=max_videos)
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching channel feed: {str(e)}"
        )



