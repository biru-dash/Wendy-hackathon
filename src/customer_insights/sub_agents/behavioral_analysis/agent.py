"""Behavioral Analysis Agent - Quant Specialist"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

def get_behavioral_tools():
    """Get tools for BehavioralAnalysisAgent"""
    # Import the wrapped FunctionTool instance
    # Participants can add more tools during hackathon
    from .tools import crm_database_tool
    return [crm_database_tool]

behavioral_analysis_agent = LlmAgent(
    name="BehavioralAnalysisAgent",
    model=os.getenv("GEN_FAST_MODEL", "gemini-2.5-flash"),
    instruction=load_instruction_from_file(
        "customer_insights/sub_agents/behavioral_analysis/instruction.txt"
    ),
    description="Analyzes quantitative behavioral data including redemption patterns, segment identification, and lift metrics.",
    tools=get_behavioral_tools(),
)
