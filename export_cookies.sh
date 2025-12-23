#!/bin/bash
# Export YouTube cookies from your local browser
# This script uses yt-dlp to extract cookies from your browser

echo "================================================================"
echo "  Exporting YouTube Cookies from Browser"
echo "================================================================"
echo ""

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    echo "Activating virtual environment..."
    source venv/Scripts/activate
else
    echo "[ERROR] Virtual environment not found!"
    echo "Please run setup.sh first to create the venv."
    echo ""
    exit 1
fi

# Check if yt-dlp is available
if ! command -v yt-dlp &> /dev/null; then
    echo "[ERROR] yt-dlp not found in venv!"
    echo ""
    echo "The virtual environment might not be set up correctly."
    echo "Please run setup.sh first."
    echo ""
    exit 1
fi

echo "Select your browser:"
echo "  1. Chrome"
echo "  2. Edge"
echo "  3. Firefox"
echo "  4. Safari (Mac only)"
echo ""
read -p "Enter choice (1-4): " browser_choice

case $browser_choice in
    1) BROWSER="chrome" ;;
    2) BROWSER="edge" ;;
    3) BROWSER="firefox" ;;
    4) BROWSER="safari" ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo "Extracting cookies from $BROWSER..."
echo ""

# Use a simple YouTube URL to trigger cookie extraction
yt-dlp --cookies-from-browser "$BROWSER" --cookies cookies.txt --skip-download "https://www.youtube.com/watch?v=jNQXAC9IVRw"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================"
    echo "  SUCCESS! Cookies exported to: cookies.txt"
    echo "================================================================"
    echo ""
    echo "Next steps:"
    echo "  1. Copy cookies.txt to your production server:"
    echo "     scp cookies.txt user@server:/path/to/project/"
    echo ""
    echo "  2. Add to production .env:"
    echo "     YOUTUBE_COOKIES_PATH=/app/cookies.txt"
    echo "     YOUTUBE_COOKIES_FILE=./cookies.txt"
    echo ""
    echo "  3. Rebuild container:"
    echo "     ./update_docker.sh"
    echo ""
else
    echo ""
    echo "================================================================"
    echo "[ERROR] Failed to export cookies!"
    echo "================================================================"
    echo ""
    echo "Common Solutions:"
    echo ""
    echo "1. CLOSE $BROWSER COMPLETELY (including background processes):"
    echo "   - Quit $BROWSER completely"
    echo "   - Check no $BROWSER processes are running"
    echo "   - Then run this script again"
    echo ""
    echo "2. USE BROWSER EXTENSION INSTEAD (easier):"
    echo "   - Install 'Get cookies.txt LOCALLY' extension"
    echo "   - Go to YouTube.com (logged in)"
    echo "   - Click extension icon > Export"
    echo "   - Save as cookies.txt in this folder"
    echo ""
    echo "Extension links:"
    echo "  Chrome:  https://chrome.google.com/webstore/detail/cclelndahbckbenkjhflpdbgdldlbecc"
    echo "  Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/"
    echo ""
    exit 1
fi

