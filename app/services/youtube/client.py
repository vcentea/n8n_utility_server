import re
import json
import logging
import asyncio
import requests
from urllib.parse import unquote
from typing import Dict, Any, Optional, List

from app.config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID

logger = logging.getLogger(__name__)

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"

CHANNEL_ID_REGEX = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
CHANNEL_ID_URL_PATTERN = re.compile(r"/channel/(UC[a-zA-Z0-9_-]{22})")
CANONICAL_LINK_PATTERN = re.compile(
    r'<link[^>]+rel="canonical"[^>]+href="https://www\.youtube\.com/channel/([^"]+)"'
)

# Consent button selectors for Playwright
CONSENT_BUTTON_SELECTORS = [
    'button:has-text("Accept all")',
    'button:has-text("Accept")',
    'button:has-text("I agree")',
    'button[aria-label="Accept all"]',
    'button[aria-label="Accept the use of cookies"]',
    '[aria-label="Accept all"]',
    'form[action*="consent"] button',
]


def get_public_subscriptions(
    channel_id: Optional[str] = None,
    max_results: int = 50
) -> Dict[str, Any]:
    """
    Get public subscriptions for a YouTube channel.
    
    Args:
        channel_id: Channel ID to get subscriptions for. Defaults to configured channel.
        max_results: Maximum number of results per page (max 50).
    
    Returns:
        Dictionary containing subscription data with channel names and URLs.
    """
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY is not configured")
    
    target_channel_id = channel_id or YOUTUBE_CHANNEL_ID
    if not target_channel_id:
        raise ValueError("Channel ID is required")
    
    url = f"{YOUTUBE_API_BASE_URL}/subscriptions"
    
    params = {
        "part": "snippet",
        "channelId": target_channel_id,
        "key": YOUTUBE_API_KEY,
        "maxResults": min(max_results, 50)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        subscriptions = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            resource_id = snippet.get("resourceId", {})
            sub_channel_id = resource_id.get("channelId", "")
            
            subscription_data = {
                "channel_name": snippet.get("title", ""),
                "channel_id": sub_channel_id,
                "channel_url": f"https://www.youtube.com/channel/{sub_channel_id}" if sub_channel_id else "",
                "description": snippet.get("description", ""),
                "thumbnail": snippet.get("thumbnails", {}).get("default", {}).get("url", "")
            }
            subscriptions.append(subscription_data)
        
        return {
            "total_results": data.get("pageInfo", {}).get("totalResults", 0),
            "subscriptions": subscriptions
        }
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            raise ValueError(
                "Error 403: Forbidden. The subscriptions are still marked as 'Private' "
                "in the YouTube account settings. Note: It can take 10-15 mins for "
                "privacy setting changes to propagate."
            )
        raise ValueError(f"YouTube API error: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to connect to YouTube API: {str(e)}")


def _is_valid_channel_id(channel_id: str) -> bool:
    """Validate that a string matches the YouTube channel ID pattern (UC + 22 chars)."""
    return bool(CHANNEL_ID_REGEX.match(channel_id))


def _extract_json_object(html: str, start_marker: str) -> Optional[str]:
    """
    Extract a JSON object from HTML using brace counting.
    
    Args:
        html: The HTML content to search
        start_marker: The marker to find (e.g., 'ytInitialData')
    
    Returns:
        The extracted JSON string, or None if not found
    """
    marker_pos = html.find(start_marker)
    if marker_pos == -1:
        return None
    
    brace_start = html.find("{", marker_pos)
    if brace_start == -1:
        return None
    
    depth = 0
    in_string = False
    escape_next = False
    
    for i, char in enumerate(html[brace_start:], start=brace_start):
        if escape_next:
            escape_next = False
            continue
            
        if char == "\\":
            escape_next = True
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
            
        if in_string:
            continue
            
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return html[brace_start:i + 1]
    
    return None


def _find_channel_ids_recursive(obj: Any, ids: List[str]) -> None:
    """
    Recursively traverse a JSON object and collect all channelId values.
    
    Args:
        obj: The object to traverse (dict, list, or primitive)
        ids: List to collect found channel IDs
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "channelId" and isinstance(value, str):
                if _is_valid_channel_id(value):
                    ids.append(value)
            _find_channel_ids_recursive(value, ids)
    elif isinstance(obj, list):
        for item in obj:
            _find_channel_ids_recursive(item, ids)


def _get_nested_value(obj: Any, path: list) -> Optional[str]:
    """
    Safely get a nested value from a dictionary or list.
    
    Args:
        obj: The object to traverse (dict or list)
        path: List of keys (strings for dicts, ints for lists) representing the path
    
    Returns:
        The value at the path, or None if not found
    """
    current = obj
    for key in path:
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            if isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                return None
        else:
            return None
    return current if isinstance(current, str) else None


def _extract_channel_id_from_json(html: str) -> Optional[str]:
    """
    Extract channel ID from ytInitialData JSON embedded in HTML.
    
    Priority:
    1. header.c4TabbedHeaderRenderer.channelId
    2. metadata.channelMetadataRenderer.externalId
    3. Any valid channelId found in the JSON (most common one)
    
    Args:
        html: The HTML content containing ytInitialData
    
    Returns:
        The extracted channel ID, or None if not found
    """
    json_str = _extract_json_object(html, "ytInitialData")
    if not json_str:
        json_str = _extract_json_object(html, "ytInitialPlayerResponse")
    
    if not json_str:
        return None
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return None
    
    # Priority paths - these contain the main channel ID
    priority_paths = [
        ["header", "c4TabbedHeaderRenderer", "channelId"],
        ["metadata", "channelMetadataRenderer", "externalId"],
        ["header", "pageHeaderRenderer", "content", "pageHeaderViewModel", 
         "actions", "flexibleActionsViewModel", "actionsRows", 0, 
         "actions", 0, "buttonViewModel", "onTap", "innertubeCommand", 
         "browseEndpoint", "browseId"],
    ]
    
    for path in priority_paths:
        channel_id = _get_nested_value(data, path)
        if channel_id and _is_valid_channel_id(channel_id):
            logger.info(f"Found channel ID via priority path: {channel_id}")
            return channel_id
    
    # Fallback: collect all channel IDs and return the most common one
    all_ids: List[str] = []
    _find_channel_ids_recursive(data, all_ids)
    
    if all_ids:
        from collections import Counter
        counter = Counter(all_ids)
        most_common = counter.most_common(1)[0][0]
        logger.info(f"Found channel ID via fallback (most common): {most_common}")
        return most_common
    
    return None


def _extract_channel_id_from_canonical(html: str) -> Optional[str]:
    """
    Extract channel ID from the canonical link in HTML head.
    
    Args:
        html: The HTML content
    
    Returns:
        The extracted channel ID, or None if not found
    """
    match = CANONICAL_LINK_PATTERN.search(html)
    if match:
        channel_id = match.group(1)
        if _is_valid_channel_id(channel_id):
            logger.info(f"Found channel ID via canonical link: {channel_id}")
            return channel_id
    return None


def _fetch_youtube_page_sync(url: str) -> str:
    """
    Fetch a YouTube page using Playwright via subprocess.
    This avoids asyncio conflicts with uvicorn on Windows.
    
    Args:
        url: The YouTube URL to fetch
    
    Returns:
        The page HTML content
    """
    import subprocess
    import sys
    import os
    
    logger.info(f"Fetching YouTube page with Playwright subprocess: {url}")
    
    # Get path to worker script
    worker_script = os.path.join(
        os.path.dirname(__file__), 
        "playwright_worker.py"
    )
    
    # Get path to Python executable (use venv if available)
    python_exe = sys.executable
    
    try:
        result = subprocess.run(
            [python_exe, worker_script, url],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"Worker script error: {result.stderr}")
            raise ValueError(f"Worker script failed: {result.stderr}")
        
        output = json.loads(result.stdout)
        
        if not output.get("success"):
            raise ValueError(output.get("error", "Unknown error"))
        
        html_content = output.get("html", "")
        title = output.get("title", "")
        
        logger.info(f"Page fetched successfully. Title: {title}, HTML length: {len(html_content)}")
        
        return html_content
        
    except subprocess.TimeoutExpired:
        raise ValueError("Timeout fetching YouTube page")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse worker output: {e}")
        raise ValueError("Failed to parse worker output")


async def _fetch_youtube_page_with_playwright(url: str) -> str:
    """
    Fetch a YouTube page using Playwright in a subprocess.
    Uses asyncio.to_thread to avoid blocking.
    
    Args:
        url: The YouTube URL to fetch
    
    Returns:
        The page HTML content
    
    Raises:
        ValueError: If page cannot be fetched
    """
    return await asyncio.to_thread(_fetch_youtube_page_sync, url)


async def extract_channel_id(channel_url: str) -> Dict[str, Any]:
    """
    Extract the channel ID (UCID) from a YouTube channel URL.
    
    Uses Playwright to fetch the page and handle consent dialogs,
    then extracts the channel ID from ytInitialData JSON.
    
    Args:
        channel_url: YouTube channel URL (supports /channel/, /@handle, /c/, /user/ formats)
    
    Returns:
        Dictionary containing channel_id and channel_url.
    
    Raises:
        ValueError: If channel ID cannot be extracted
    """
    if not channel_url:
        raise ValueError("Channel URL is required")
    
    channel_url = channel_url.strip()
    
    # Decode URL-encoded URLs (handles n8n encoding)
    original_url = channel_url
    channel_url = unquote(channel_url)
    
    logger.info(f"Extracting channel ID - Original: {original_url}, Decoded: {channel_url}")
    
    if not channel_url.startswith(("http://", "https://")):
        channel_url = f"https://{channel_url}"
    
    # Quick check: if URL already contains channel ID, extract directly
    direct_match = CHANNEL_ID_URL_PATTERN.search(channel_url)
    if direct_match:
        channel_id = direct_match.group(1)
        if _is_valid_channel_id(channel_id):
            logger.info(f"Extracted channel ID directly from URL: {channel_id}")
            return {
                "channel_id": channel_id,
                "channel_url": f"https://www.youtube.com/channel/{channel_id}"
            }
    
    try:
        # Fetch page using Playwright
        html_content = await _fetch_youtube_page_with_playwright(channel_url)
        
        # Check if ytInitialData is present
        if "ytInitialData" not in html_content:
            logger.error("ytInitialData not found in page content")
            raise ValueError(
                "Could not load YouTube page properly. "
                "The page may be blocked or the URL is invalid."
            )
        
        # Method 1: Try ytInitialData JSON parsing
        channel_id = _extract_channel_id_from_json(html_content)
        if channel_id:
            return {
                "channel_id": channel_id,
                "channel_url": f"https://www.youtube.com/channel/{channel_id}"
            }
        
        # Method 2: Try canonical link
        channel_id = _extract_channel_id_from_canonical(html_content)
        if channel_id:
            return {
                "channel_id": channel_id,
                "channel_url": f"https://www.youtube.com/channel/{channel_id}"
            }
        
        logger.error(f"Could not extract channel ID from: {channel_url}")
        raise ValueError(
            "Could not find channel ID in page source. "
            "Make sure the URL is a valid YouTube channel page."
        )
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error fetching channel page: {e}")
        raise ValueError(f"Failed to fetch channel page: {str(e)}")
