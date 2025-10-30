from core.goal import Goal
from core.agent import Agent
from core.agent_language import AgentFunctionCallingActionLanguage
from actions.tool_actions import PythonActionRegistry
from llm.litellm_provider import generate_response
from environment.base_env import Environment
from goals.file_management import get_file_management_goals


def create_file_manager_agent():
    """Create a file management agent."""
    return Agent(
        goals=get_file_management_goals(),
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
        generate_response=generate_response,
        environment=Environment()
    )