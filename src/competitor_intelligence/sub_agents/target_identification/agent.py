"""Target Identification Agent - The Scout"""
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search
from utils.instruction_loader import load_instruction_from_file
import os

def get_target_identification_tools():
    """Get tools for TargetIdentificationAgent"""
    return [google_search]

target_identification_agent = LlmAgent(
    name="TargetIdentificationAgent",
    model=os.getenv("GEN_FAST_MODEL", "gemini-2.5-flash"),
    instruction=load_instruction_from_file(
        "competitor_intelligence/sub_agents/target_identification/instruction.txt"
    ),
    description="Identifies competitors and their digital assets to be analyzed for competitive intelligence.",
    tools=get_target_identification_tools(),
)

