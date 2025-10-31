"""Insight Synthesizer Agent - Single-Step Synthesis"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

# InsightSynthesizerAgent is model-only - no tools needed
# It combines quantitative behavioral metrics and qualitative sentiment analysis
# into structured customer insights profiles

insight_synthesizer_agent = LlmAgent(
    name="InsightSynthesizerAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "customer_insights/sub_agents/insight_synthesizer/instruction.txt"
    ),
    description="Synthesizes behavioral metrics and sentiment analysis into structured customer insights profiles with segments, preferences, and key messaging.",
    tools=[],  # Model-only agent - no tools needed
)

