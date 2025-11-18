"""
Configuration loader for the application.
"""
import os
from dotenv import load_dotenv
from google.genai import types

# Load environment variables from .env file
load_dotenv()

def get_google_api_key():
    """Retrieves the Google API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Please set it in your .env file or environment."
        )
    return api_key

def get_retry_config():
    """Returns a standard retry configuration for Gemini API calls."""
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )

# Constants
GEMINI_MODEL = "gemini-1.5-flash-latest"
APP_NAME = "MedicalDiagnosticsApp"
USER_ID = "physician_user"
DATABASE_URL = "sqlite:///medical_sessions.db"
IMAGING_AGENT_URL = "http://localhost:8001"

print("✅ Configuration loaded.")
