from typing import Any, Callable, Dict, Optional, Sequence

from ..core.action import ActionContext
from ..core.agent import Agent
from ..core.environment import Environment
from ..core.language import AgentFunctionCallingActionLanguage, AgentLanguage, Goal
from ..core.llm import generate_response
from ..core.memory import Memory
from .registry import PythonActionRegistry, register_tool


@register_tool(tags=["agents"])
def call_agent(
    action_context: ActionContext,
    agent_name: str,
    task: str,
) -> Dict[str, Any]:
    """Invoke another registered agent and return its output summary."""

    agent_registry = action_context.get("agent_registry")
    if not agent_registry:
        return {
            "success": False,
            "error": "No agent registry found in context",
        }

    agent_run = agent_registry.get_agent(agent_name)
    if not agent_run:
        available = agent_registry.list_agents()
        available_str = ", ".join(available) if available else "<none>"
        return {
            "success": False,
            "error": f"Agent '{agent_name}' not found. Available agents: {available_str}",
        }
#  This passes all the memory from the parent agent to the child agent
    # invoked_memory = action_context.get_memory() or Memory()
    invoked_memory = Memory()

    try:
        result_memory = agent_run(user_input=task, memory=invoked_memory)
    except Exception as exc:  # pragma: no cover - defensive guardrail
        return {
            "success": False,
            "agent": agent_name,
            "error": f"Agent execution failed: {exc}",
        }

    if not result_memory:
        return {
            "success": False,
            "agent": agent_name,
            "error": "Agent completed but returned no memory",
        }

    last_memory = result_memory.get_last_memory()
    if not last_memory:
        return {
            "success": False,
            "agent": agent_name,
            "error": "Agent completed but produced no results",
        }

    return {
        "success": True,
        "agent": agent_name,
        "result": last_memory.get("content", "No content"),
        "memory_items": len(result_memory.items),
    }