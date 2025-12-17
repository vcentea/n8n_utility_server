from fastapi import APIRouter, HTTPException, Query, Request
from typing import Optional

from app.core.rate_limiter import limiter, YOUTUBE_RATE_LIMIT
from app.services.youtube.client import get_public_subscriptions, extract_channel_id

router = APIRouter()


@router.get("/subscriptions")
@limiter.limit(YOUTUBE_RATE_LIMIT)
async def get_subscriptions(
    request: Request,
    channel_id: Optional[str] = Query(
        default=None,
        description="Channel ID to get subscriptions for. Defaults to configured channel."
    ),
    max_results: int = Query(
        default=50,
        ge=1,
        le=50,
        description="Maximum number of results per page (1-50)."
    )
):
    """
    Get public subscriptions for a YouTube channel.
    
    Returns a list of subscribed channels with their names and URLs.
    
    Rate limit: 5 requests per minute.
    """
    try:
        result = get_public_subscriptions(
            channel_id=channel_id,
            max_results=max_results
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching subscriptions: {str(e)}"
        )


@router.get("/channel-id")
@limiter.limit(YOUTUBE_RATE_LIMIT)
async def get_channel_id(
    request: Request,
    url: str = Query(
        ...,
        description="YouTube channel URL (supports /channel/, /@handle, /c/, /user/ formats)"
    )
):
    """
    Extract the channel ID (UCID) from a YouTube channel URL.
    
    The channel ID is a 24-character identifier starting with 'UC' that uniquely
    identifies a YouTube channel. This ID is stable and does not change when
    the channel name or handle changes.
    
    Supported URL formats:
    - https://www.youtube.com/channel/UCxxxxxx
    - https://www.youtube.com/@handle
    - https://www.youtube.com/c/channelname
    - https://www.youtube.com/user/username
    
    Rate limit: 5 requests per minute.
    """
    try:
        result = await extract_channel_id(url)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting channel ID: {str(e)}"
        )
