"""
Tools for interactive symptom gathering from the patient/user.
"""
import logging
from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)

def ask_clarifying_question(question_to_user: str, tool_context: ToolContext) -> dict:
    """
    Asks the user a clarifying question and pauses the workflow to wait for their answer.
    This simulates a human-in-the-loop interaction for gathering more evidence.

    Args:
        question_to_user: The specific question to ask the user.
        tool_context: The ADK tool context to request confirmation.

    Returns:
        A dictionary indicating that the workflow is pending user input.
    """
    logger.info(f"Pausing to ask user: '{question_to_user}'")
    
    # Use request_confirmation to pause the agent execution and wait for external input.
    # The 'hint' is what the user-facing application will display.
    tool_context.request_confirmation(
        hint=question_to_user,
        payload={"type": "clarification_request"}
    )
    
    return {
        "status": "pending_user_input",
        "question_asked": question_to_user,
        "message": "Waiting for the user to provide more information."
    }

