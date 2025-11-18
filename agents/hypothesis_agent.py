"""
Agent responsible for generating a differential diagnosis.
"""
import logging
from agents.base_agent import create_agent
from tools.medical_knowledge import search_medical_knowledge

logger = logging.getLogger(__name__)

def get_hypothesis_agent():
    """Factory function for the Hypothesis Agent."""

    instruction = """
    You are a medical hypothesis generation agent. Your task is to develop a differential
    diagnosis based on a given set of symptoms and patient information.
    
    Workflow:
    1. Receive the initial symptoms.
    2. Use the 'search_medical_knowledge' tool to research potential causes related to the primary symptoms.
    3. Synthesize the research into a list of 3-5 plausible medical conditions.
    4. For each condition, provide a brief rationale explaining why it fits the current evidence.
    5. Present the output as a structured list of potential diagnoses. Do not make a final conclusion.
    """

    hypothesis_agent = create_agent(
        name="HypothesisAgent",
        description="Generates a list of possible medical conditions (differential diagnosis) based on initial symptoms.",
        instruction=instruction,
        tools=[search_medical_knowledge],
    )
    logger.info("✅ Hypothesis Agent created.")
    return hypothesis_agent

