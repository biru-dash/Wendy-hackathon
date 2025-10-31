"""Offer Definition Agent - The Structurer"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

# OfferDefinitionAgent is model-only - no tools needed
# It structures raw concepts into defined offers

offer_definition_agent = LlmAgent(
    name="OfferDefinitionAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "offer_design/sub_agents/offer_definition/instruction.txt"
    ),
    description="Takes raw offer concepts and defines their full structure including mechanic, channel, duration, and target segment.",
    tools=[],  # Model-only agent - no tools needed
)

