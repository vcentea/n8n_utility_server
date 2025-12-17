import os
import platform
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", "2277"))
API_KEY = os.getenv("API_KEY", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
TEMP_PATH = os.getenv("TEMP_PATH", "/tmp/pdf_service")
MAX_FILE_SIZE = 10 * 1024 * 1024

YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")


def find_poppler_path():
    """Auto-detect Poppler installation on Windows."""
    env_path = os.getenv("POPPLER_PATH", "").strip()
    if env_path:
        return env_path
    
    if platform.system() != "Windows":
        return None
    
    common_locations = [
        Path("C:/Program Files/poppler/Library/bin"),
        Path("C:/Program Files (x86)/poppler/Library/bin"),
        Path("C:/poppler/Library/bin"),
        Path("C:/poppler/bin"),
        Path.home() / "poppler/Library/bin",
        Path.home() / "poppler/bin",
    ]
    
    for location in common_locations:
        if location.exists() and (location / "pdftoppm.exe").exists():
            return str(location)
    
    return None


POPPLER_PATH = find_poppler_path()

