"""
The specialized agent for handling medical imaging analysis tasks.
"""
import logging
from agents.base_agent import create_agent
from imaging.ct_scan_tool import analyze_ct_scan
from imaging.mri_tool import analyze_mri
from imaging.pathology_tool import analyze_pathology_slide

logger = logging.getLogger(__name__)

def get_imaging_agent():
    """Factory function for the Imaging Agent."""
    
    instruction = """
    You are a specialized medical imaging assistant. Your role is to receive a request
    for an imaging study analysis and delegate it to the appropriate tool.
    - For CT scans, use the 'analyze_ct_scan' tool.
    - For MRIs, use the 'analyze_mri' tool.
    - For pathology slides, use the 'analyze_pathology_slide' tool.
    Return the JSON output from the tool directly. Do not add any commentary.
    """

    imaging_agent = create_agent(
        name="ImagingAnalysisAgent",
        description="An agent that analyzes medical imaging data like CT scans, MRIs, and pathology slides.",
        instruction=instruction,
        tools=[
            analyze_ct_scan,
            analyze_mri,
            analyze_pathology_slide,
        ],
    )
    logger.info("✅ Imaging Analysis Agent created.")
    return imaging_agent

