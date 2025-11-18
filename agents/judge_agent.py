"""
Agent responsible for evaluating hypotheses and planning the next steps.
"""
import logging
from agents.base_agent import create_agent
from tools.medical_knowledge import search_medical_knowledge

logger = logging.getLogger(__name__)

def get_judge_agent():
    """Factory function for the Judge Agent."""

    instruction = """
    You are a clinical reasoning evaluator. Your role is to act as a judge, critically
    assessing a list of diagnostic hypotheses against the available evidence.

    Workflow:
    1. Receive the list of hypotheses and all collated evidence (symptoms, lab results, imaging reports).
    2. For each hypothesis, evaluate its plausibility. Rank the hypotheses from most likely to least likely.
    3. Identify critical missing information.
    4. Create a strategic plan for the next steps. This plan should specify which clarifying questions to ask, lab tests to order, or imaging studies to request in order to differentiate between the leading hypotheses.
    5. Determine if the available information is sufficient to reach a conclusive diagnosis. If so, declare it.
    6. Your output should be a structured JSON object with keys: 'ranked_hypotheses', 'next_step_plan', and 'is_conclusive'.
    """

    judge_agent = create_agent(
        name="JudgeAgent",
        description="Evaluates diagnostic hypotheses, ranks their plausibility, and determines the next best action for evidence gathering.",
        instruction=instruction,
        tools=[search_medical_knowledge], # Judge might need to do its own quick lookups
    )
    logger.info("✅ Judge Agent created.")
    return judge_agent
