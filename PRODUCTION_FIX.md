# Production Fix: YouTube Authentication Issue

## Problem

Getting error: `400 - "This video requires authentication to access."` when calling the YouTube transcript endpoint in production.

## Root Cause

The `YOUTUBE_API_KEY` in `.env` is only used for the YouTube Data API (subscriptions). For video transcript extraction, `yt-dlp` needs browser cookies to access age-restricted or member-only videos.

## Solution Steps

### 1. Export YouTube Cookies

On your local machine (where you're logged into YouTube):

**Option A: Using Browser Extension (Recommended)**

1. Install extension:
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt extension](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Go to YouTube and make sure you're logged in
3. Click the extension icon
4. Export/Download cookies
5. Save as `cookies.txt`

**Option B: Using yt-dlp (from project venv)**

```bash
# IMPORTANT: Use the project's virtual environment
# On Windows:
venv\Scripts\activate.bat
# On Linux/Mac:
source venv/bin/activate

# Export cookies from Chrome
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Or from Firefox
yt-dlp --cookies-from-browser firefox --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### 2. Copy Cookies to Production Server

```bash
# From your local machine
scp cookies.txt user@your-server:/path/to/n8n_utility_server/cookies.txt

# Example:
scp cookies.txt root@your-server.com:/root/n8n_utility_server/cookies.txt
```

### 3. Update .env on Production Server

SSH into your production server and update the `.env` file:

```bash
ssh user@your-server
cd /path/to/n8n_utility_server
nano .env
```

Add these lines to your `.env`:

```env
# YouTube Cookies (for age-restricted/members-only videos)
YOUTUBE_COOKIES_PATH=/app/cookies.txt
YOUTUBE_COOKIES_FILE=./cookies.txt
```

### 4. Rebuild and Restart Container

```bash
# On Ubuntu server
./update_docker.sh

# Or manually
docker-compose down
docker-compose up -d --build
```

### 5. Verify the Fix

Check logs to confirm cookies are loaded:

```bash
docker-compose logs -f | grep cookies
```

You should see:
```
Using cookies from: /app/cookies.txt
```

Test the endpoint:

```bash
curl -X GET "http://your-server:2277/api/youtube/transcript?video=VIDEO_ID" \
  -H "X-API-Key: your-api-key"
```

## Security Checklist

- ✅ Cookies file is in `.gitignore`
- ✅ Docker volume is mounted as read-only (`:ro`)
- ✅ Cookies are not committed to version control
- ⚠️ Cookies will expire after ~2-4 weeks (need to refresh periodically)

## Troubleshooting

### Still getting authentication error?

1. **Check file permissions:**
```bash
ls -l cookies.txt
# Should be readable
chmod 644 cookies.txt
```

2. **Verify cookies file is not empty:**
```bash
head cookies.txt
# Should show cookie data
```

3. **Check Docker volume mount:**
```bash
docker-compose exec utility-service ls -la /app/cookies.txt
# Should exist inside container
```

4. **Re-export fresh cookies:**
   - Log out and log back into YouTube
   - Export cookies again
   - Replace the old `cookies.txt`
   - Restart container

### Cookies expired?

Re-export cookies following Step 1 and restart the service:

```bash
# After copying new cookies.txt
docker-compose restart utility-service
```

## What Works Without Cookies?

| Video Type | Works Without Cookies? |
|-----------|----------------------|
| Public videos | ✅ Yes |
| Unlisted videos | ✅ Yes (with URL) |
| Age-restricted videos | ❌ No - needs cookies |
| Members-only videos | ❌ No - needs cookies |
| Private videos | ❌ No - needs cookies |

## Files Changed

The following files have been updated to support cookies:

- `app/config.py` - Added `YOUTUBE_COOKIES_PATH` configuration
- `app/services/youtube/transcript_client.py` - Added cookie support to yt-dlp
- `docker-compose.yml` - Added cookie volume mount
- `.env` - Added cookie configuration
- `.gitignore` - Added `cookies.txt` to prevent commits

See `YOUTUBE_COOKIES.md` for detailed documentation.


