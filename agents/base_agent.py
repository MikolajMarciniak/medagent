"""
Base factory for creating LLM agents with common configurations.
"""
import logging
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from utils.config import get_retry_config, GEMINI_MODEL

logger = logging.getLogger(__name__)

def create_agent(name: str, description: str, instruction: str, tools: list = None, sub_agents: list = None):
    """
    Creates an LlmAgent with standardized settings.

    Args:
        name: The name of the agent.
        description: A brief description of the agent's purpose.
        instruction: The detailed system prompt for the agent.
        tools: A list of tools the agent can use.
        sub_agents: A list of sub-agents the agent can delegate to.

    Returns:
        An instance of LlmAgent.
    """
    logger.info(f"Creating agent: {name}")
    return LlmAgent(
        model=Gemini(model=GEMINI_MODEL, retry_options=get_retry_config()),
        name=name,
        description=description,
        instruction=instruction.strip(),
        tools=tools or [],
        sub_agents=sub_agents or [],
    )
