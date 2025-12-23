# Deploy Cookie Fix to Production

## What Was Fixed

1. ✅ **Automatic cookie detection** - Auto-extracts from Firefox in dev
2. ✅ **Proper browser headers** - User-Agent + Referer for server IPs
3. ✅ **Updated yt-dlp** - Fixed nsig extraction issues (2024.12.6 → 2025.12.8)
4. ✅ **Smart fallback** - Cookie file for production, auto-extract for dev

## What Works Now

- ✅ Dev: Automatic cookie extraction from Firefox (tested)
- ✅ Dev: Transcript extraction working
- ✅ Cookies: 814 cookies extracted successfully
- ✅ Headers: Proper User-Agent and Referer added

## Production Deployment Steps

### Step 1: Export Cookies (One-Time)

**You already have Firefox working, so:**

```cmd
cd E:\Google Drive AInnovate\vlad\_PROJECTS\n8n_utility_server
.\export_cookies.bat
```

Select option 1 (Firefox)

This will create `cookies.txt` in your project folder.

**Alternative:** Use browser extension method (see COOKIE_EXPORT_GUIDE.md)

### Step 2: Copy Cookies to Production Server

```bash
scp cookies.txt user@your-production-server:/path/to/n8n_utility_server/cookies.txt
```

Replace:
- `user` with your SSH username
- `your-production-server` with your server IP/domain
- `/path/to/n8n_utility_server/` with actual path

### Step 3: Update .env on Production Server

SSH into your server:

```bash
ssh user@your-production-server
cd /path/to/n8n_utility_server
```

Add these lines to `.env`:

```bash
echo "YOUTUBE_COOKIES_PATH=/app/cookies.txt" >> .env
echo "YOUTUBE_COOKIES_FILE=./cookies.txt" >> .env
```

### Step 4: Rebuild Docker Container

This will:
- Pull updated code with cookie detection
- Install updated yt-dlp (2025.12.8)
- Mount cookies.txt into container

```bash
./update_docker.sh
```

Or manually:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Step 5: Verify It's Working

Check logs to confirm cookies are loaded:

```bash
docker-compose logs | grep cookies
```

You should see:
```
Using cookies from file: /app/cookies.txt
```

Or:
```
Using cookies from browser: firefox
```

Test the transcript endpoint:

```bash
curl -X GET "http://your-server:2277/api/youtube/transcript?video=jNQXAC9IVRw" \
  -H "X-API-Key: your-api-key"
```

Should return transcript data (not 400 error).

## Files Changed (Already Committed)

- ✅ `app/services/youtube/transcript_client.py` - Cookie auto-detection + headers
- ✅ `app/config.py` - Added YOUTUBE_COOKIES_PATH
- ✅ `docker-compose.yml` - Cookie volume mount
- ✅ `requirements.txt` - Updated yt-dlp version
- ✅ `.env` - Cookie configuration (local)
- ✅ `.gitignore` - Added cookies.txt
- ✅ `export_cookies.bat` - Firefox prioritized
- ✅ Documentation created

## Troubleshooting

### "400 - authentication required" still happening

1. **Verify cookies.txt exists on server:**
   ```bash
   ls -la /path/to/n8n_utility_server/cookies.txt
   ```

2. **Check it's not empty:**
   ```bash
   head -20 /path/to/n8n_utility_server/cookies.txt
   ```

3. **Verify Docker mount:**
   ```bash
   docker-compose exec utility-service ls -la /app/cookies.txt
   ```

4. **Check logs:**
   ```bash
   docker-compose logs -f utility-service
   ```

### "Cookies expired"

Cookies typically last 2-4 weeks. If they expire:

1. Re-export from Firefox (Step 1)
2. Copy to server again (Step 2)
3. Restart container: `docker-compose restart utility-service`

### "nsig extraction failed"

This means yt-dlp is outdated. Make sure you rebuilt with `--no-cache`:

```bash
docker-compose build --no-cache
docker-compose up -d
```

## Success Criteria

✅ Dev works with auto-extracted cookies  
✅ Production builds without errors  
✅ Logs show "Using cookies from file"  
✅ Transcript requests return 200 OK  
✅ No more "400 - authentication required"  

## Maintenance

**Cookie Refresh (every 2-4 weeks):**
1. Re-run `export_cookies.bat`
2. `scp cookies.txt` to server
3. `docker-compose restart utility-service`

**Monitor for YouTube changes:**
- If transcripts start failing, update yt-dlp
- Check yt-dlp GitHub for known issues

## Summary

**Before:**
- ❌ 400 error in production
- ❌ Manual cookie management
- ❌ Outdated yt-dlp

**After:**
- ✅ Auto-cookie detection (dev)
- ✅ Server IP bypass (cookies + headers)
- ✅ Latest yt-dlp version
- ✅ Smart fallbacks

**Deploy now:** Follow steps 1-5 above! 🚀


