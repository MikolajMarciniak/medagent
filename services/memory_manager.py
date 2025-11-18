"""
Manages long-term memory for the agents.
"""
import logging
from google.adk.memory import InMemoryMemoryService

logger = logging.getLogger(__name__)

class MemoryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Initializing MemoryManager.")
            cls._instance = super(MemoryManager, cls).__new__(cls)
            # For production, consider VertexAiMemoryBankService for intelligent consolidation
            # and persistent, semantic search capabilities.
            cls._instance.memory_service = InMemoryMemoryService()
            logger.info("✅ InMemoryMemoryService created for long-term memory.")
        return cls._instance

    def get_service(self):
        return self.memory_service

# Singleton instance
memory_manager = MemoryManager()

def get_memory_service():
    """Provides access to the memory service singleton."""
    return memory_manager.get_service()
