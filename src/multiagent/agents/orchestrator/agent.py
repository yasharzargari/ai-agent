from ...core.agent import Agent
from ...core.language import AgentFunctionCallingActionLanguage
from ...core.environment import Environment
from ...core.llm import generate_response
from ...tools.registry import PythonActionRegistry
from . import actions as orchestrator_actions
from .goals import ORCHESTRATOR_GOALS



def create_orchestrator_agent():
    """Factory function to create an Orchestrator agent"""
    _ = orchestrator_actions  # Ensure tool decorators execute before registry creation
    action_registry = PythonActionRegistry(tags=["orchestrator", "system", "orchestrator_delegation"])
    action_registry.register_terminate_tool()
    
    return Agent(
        name="Orchestrator",
        goals=ORCHESTRATOR_GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
