"""
A critical tool for ensuring agent outputs are safe and responsible.
"""
import logging
import json

logger = logging.getLogger(__name__)

# This could be a separate, highly-constrained LLM call in a real system.
def perform_safety_check(proposed_diagnosis: str, action_plan: str) -> str:
    """
    Reviews a proposed diagnosis and action plan for potential risks, biases,
    and ethical concerns. It is a mandatory final step before presenting
    information to the user.

    Args:
        proposed_diagnosis: The final diagnosis suggested by the agent system.
        action_plan: The recommended next steps or treatments.

    Returns:
        A JSON string containing the safety review results.
    """
    logger.warning(f"PERFORMING SAFETY CHECK on Diagnosis: '{proposed_diagnosis}'")
    
    # Mock safety logic. A real system would have a robust, multi-layered check.
    issues = []
    if "definitely" in proposed_diagnosis.lower() or "certainly" in proposed_diagnosis.lower():
        issues.append({
            "level": "critical",
            "concern": "Overly confident language",
            "suggestion": "Rephrase diagnosis to be probabilistic and suggestive, not definitive. Always state that this is not a substitute for professional medical advice."
        })

    if not "consult a qualified physician" in action_plan.lower():
         issues.append({
            "level": "critical",
            "concern": "Missing disclaimer",
            "suggestion": "The action plan MUST include a clear and prominent recommendation to consult a qualified human physician."
        })

    if not issues:
        return json.dumps({
            "status": "passed",
            "message": "The proposed plan passes the initial safety check. Ready for physician review."
        })
    else:
        return json.dumps({
            "status": "failed",
            "issues": issues,
            "message": "The proposed plan has critical safety issues that must be addressed before proceeding."
        })

