"""Competitor Analysis Agent - The Specialist"""
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search
from utils.instruction_loader import load_instruction_from_file
import os

def get_competitor_analysis_tools():
    """Get tools for CompetitorAnalysisAgent"""
    tools = [google_search]
    
    # Add web scraper tool when available
    # from .tools import web_scraper_tool
    # tools.append(web_scraper_tool)
    
    return tools

competitor_analysis_agent = LlmAgent(
    name="CompetitorAnalysisAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "competitor_intelligence/sub_agents/competitor_analysis/instruction.txt"
    ),
    description="Researches a single competitor's promotions, loyalty programs, and offers to build a structured profile.",
    tools=get_competitor_analysis_tools(),
)

