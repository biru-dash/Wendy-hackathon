"""Simplified Offer Design Agent - Single LlmAgent"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

# SimplifiedOfferDesignAgent is a single LlmAgent that performs all design steps at once
# This replaces the multi-step pipeline (ConceptGeneration → Definition → Rationale → Prioritization)
# with a single agent that does everything in one pass

simplified_offer_design_agent = LlmAgent(
    name="SimplifiedOfferDesignAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "offer_design/sub_agents/simplified_offer_design/instruction.txt"
    ),
    description="Simplified offer design agent that generates, structures, rationalizes, and prioritizes offer concepts in a single step.",
    tools=[],  # Model-only agent - no tools needed
)

