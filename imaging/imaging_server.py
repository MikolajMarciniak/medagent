"""
A2A server to expose the Imaging Agent as a microservice.
"""
import logging
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from imaging.imaging_agent import get_imaging_agent
from utils.config import IMAGING_AGENT_URL

logger = logging.getLogger(__name__)

def create_imaging_app():
    """Creates the A2A-compatible FastAPI application for the imaging agent."""
    imaging_agent = get_imaging_agent()
    port = int(IMAGING_AGENT_URL.split(":")[-1])
    
    logger.info(f"Wrapping Imaging Agent in an A2A server to run on port {port}.")
    
    # to_a2a wraps the ADK agent in a FastAPI application, handling the A2A protocol.
    app = to_a2a(imaging_agent, port=port)
    
    logger.info("✅ A2A server app created.")
    logger.info(f"   Agent card will be at: {IMAGING_AGENT_URL}/.well-known/agent-card.json")
    return app

# This allows running the server with `uvicorn imaging.imaging_server:app`
app = create_imaging_app()

