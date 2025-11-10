"""
This module defines the root agent for the entire multi-agent system.
It uses a SequentialAgent architecture, which means it runs a series of sub-agents
one after another, passing the combined results from one step to the next.

This sequential process ensures a logical workflow:
1. Research is conducted.
2. Insights are gathered.
3. Offers are designed based on the collected information.
"""
import sys
from pathlib import Path

# Add project root and src to Python path so we can import from src
project_root = Path(__file__).parent.parent.parent
src_dir = project_root / "src"
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Load environment variables from .env file (must be imported early)
from src.utils.env_loader import load_env
load_env()

from google.adk.agents.sequential_agent import SequentialAgent

# Import the primary agent from each specialized team.
# These are the entry points for the Market Trends, Customer Insights,
# Competitor Intelligence, and Offer Design teams.
from src.market_trends_analyst.agent import market_trends_analyst_root_agent
from src.customer_insights.agent import customer_insights_manager_agent
from src.competitor_intelligence.agent import competitor_intel_manager_agent
from src.offer_design.sub_agents.simplified_offer_design.agent import (
    simplified_offer_design_agent,
)

# This is the main SequentialAgent that orchestrates the entire workflow.
# You can modify the workflow by changing the order of the agents in the `sub_agents`
# list or by adding/removing agents.
marketing_orchestrator_agent = SequentialAgent(
    name="MarketingOrchestratorAgent",
    sub_agents=[
        market_trends_analyst_root_agent,
        customer_insights_manager_agent,
        competitor_intel_manager_agent,
        simplified_offer_design_agent,
    ],
    description=(
        "A root agent that manages the end-to-end process of marketing"
        " intelligence and offer design. It starts with a high-level research"
        " goal and concludes with concrete, prioritized offer concepts."
    ),
)

# The `root_agent` is the entry point that the ADK server will run.
# For this application, the orchestrator is the root.
root_agent = marketing_orchestrator_agent

