"""Whitespace Synthesizer Agent - The Strategist"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

# WhitespaceSynthesizerAgent is model-only - no tools needed
# It performs strategic analysis and comparison

whitespace_synthesizer_agent = LlmAgent(
    name="WhitespaceSynthesizerAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "competitor_intelligence/sub_agents/whitespace_synthesizer/instruction.txt"
    ),
    description="Analyzes complete competitor landscape, compares to Wendy's offers, and identifies strategic whitespace opportunities.",
    tools=[],  # Model-only agent - no tools needed
)

