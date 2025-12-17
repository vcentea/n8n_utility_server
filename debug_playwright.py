"""
Test script for YouTube channel ID extraction.
Run: venv\Scripts\python.exe debug_playwright.py [url]
"""
import sys
import os
import subprocess
import json
import re
from urllib.parse import unquote

CHANNEL_ID_REGEX = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
CHANNEL_ID_URL_PATTERN = re.compile(r"/channel/(UC[a-zA-Z0-9_-]{22})")


def is_valid_channel_id(channel_id: str) -> bool:
    return bool(CHANNEL_ID_REGEX.match(channel_id))


def extract_from_json(html: str):
    """Extract channel ID from ytInitialData."""
    marker = "ytInitialData"
    pos = html.find(marker)
    if pos == -1:
        return None
    
    brace_start = html.find("{", pos)
    if brace_start == -1:
        return None
    
    depth = 0
    in_string = False
    escape = False
    
    for i, c in enumerate(html[brace_start:], start=brace_start):
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                json_str = html[brace_start:i + 1]
                break
    else:
        return None
    
    try:
        data = json.loads(json_str)
    except:
        return None
    
    # Priority paths
    paths = [
        ["header", "c4TabbedHeaderRenderer", "channelId"],
        ["metadata", "channelMetadataRenderer", "externalId"],
    ]
    
    for path in paths:
        obj = data
        for key in path:
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                obj = None
                break
        if obj and isinstance(obj, str) and is_valid_channel_id(obj):
            return obj
    
    return None


def test_channel_extraction(url: str):
    """Test channel ID extraction for a given URL."""
    print(f"\nTesting URL: {url}")
    print("-" * 60)
    
    try:
        url = unquote(url.strip())
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        
        # Check direct URL
        match = CHANNEL_ID_URL_PATTERN.search(url)
        if match and is_valid_channel_id(match.group(1)):
            print(f"SUCCESS! (direct from URL)")
            print(f"  Channel ID:  {match.group(1)}")
            return True
        
        # Call worker script
        worker = os.path.join(
            os.path.dirname(__file__),
            "app", "services", "youtube", "playwright_worker.py"
        )
        
        result = subprocess.run(
            [sys.executable, worker, url],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"FAILED: Worker error: {result.stderr}")
            return False
        
        output = json.loads(result.stdout)
        if not output.get("success"):
            print(f"FAILED: {output.get('error')}")
            return False
        
        html = output.get("html", "")
        print(f"  Page title: {output.get('title')}")
        print(f"  HTML length: {len(html)}")
        print(f"  Has ytInitialData: {'ytInitialData' in html}")
        
        # Extract channel ID
        channel_id = extract_from_json(html)
        if channel_id:
            print(f"SUCCESS! (from JSON)")
            print(f"  Channel ID:  {channel_id}")
            print(f"  Channel URL: https://www.youtube.com/channel/{channel_id}")
            return True
        
        print(f"FAILED: Could not extract channel ID from page")
        return False
        
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def main():
    test_urls = [
        "https://www.youtube.com/@Fireship",
        "https://www.youtube.com/@ai-by-hand",
        "https://www.youtube.com/channel/UCsBjURrPoezykLs9EqgamOA",
    ]
    
    if len(sys.argv) > 1:
        test_urls = [sys.argv[1]]
    
    print("YouTube Channel ID Extraction Test")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for url in test_urls:
        if test_channel_extraction(url):
            success += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {success} passed, {failed} failed")


if __name__ == "__main__":
    main()
