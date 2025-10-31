"""Data Collection Agent - The Hunter"""
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search
from utils.instruction_loader import load_instruction_from_file
import os

# Note: google_trends_api_tool would need to be implemented as a custom tool
# For now, we'll structure it to accept it when available
# You can create a placeholder tool using the Tool decorator from google.adk.tools

def get_tools():
    """Get tools for DataCollectionAgent"""
    tools = [google_search]
    
    # If google_trends_api_tool is available, add it here
    # from .tools import google_trends_api_tool
    # tools.append(google_trends_api_tool)
    
    return tools

data_collection_agent = LlmAgent(
    name="DataCollectionAgent",
    model=os.getenv("GEN_FAST_MODEL", "gemini-2.5-flash"),
    instruction=load_instruction_from_file(
        "market_trends_analyst/sub_agents/data_collection/instruction.txt"
    ),
    description="Fetches raw data points including URLs from Google Search and quantitative trend data. Does not analyze content.",
    tools=get_tools(),
)
