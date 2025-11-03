from ...core.agent import Agent
from ...core.language import AgentFunctionCallingActionLanguage
from ...core.environment import Environment
from ...core.llm import generate_response
from ...tools.registry import PythonActionRegistry, register_tool
from .goals import ORCHESTRATOR_GOALS


@register_tool(tags=["orchestrator"], terminal=False)
def dispatch_retrieval_tasks(tasks: str) -> str:
    """
    Dispatch retrieval tasks to the Retrieval Worker.
    
    Args:
        tasks: JSON string describing retrieval tasks to perform
    """
    return f"Dispatched retrieval tasks: {tasks}"


@register_tool(tags=["orchestrator"], terminal=False)
def request_synthesis(data_summary: str) -> str:
    """
    Request the Synthesizer to consolidate and format results.
    
    Args:
        data_summary: Summary of retrieved data to synthesize
    """
    return f"Synthesis requested for: {data_summary}"


@register_tool(tags=["orchestrator"], terminal=True)
def complete_orchestration(final_result: str) -> str:
    """
    Complete orchestration and return final result.
    
    Args:
        final_result: The final synthesized result to return to user
    """
    return f"Orchestration complete: {final_result}"


def create_orchestrator_agent():
    """Factory function to create an Orchestrator agent"""
    action_registry = PythonActionRegistry(tags=["orchestrator"])
    
    return Agent(
        name="Orchestrator",
        goals=ORCHESTRATOR_GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
