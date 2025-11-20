import time
import traceback
from typing import Any

from .action import Action


class Environment:
    """Manages action execution and result formatting"""

    def execute_action(self, action: Action, args: dict, action_context=None) -> dict:
        """Execute an action and return formatted result"""
        try:
            result = action.execute(action_context=action_context, **args)
            return self.format_result(result)
        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def format_result(self, result: Any) -> dict:
        """Format result with metadata"""
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }
