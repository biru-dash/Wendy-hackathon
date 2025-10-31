"""Sentiment Analysis Agent - Qual Specialist"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

def get_sentiment_tools():
    """Get tools for SentimentAnalysisAgent"""
    from .tools import feedback_database_tool
    return [feedback_database_tool]

sentiment_analysis_agent = LlmAgent(
    name="SentimentAnalysisAgent",
    model=os.getenv("GEN_FAST_MODEL", "gemini-2.5-flash"),
    instruction=load_instruction_from_file(
        "customer_insights/sub_agents/sentiment_analysis/instruction.txt"
    ),
    description="Analyzes qualitative sentiment data including feedback, reviews, and messaging cues.",
    tools=get_sentiment_tools(),
)
