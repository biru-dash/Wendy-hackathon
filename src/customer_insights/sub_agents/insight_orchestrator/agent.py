"""Insight Orchestrator Agent - Team Lead (ParallelAgent)"""
from google.adk.agents.parallel_agent import ParallelAgent
from utils.instruction_loader import load_instruction_from_file
from ..behavioral_analysis.agent import behavioral_analysis_agent
from ..sentiment_analysis.agent import sentiment_analysis_agent
import os

insight_orchestrator_agent = ParallelAgent(
    name="InsightOrchestratorAgent",
    sub_agents=[
        behavioral_analysis_agent,
        sentiment_analysis_agent,
    ],
    description="Coordinates parallel execution of BehavioralAnalysisAgent and SentimentAnalysisAgent to analyze customer data simultaneously.",
)
