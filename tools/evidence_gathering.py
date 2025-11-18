"""
Tools for requesting medical tests and procedures.
"""
import logging
from google.adk.tools.tool_context import ToolContext
import json

logger = logging.getLogger(__name__)

def request_lab_test(test_name: str, reason: str, tool_context: ToolContext) -> dict:
    """
    Requests a laboratory test (e.g., CBC, lipid panel).
    This action requires confirmation from the supervising physician.

    Args:
        test_name: The name of the lab test to order.
        reason: The clinical justification for ordering the test.
        tool_context: The ADK tool context for requesting confirmation.

    Returns:
        A dictionary indicating the request is pending approval.
    """
    logger.info(f"Requesting lab test '{test_name}' for reason: {reason}")
    
    hint = f"Physician approval required: Order lab test '{test_name}'? Justification: {reason}"
    tool_context.request_confirmation(
        hint=hint,
        payload={"type": "lab_test_request", "test_name": test_name, "reason": reason}
    )
    
    return {
        "status": "pending_physician_approval",
        "test_name": test_name,
        "message": "Awaiting approval from the supervising physician to order the lab test."
    }

def request_imaging_study(study_type: str, body_part: str, reason: str) -> str:
    """
    A placeholder function that would format a request to an imaging agent/service.
    This tool does not directly interact with the imaging agent, but prepares the
    query for the DiagnosticAgent to delegate.
    
    Args:
        study_type: The type of imaging, e.g., 'CT Scan', 'MRI', 'X-ray'.
        body_part: The area to be imaged, e.g., 'Head', 'Chest', 'Abdomen'.
        reason: The clinical justification for the study.
        
    Returns:
        A JSON string representing the structured request for the imaging agent.
    """
    logger.info(f"Formatting request for {study_type} of the {body_part}.")
    request = {
        "study_type": study_type,
        "body_part": body_part,
        "reason": reason
    }
    return json.dumps(request)

