import os
import sys
import time
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Delay between requests to avoid rate limiting (seconds)
REQUEST_DELAY = 3

BASE_URL = os.getenv("BASE_URL", "http://localhost:2277")
API_KEY = os.getenv("API_KEY", "supersecretapikey")

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


def test_youtube_subscriptions():
    """Test the YouTube subscriptions endpoint."""
    url = f"{BASE_URL}/api/v1/youtube/subscriptions"
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    params = {
        "max_results": 50
    }
    
    try:
        print(f"Testing: {url}")
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success! Found {data.get('total_results', 0)} subscriptions.\n")
            
            subscriptions = data.get("subscriptions", [])
            for sub in subscriptions:
                print(f"- {sub.get('channel_name')} ({sub.get('channel_id')})")
                print(f"  URL: {sub.get('channel_url')}\n")
            
            print(f"\nFull JSON Response:")
            print(json.dumps(data, indent=2))
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                pass
                
    except requests.exceptions.ConnectionError:
        print(f"❌ Failed to connect to {BASE_URL}")
        print("Make sure the server is running.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_youtube_subscriptions_with_channel_id():
    """Test the YouTube subscriptions endpoint with a specific channel ID."""
    url = f"{BASE_URL}/api/v1/youtube/subscriptions"
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    channel_id = os.getenv("YOUTUBE_CHANNEL_ID", "UC6S2pe9IBZkRuY1T_yZnIWQ")
    
    params = {
        "channel_id": channel_id,
        "max_results": 10
    }
    
    try:
        print(f"\nTesting with channel_id: {channel_id}")
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {data.get('total_results', 0)} subscriptions.")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_extract_channel_id(max_channels: int = 5):
    """Test the channel ID extraction endpoint with test channels."""
    url = f"{BASE_URL}/api/v1/youtube/channel-id"
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    test_channels = load_test_channels()
    if not test_channels:
        print("❌ No test channels loaded. Using fallback URLs.")
        test_channels = [
            {"account_name": "MrBeast", "account_url": "https://www.youtube.com/@MrBeast"},
            {"account_name": "PewDiePie", "account_url": "https://www.youtube.com/@pewdiepie"},
        ]
    
    test_channels = test_channels[:max_channels]
    
    print(f"Testing {len(test_channels)} channel(s)...")
    
    results = []
    for idx, channel in enumerate(test_channels, 1):
        channel_url = channel.get("account_url", "")
        channel_name = channel.get("account_name", "Unknown")
        
        if not channel_url:
            print(f"\n[{idx}/{len(test_channels)}] Skipping {channel_name}: No URL provided")
            continue
        
        # Add delay between requests to be respectful to YouTube
        if idx > 1:
            print(f"   Waiting {REQUEST_DELAY}s before next request...")
            time.sleep(REQUEST_DELAY)
        
        params = {"url": channel_url}
        
        try:
            print(f"\n[{idx}/{len(test_channels)}] Testing: {channel_name}")
            print(f"   URL: {channel_url}")
            response = requests.get(url, headers=headers, params=params)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                channel_id = data.get('channel_id', 'N/A')
                channel_url_result = data.get('channel_url', 'N/A')
                print(f"   ✅ Success!")
                print(f"   Channel ID: {channel_id}")
                print(f"   Channel URL: {channel_url_result}")
                results.append({
                    "account_name": channel_name,
                    "account_url": channel_url,
                    "channel_id": channel_id,
                    "channel_url": channel_url_result,
                    "status": "success"
                })
            elif response.status_code == 429:
                print(f"   ⚠️ Rate limited! (5 requests per minute)")
                print(f"   Stopping tests due to rate limit.")
                break
            else:
                error_text = response.text[:100] if response.text else "No error message"
                print(f"   ❌ Error {response.status_code}: {error_text}")
                results.append({
                    "account_name": channel_name,
                    "account_url": channel_url,
                    "status": "error",
                    "error_code": response.status_code,
                    "error_message": error_text
                })
                    
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            results.append({
                "account_name": channel_name,
                "account_url": channel_url,
                "status": "exception",
                "error_message": str(e)
            })
    
    print(f"\n{'=' * 60}")
    print(f"Test Summary: {len([r for r in results if r.get('status') == 'success'])}/{len(results)} successful")
    print(f"{'=' * 60}")
    
    return results


def batch_test(max_channels: int = 5):
    """Run multiple test scenarios."""
    print("=" * 60)
    print("YouTube API - Batch Test")
    print("=" * 60)
    print()
    
    # print("Test 1: Default channel subscriptions")
    # print("-" * 60)
    # test_youtube_subscriptions()
    
    # print("\n" + "=" * 60)
    # print("Test 2: Specific channel ID")
    # print("-" * 60)
    # test_youtube_subscriptions_with_channel_id()
    
    print("\n" + "=" * 60)
    print(f"Test 3: Extract channel ID from URL (testing {max_channels} channels)")
    print("-" * 60)
    results = test_extract_channel_id(max_channels=max_channels)
    
    print("\n" + "=" * 60)
    print("Batch test completed!")
    print("=" * 60)
    
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
    
    batch_test(max_channels=max_channels)
