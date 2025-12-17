"""
Direct test for channel ID extraction without needing the server running.
This tests the extract_channel_id function directly.

Usage:
    python tests/test_channel_extraction_direct.py
    python tests/test_channel_extraction_direct.py 10
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.youtube.client import extract_channel_id

TEST_CHANNELS_FILE = Path(__file__).parent / "youtube_test_channels.json"


def load_test_channels():
    """Load test channels from JSON file."""
    try:
        with open(TEST_CHANNELS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("for_update", {}).get("data", [])
    except FileNotFoundError:
        print(f"❌ Test channels file not found: {TEST_CHANNELS_FILE}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing test channels file: {e}")
        return []


def test_channel_extraction(max_channels: int = 5):
    """Test channel ID extraction directly."""
    test_channels = load_test_channels()
    
    if not test_channels:
        print("❌ No test channels loaded. Using fallback URLs.")
        test_channels = [
            {"account_name": "AI by Hand", "account_url": "https://www.youtube.com/@ai-by-hand"},
            {"account_name": "Fireship", "account_url": "https://www.youtube.com/@Fireship"},
            {"account_name": "n8n", "account_url": "https://www.youtube.com/@n8n-io"},
        ]
    
    test_channels = test_channels[:max_channels]
    
    print("=" * 70)
    print(f"Direct Channel ID Extraction Test - Testing {len(test_channels)} channel(s)")
    print("=" * 70)
    
    results = []
    success_count = 0
    
    for idx, channel in enumerate(test_channels, 1):
        channel_url = channel.get("account_url", "")
        channel_name = channel.get("account_name", "Unknown")
        
        if not channel_url:
            print(f"\n[{idx}/{len(test_channels)}] ⏭️  Skipping {channel_name}: No URL")
            continue
        
        print(f"\n[{idx}/{len(test_channels)}] Testing: {channel_name}")
        print(f"   Input URL: {channel_url}")
        
        try:
            result = extract_channel_id(channel_url)
            channel_id = result.get("channel_id", "N/A")
            output_url = result.get("channel_url", "N/A")
            
            print(f"   ✅ Success!")
            print(f"   Channel ID: {channel_id}")
            print(f"   Output URL: {output_url}")
            
            results.append({
                "account_name": channel_name,
                "input_url": channel_url,
                "channel_id": channel_id,
                "output_url": output_url,
                "status": "success"
            })
            success_count += 1
            
        except ValueError as e:
            print(f"   ❌ ValueError: {str(e)}")
            results.append({
                "account_name": channel_name,
                "input_url": channel_url,
                "status": "error",
                "error": str(e)
            })
        except Exception as e:
            print(f"   ❌ Exception: {type(e).__name__}: {str(e)}")
            results.append({
                "account_name": channel_name,
                "input_url": channel_url,
                "status": "exception",
                "error": f"{type(e).__name__}: {str(e)}"
            })
    
    print("\n" + "=" * 70)
    print(f"Test Summary: {success_count}/{len(results)} successful")
    print("=" * 70)
    
    if results:
        successful = [r for r in results if r.get("status") == "success"]
        if successful:
            print("\n✅ Successful extractions:")
            for r in successful:
                print(f"   - {r['account_name']}: {r['channel_id']}")
        
        failed = [r for r in results if r.get("status") != "success"]
        if failed:
            print("\n❌ Failed extractions:")
            for r in failed:
                print(f"   - {r['account_name']}: {r.get('error', 'Unknown error')}")
    
    return results


if __name__ == "__main__":
    max_channels = 5
    
    if len(sys.argv) > 1:
        try:
            max_channels = int(sys.argv[1])
            if max_channels < 1:
                print("⚠️ Invalid number of channels. Using default: 5")
                max_channels = 5
        except ValueError:
            print("⚠️ Invalid argument. Using default: 5 channels")
            max_channels = 5
    
    test_channel_extraction(max_channels=max_channels)
