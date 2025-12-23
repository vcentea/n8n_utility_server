# Cookie Export Guide - Two Methods

## ⚠️ Common Issue: Browser Database Lock

**Error:** `Could not copy Chrome cookie database`

**Cause:** Edge/Chrome lock their cookie databases while running (including background processes)

---

## Method 1: Browser Extension (EASIEST - Recommended) ⭐

### Why This Method?
- ✅ Works while browser is running
- ✅ No database lock issues
- ✅ Most reliable
- ✅ One-click export

### Steps:

#### For Edge:

1. **Install Extension:**
   ```
   https://microsoftedge.microsoft.com/addons/detail/get-cookiestxt-locally/hbihflbpfdeopgegegknkfplckkomdja
   ```
   Or search: "Get cookies.txt LOCALLY" in Edge Add-ons

2. **Export:**
   - Go to `youtube.com` (make sure you're logged in)
   - Click the extension icon (puzzle piece icon)
   - Click "Export" or "Download"
   - Choose location: `E:\Google Drive AInnovate\vlad\_PROJECTS\n8n_utility_server\`
   - Save as: `cookies.txt`

3. **Done!** ✅

#### For Chrome:

1. **Install Extension:**
   ```
   https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
   ```

2. Follow same steps as Edge above

---

## Method 2: Using yt-dlp Script

### Only works if browser is COMPLETELY closed!

#### Steps:

1. **Close Edge/Chrome Completely:**

   **Windows:**
   - Press `Ctrl + Shift + Esc` (Task Manager)
   - Find ALL `Microsoft Edge` or `Chrome` processes
   - Right-click each → "End Task"
   - Look for:
     - Microsoft Edge
     - Microsoft Edge WebView2
     - msedge.exe
     - chrome.exe
     - All related processes

   **Verify it's closed:**
   - No Edge/Chrome icon in system tray
   - No processes in Task Manager

2. **Run Export Script:**

   ```cmd
   cd E:\Google Drive AInnovate\vlad\_PROJECTS\n8n_utility_server
   export_cookies.bat
   ```

3. **Select your browser** (it must be closed!)

---

## Comparison

| Method | Pros | Cons |
|--------|------|------|
| **Browser Extension** | ✅ Works with browser open<br>✅ No lock issues<br>✅ One-click | Requires extension install |
| **yt-dlp Script** | ✅ Automated<br>✅ No extension needed | ❌ Browser must be closed<br>❌ Can have lock issues |

---

## After Export (Both Methods)

Once you have `cookies.txt`:

```bash
# 1. Verify the file exists
dir cookies.txt

# 2. Copy to production server
scp cookies.txt user@your-server:/path/to/n8n_utility_server/

# 3. SSH to server
ssh user@your-server

# 4. Update .env
cd /path/to/n8n_utility_server
echo "YOUTUBE_COOKIES_PATH=/app/cookies.txt" >> .env
echo "YOUTUBE_COOKIES_FILE=./cookies.txt" >> .env

# 5. Rebuild
./update_docker.sh

# 6. Verify
docker-compose logs | grep cookies
# Should see: "Using cookies from: /app/cookies.txt"
```

---

## Troubleshooting

### "ERROR: Could not copy Chrome cookie database"
- **Solution:** Use Method 1 (Browser Extension) instead
- **Or:** Make absolutely sure the browser is fully closed (check Task Manager)

### "cookies.txt is empty"
- Make sure you're logged into YouTube when exporting
- Try the other method

### "Still getting 400 error in production"
- Verify cookies.txt was copied to server: `ls -la cookies.txt`
- Check it's not empty: `head cookies.txt`
- Verify container mount: `docker-compose exec utility-service ls -la /app/cookies.txt`
- Check logs: `docker-compose logs | grep cookies`

---

## Quick Decision Guide

```
Are you comfortable installing a browser extension?
├── YES → Use Method 1 (Extension) - Takes 2 minutes
└── NO  → Use Method 2 (Script) - Must close browser completely
```

**Recommendation:** Use **Method 1 (Extension)** - it's faster and more reliable! 🚀

