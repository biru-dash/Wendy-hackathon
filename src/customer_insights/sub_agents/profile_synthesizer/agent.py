"""Profile Synthesizer Agent - Strategist"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

def get_synthesizer_tools():
    """Get tools for ProfileSynthesizerAgent"""
    # save_customer_segments_tool requires BigQuery write access
    # Commented out for hackathon (participants have read-only access)
    # from .tools import save_customer_segments_tool
    # return [save_customer_segments_tool]
    return []  # No tools needed - agent only synthesizes data

profile_synthesizer_agent = LlmAgent(
    name="ProfileSynthesizerAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "customer_insights/sub_agents/profile_synthesizer/instruction.txt"
    ),
    description="Synthesizes quantitative behavioral data and qualitative sentiment data into actionable customer insight profiles.",
    tools=get_synthesizer_tools(),  # Can save results to BigQuery
)
