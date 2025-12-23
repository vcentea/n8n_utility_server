# YouTube Cookies Setup

## Why Are Cookies Needed?

Some YouTube videos require authentication to access:
- Age-restricted videos
- Members-only videos
- Private videos shared with your account
- Videos with other access restrictions

The `YOUTUBE_API_KEY` only works for the YouTube Data API (subscriptions endpoint). For video transcript extraction, `yt-dlp` needs your browser cookies to authenticate.

## How to Export YouTube Cookies

### Method 1: Using Browser Extension (Recommended)

1. **Install a Cookie Export Extension:**
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Export Cookies:**
   - Go to YouTube and make sure you're logged in
   - Click the extension icon
   - Click "Export" or "Download"
   - Save the file as `cookies.txt`

3. **Place the File:**
   - Copy `cookies.txt` to your project root directory (same level as `docker-compose.yml`)

### Method 2: Using yt-dlp (Alternative)

**IMPORTANT:** Must use the project's virtual environment!

```bash
# Windows - Activate venv first
cd /path/to/n8n_utility_server
venv\Scripts\activate.bat

# Linux/Mac - Activate venv first
cd /path/to/n8n_utility_server
source venv/bin/activate

# Export cookies from Chrome
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Or from Firefox
yt-dlp --cookies-from-browser firefox --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Method 3: Using Export Script (Easiest)

We've provided scripts that automatically use the project's venv:

```bash
# Windows
export_cookies.bat

# Linux/Mac
./export_cookies.sh
```

## Configuration

### Local Development (.env)

```env
# Path inside the container
YOUTUBE_COOKIES_PATH=/app/cookies.txt
# Path on your host machine
YOUTUBE_COOKIES_FILE=./cookies.txt
```

### Production Server

1. **Copy your cookies.txt to the server:**

```bash
scp cookies.txt user@your-server:/path/to/project/cookies.txt
```

2. **Update .env on server:**

```env
YOUTUBE_COOKIES_PATH=/app/cookies.txt
YOUTUBE_COOKIES_FILE=/path/to/project/cookies.txt
```

3. **Rebuild the container:**

```bash
# On Ubuntu server
./update_docker.sh

# Or manually
docker-compose down
docker-compose up -d --build
```

## Security Notes

⚠️ **IMPORTANT:**
- Cookies contain sensitive authentication data
- Add `cookies.txt` to `.gitignore` (already done)
- Never commit cookies to version control
- Rotate cookies periodically for security
- Use read-only volume mount in Docker (`:ro`)

## Troubleshooting

### "This video requires authentication to access"

This error means:
1. Cookies are not configured or expired
2. The cookies file path is incorrect
3. You need to re-export fresh cookies from your browser

### Verify Cookies Are Loaded

Check the logs:
```bash
docker-compose logs | grep cookies
```

You should see:
```
Using cookies from: /app/cookies.txt
```

### Test Locally First

Before deploying to production, test with a restricted video:

```bash
# Start local server
./start_local.bat  # Windows
./start_local.sh   # Linux/Mac

# Test with a restricted video
curl -X POST "http://localhost:2277/api/youtube/transcript" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"video_url": "VIDEO_URL_HERE"}'
```

## Cookie Expiration

YouTube cookies typically expire after:
- 2 weeks to 1 month for regular sessions
- Shorter if you clear browser data
- Immediately if you log out

**Solution:** Re-export cookies when they expire.

## Automated Cookie Refresh (Advanced)

For production environments, consider:
1. Setting up a cron job to refresh cookies
2. Using Selenium/Playwright to maintain an authenticated session
3. Monitoring for authentication failures and alerting

## Without Cookies

If you don't configure cookies, the service will still work for:
- ✅ Public videos
- ✅ Unlisted videos (with URL)
- ✅ Videos without age restrictions
- ❌ Age-restricted videos
- ❌ Members-only videos
- ❌ Private videos


