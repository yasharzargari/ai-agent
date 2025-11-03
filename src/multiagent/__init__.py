"""
Multiagent Chatbot System

A flexible framework for building multiagent systems with specialized roles
based on the GAME (Goals-Actions-Memory-Environment) loop.
"""

__version__ = "0.1.0"

from .core.agent import Agent
from .core.action import Action, ActionRegistry
from .core.memory import Memory
from .core.environment import Environment
from .core.language import Goal, Prompt, AgentLanguage, AgentFunctionCallingActionLanguage

__all__ = [
    "Agent",
    "Action",
    "ActionRegistry",
    "Memory",
    "Environment",
    "Goal",
    "Prompt",
    "AgentLanguage",
    "AgentFunctionCallingActionLanguage",
]
