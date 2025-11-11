import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", "8080"))
API_KEY = os.getenv("API_KEY", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
TEMP_PATH = os.getenv("TEMP_PATH", "/tmp/pdf_service")
MAX_FILE_SIZE = 10 * 1024 * 1024

