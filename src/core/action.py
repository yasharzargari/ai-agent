from typing import Callable, Dict, Any, List
import uuid


class Action:
    """Represents an executable action with metadata"""
    
    def __init__(self,
                 name: str,
                 function: Callable,
                 description: str,
                 parameters: Dict,
                 terminal: bool = False,
                 accepts_action_context: bool = False):
        self.name = name
        self.function = function
        self.description = description
        self.terminal = terminal
        self.parameters = parameters
        self.accepts_action_context = accepts_action_context

    def execute(self, action_context=None, **args) -> Any:
        """Execute the action's function"""
        if self.accepts_action_context:
            return self.function(action_context=action_context, **args)
        return self.function(**args)


class ActionRegistry:
    """Registry for managing available actions"""
    
    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        """Register a new action"""
        self.actions[action.name] = action

    def get_action(self, name: str) -> Action:
        """Get an action by name"""
        return self.actions.get(name, None)

    def get_actions(self) -> List[Action]:
        """Get all registered actions"""
        return list(self.actions.values())

    def get_action_names(self) -> List[str]:
        """Get names of all registered actions"""
        return list(self.actions.keys())

class ActionContext:
    def __init__(self, properties: Dict=None):
        self.context_id = str(uuid.uuid4())
        self.properties = properties or {}

    def get(self, key: str, default=None):
        return self.properties.get(key, default)

    def get_memory(self):
        return self.properties.get("memory", None)

    def get_agent_registry(self):
        return self.properties.get("agent_registry", None)