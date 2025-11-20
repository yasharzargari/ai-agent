import inspect
from typing import List, get_type_hints

from ..core.action import Action, ActionRegistry

# Global tool registries
tools = {}
tools_by_tag = {}


def get_tool_metadata(func, tool_name=None, description=None, 
                     parameters_override=None, terminal=False, tags=None):
    """Extract metadata from a function for tool registration"""
    tool_name = tool_name or func.__name__
    description = description or (
        func.__doc__.strip() if func.__doc__ else "No description provided."
    )

    if parameters_override is None:
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)

        args_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }

        for param_name, param in signature.parameters.items():
            if param_name in ["action_context", "action_agent"]:
                continue

            param_type = type_hints.get(param_name, str)
            param_schema = {"type": _get_json_type(param_type)}
            args_schema["properties"][param_name] = param_schema

            if param.default == inspect.Parameter.empty:
                args_schema["required"].append(param_name)
    else:
        args_schema = parameters_override

    return {
        "tool_name": tool_name,
        "description": description,
        "parameters": args_schema,
        "function": func,
        "terminal": terminal,
        "tags": tags or []
    }


def _get_json_type(param_type):
    """Convert Python type to JSON schema type"""
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object"
    }
    return type_map.get(param_type, "string")


def register_tool(tool_name=None, description=None, parameters_override=None, 
                 terminal=False, tags=None):
    """Decorator to register a function as a tool"""
    def decorator(func):
        metadata = get_tool_metadata(
            func=func,
            tool_name=tool_name,
            description=description,
            parameters_override=parameters_override,
            terminal=terminal,
            tags=tags
        )

        tools[metadata["tool_name"]] = {
            "description": metadata["description"],
            "parameters": metadata["parameters"],
            "function": metadata["function"],
            "terminal": metadata["terminal"],
            "tags": metadata["tags"]
        }

        for tag in metadata["tags"]:
            if tag not in tools_by_tag:
                tools_by_tag[tag] = []
            tools_by_tag[tag].append(metadata["tool_name"])

        return func
    return decorator


class PythonActionRegistry(ActionRegistry):
    """Action registry that loads from decorated functions"""
    
    def __init__(self, tags: List[str] = None, tool_names: List[str] = None):
        super().__init__()
        self.terminate_tool = None

        for tool_name, tool_desc in tools.items():
            if tool_name == "terminate":
                self.terminate_tool = tool_desc
                continue

            if tool_names and tool_name not in tool_names:
                continue

            tool_tags = tool_desc.get("tags", [])
            if tags and not any(tag in tool_tags for tag in tags):
                continue

            self.register(Action(
                name=tool_name,
                function=tool_desc["function"],
                description=tool_desc["description"],
                parameters=tool_desc.get("parameters", {}),
                terminal=tool_desc.get("terminal", False),
                accepts_action_context="action_context" in inspect.signature(tool_desc["function"]).parameters
            ))

    def register_terminate_tool(self):
        """Register the terminate tool"""
        if self.terminate_tool:
            self.register(Action(
                name="terminate",
                function=self.terminate_tool["function"],
                description=self.terminate_tool["description"],
                parameters=self.terminate_tool.get("parameters", {}),
                terminal=self.terminate_tool.get("terminal", False),
                accepts_action_context="action_context" in inspect.signature(self.terminate_tool["function"]).parameters
            ))
        else:
            raise Exception("Terminate tool not found in tool registry")
