"""
Agent responsible for performing in-depth research on a specific condition.
"""
import logging
from agents.base_agent import create_agent
from tools.medical_knowledge import search_medical_knowledge

logger = logging.getLogger(__name__)

def get_research_agent():
    """Factory function for the Research Agent."""

    instruction = """
    You are a medical research specialist. Your task is to conduct a deep dive into a
    specific medical condition provided to you.

    Workflow:
    1. Receive a specific medical condition as input.
    2. Use the 'search_medical_knowledge' tool multiple times to gather comprehensive information on:
        - Pathophysiology of the condition.
        - Common and rare symptoms.
        - Standard diagnostic procedures.
        - Current evidence-based treatment options and guidelines.
        - Prognosis.
    3. Synthesize this information into a clear, concise, and well-structured research summary.
    4. Your output should be a detailed report suitable for a medical professional.
    """

    research_agent = create_agent(
        name="ResearchAgent",
        description="Performs deep-dive research on a specific medical condition using the knowledge base.",
        instruction=instruction,
        tools=[search_medical_knowledge],
    )
    logger.info("✅ Research Agent created.")
    return research_agent

