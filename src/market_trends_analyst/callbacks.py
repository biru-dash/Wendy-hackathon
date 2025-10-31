"""Callbacks for state management in Market Trends Analyst root agent"""
from typing import Any
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

def before_agent_run(callback_context: Any) -> None:
    """
    Callback executed before each agent turn.
    Initializes or updates the session state to guide the root agent's workflow.
    
    Args:
        callback_context: ADK callback context with .state attribute (dict-like)
    """
    # Access session_state from callback_context.state
    # The CallbackContext object has a .state attribute that behaves like a dictionary
    session_state = callback_context.state
    
    # Initialize stage if not present
    if "stage" not in session_state:
        session_state["stage"] = "initialized"
    
    # Initialize workflow tracking
    if "workflow_state" not in session_state:
        session_state["workflow_state"] = {
            "data_collected": False,
            "research_completed": False,
            "data_collection_results": None,
        }


def after_tool_run(
    tool_context: ToolContext, 
    tool_response: dict, 
    tool: BaseTool,
    **kwargs
) -> dict:
    """
    Callback executed after any tool completes its run.
    Processes tool output and updates session state to guide next decisions.
    
    Args:
        tool_context: ADK tool context containing session state
        tool_response: Dictionary containing the tool's response/output
        tool: The Tool object that was executed
        **kwargs: Catches any additional arguments for future compatibility
    
    Returns:
        The (unmodified or modified) tool_response dictionary
    """
    # Access session_state from tool_context.state
    session_state = tool_context.state
    
    # Get tool name from the tool object
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    
    # Use tool_response as the tool output
    tool_output = tool_response
    
    workflow_state = session_state.setdefault("workflow_state", {})
    
    # Update state based on which tool was executed
    if "DataCollectionAgent" in tool_name or tool_name == "data_collection_tool":
        workflow_state["data_collected"] = True
        workflow_state["data_collection_results"] = tool_output
        session_state["stage"] = "data_collection_complete"
        
    elif "ResearchAndSynthesisAgent" in tool_name or tool_name == "research_synthesis_tool":
        workflow_state["research_completed"] = True
        session_state["stage"] = "research_complete"
        
    # Log the workflow progress
    session_state["last_tool"] = tool_name
    session_state["last_tool_output"] = str(tool_output)[:500]  # Truncate for storage
    
    # Return the tool_response (can be modified or unmodified)
    return tool_response
