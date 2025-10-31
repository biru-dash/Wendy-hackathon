"""Research Orchestrator Agent - The Team Lead (Parallel Orchestrator)"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
from competitor_intelligence.tools.agent_tools import competitor_analysis_tool
import os

research_orchestrator_agent = LlmAgent(
    name="ResearchOrchestratorAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "competitor_intelligence/sub_agents/research_orchestrator/instruction.txt"
    ),
    description="Manages parallel research of all identified competitors by orchestrating multiple CompetitorAnalysisAgent calls.",
    tools=[competitor_analysis_tool],  # AgentTool to call CompetitorAnalysisAgent
)

