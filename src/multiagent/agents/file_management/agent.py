"""File Management Agent implementation"""

from ...core.agent import Agent
from ...core.language import AgentFunctionCallingActionLanguage
from ...core.environment import Environment
from ...core.llm import generate_response
from ...tools.registry import PythonActionRegistry
from .goals import FILE_MANAGEMENT_GOALS

# Import actions to register them
from . import actions

def create_file_management_agent():
    """Factory function to create a File Management agent"""
    # Create action registry with file operations and system tools
    action_registry = PythonActionRegistry(tags=["file_operations", "system"])
    # Register the terminate tool (it's handled specially by PythonActionRegistry)
    action_registry.register_terminate_tool()
    
    return Agent(
        name="FileManagementAgent",
        goals=FILE_MANAGEMENT_GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
