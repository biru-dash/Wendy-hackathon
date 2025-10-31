"""Concept Generation Agent - The Creative Brainstormer"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

# ConceptGenerationAgent is model-only - no tools needed
# It generates raw creative ideas from input signals

concept_generation_agent = LlmAgent(
    name="ConceptGenerationAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "offer_design/sub_agents/concept_generation/instruction.txt"
    ),
    description="Generates a wide list of raw offer concept ideas by combining market trends, customer insights, and competitor whitespace opportunities.",
    tools=[],  # Model-only agent - no tools needed
)

