from ...core.agent import Agent
from ...core.language import AgentFunctionCallingActionLanguage
from ...core.environment import Environment
from ...core.llm import generate_response
from ...tools.registry import PythonActionRegistry
from . import action as retrieval_actions
from .goals import RETRIEVAL_WORKER_GOALS

def create_retrieval_worker_agent():
    """Factory function to create a Retrieval Worker agent"""
    # Include both retrieval and file operation tools
    _ = retrieval_actions  # Ensure tool decorators execute before registry creation
    action_registry = PythonActionRegistry(tags=["web_operations", "system"])
    action_registry.register_terminate_tool()

    return Agent(
        name="RetrievalWorker",
        goals=RETRIEVAL_WORKER_GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
