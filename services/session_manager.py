"""
Manages persistent session storage for conversations.
"""
import logging
from google.adk.sessions import DatabaseSessionService
from utils.config import DATABASE_URL

logger = logging.getLogger(__name__)

class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info(f"Initializing SessionManager with DB: {DATABASE_URL}")
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.session_service = DatabaseSessionService(db_url=DATABASE_URL)
            logger.info("✅ DatabaseSessionService created for persistent sessions.")
        return cls._instance

    def get_service(self):
        return self.session_service

# Singleton instance
session_manager = SessionManager()

def get_session_service():
    """Provides access to the session service singleton."""
    return session_manager.get_service()
