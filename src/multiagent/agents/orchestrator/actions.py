
import json

from ...tools.registry import register_tool
from ...core.action import ActionContext
from ...tools.agent_tools import call_agent


@register_tool(tags=["orchestrator"])
def synthesize_results(action_context: ActionContext, web_results: str, file_results: str) -> str:
    """
    Synthesize information from multiple sources.
    
    Args:
        web_results: Results from web search agent
        file_results: Results from file management agent
        
    Returns:
        JSON with synthesized information
    """
    result = {
        "web_information": web_results,
        "file_information": file_results,
        "synthesis": "Use both sources to provide a comprehensive answer",
        "status": "ready_for_final_answer"
    }
    return json.dumps(result)


@register_tool(tags=["orchestrator_delegation"])
def run_retrieval_worker_agent(
    action_context: ActionContext,
    task: str,
) -> str:
    """Delegate a task to the RetrievalWorker agent and return its response."""
    result = call_agent(
        action_context=action_context,
        agent_name="RetrievalWorker",
        task=task,
    )
    return json.dumps(result)


@register_tool(tags=["orchestrator_delegation"])
def run_file_management_agent(
    action_context: ActionContext,
    task: str,
) -> str:
    """Delegate a task to the FileManagementAgent and return its response."""
    result = call_agent(
        action_context=action_context,
        agent_name="FileManagementAgent",
        task=task,
    )
    return json.dumps(result)


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """
    Terminates the orchestrator's execution with a final synthesized answer.
    
    Args:
        message: The final comprehensive answer
        
    Returns:
        The message with a termination note
    """
    return f"{message}\n\n[Orchestrator completed]"