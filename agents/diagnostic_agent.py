"""
The main orchestrator agent for the medical diagnostic workflow.
"""
import logging
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from agents.base_agent import create_agent
from agents.hypothesis_agent import get_hypothesis_agent
from agents.judge_agent import get_judge_agent
from agents.research_agent import get_research_agent
from tools.patient_symptoms import ask_clarifying_question
from tools.evidence_gathering import request_lab_test, request_imaging_study
from tools.safety_check import perform_safety_check
from utils.config import IMAGING_AGENT_URL

logger = logging.getLogger(__name__)

def get_diagnostic_agent():
    """Factory function for the main Diagnostic Agent."""
    
    # Create the client-side proxy to communicate with the remote imaging agent service.
    try:
        remote_imaging_agent = RemoteA2aAgent(
            name="ImagingAnalysisAgent",
            description="Remote agent for analyzing medical images (CT, MRI, etc.). Use this to interpret imaging study requests.",
            agent_card=f"{IMAGING_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
        )
        logger.info(f"✅ Remote A2A proxy for Imaging Agent created, pointing to {IMAGING_AGENT_URL}.")
    except Exception as e:
        logger.error(f"Failed to create RemoteA2aAgent. Is the imaging server running? Error: {e}")
        logger.error("Proceeding without imaging capabilities.")
        remote_imaging_agent = None

    instruction = """
    You are the lead coordinating agent for a medical diagnostic process. Your goal is to systematically
    work through a patient's case to arrive at a well-researched, safe, and plausible diagnostic suggestion.

    You must follow this workflow strictly:
    1.  **GATHER INITIAL INFO**: Start by interacting with the user to understand their primary symptoms. Use the 'ask_clarifying_question' tool if more detail is needed.
    2.  **FORMULATE HYPOTHESES**: Once you have initial symptoms, delegate to the 'HypothesisAgent' to generate a differential diagnosis.
    3.  **EVALUATE & PLAN**: Pass the list of hypotheses and all current evidence to the 'JudgeAgent'. The JudgeAgent will rank the hypotheses and create a plan for the next steps.
    4.  **GATHER MORE EVIDENCE**: Execute the plan from the JudgeAgent. This may involve:
        - Using 'ask_clarifying_question' to get more symptom details from the user.
        - Using 'request_lab_test' to order blood work.
        - Using 'request_imaging_study' to format a request, then delegating that request to the 'ImagingAnalysisAgent'.
    5.  **ITERATE**: Repeat steps 3 and 4, accumulating evidence until the 'JudgeAgent' determines the information is conclusive.
    6.  **DEEP RESEARCH**: Once the diagnosis is considered conclusive, delegate the final condition to the 'ResearchAgent' for an in-depth summary.
    7.  **FINAL SAFETY CHECK**: Before presenting the final report, you MUST use the 'perform_safety_check' tool on the proposed diagnosis and action plan from the research summary.
    8.  **PRESENT REPORT**: If the safety check passes, present the comprehensive report to the user. If it fails, state that a safe conclusion could not be reached and that a physician must be consulted.

    Always prioritize patient safety and adhere to a structured, evidence-based approach.
    """

    sub_agents = [
        get_hypothesis_agent(),
        get_judge_agent(),
        get_research_agent(),
    ]
    if remote_imaging_agent:
        sub_agents.append(remote_imaging_agent)

    diagnostic_agent = create_agent(
        name="DiagnosticOrchestratorAgent",
        description="The main agent that manages the entire diagnostic workflow from symptom intake to final report.",
        instruction=instruction,
        tools=[
            ask_clarifying_question,
            request_lab_test,
            request_imaging_study,
            perform_safety_check,
        ],
        sub_agents=sub_agents,
    )
    logger.info("✅ Diagnostic Orchestrator Agent created.")
    return diagnostic_agent

