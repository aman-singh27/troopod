import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_FALLBACK_MODELS = [
	model.strip()
	for model in os.getenv("GEMINI_FALLBACK_MODELS", "gemini-flash-latest,gemini-2.0-flash").split(",")
	if model.strip()
]
SCREENSHOTONE_API_KEY = os.getenv("SCREENSHOTONE_API_KEY", "")
MICROLINK_API_KEY = os.getenv("MICROLINK_API_KEY", "")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
MAX_HTML_SIZE_KB = int(os.getenv("MAX_HTML_SIZE_KB", "500"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

# Note: GEMINI_API_KEY will be validated at API call time, not at startup
# This allows the app to start even without the key (useful for development/testing)
