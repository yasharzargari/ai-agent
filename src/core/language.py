import json
from typing import List, Dict, Any
from dataclasses import dataclass, field

from .action import Action
from .memory import Memory
from .environment import Environment


@dataclass(frozen=True)
class Goal:
    """Represents an agent's goal"""
    priority: int
    name: str
    description: str


@dataclass
class Prompt:
    """Container for LLM prompt components"""
    messages: List[Dict] = field(default_factory=list)
    tools: List[Dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class AgentLanguage:
    """Base class for agent communication protocols"""
    
    def construct_prompt(self,
                         actions: List[Action],
                         environment: Environment,
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        raise NotImplementedError("Subclasses must implement this method")

    def parse_response(self, response: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method")


class AgentFunctionCallingActionLanguage(AgentLanguage):
    """Function calling protocol for OpenAI-style APIs"""
    
    def format_goals(self, goals: List[Goal]) -> List:
        """Format goals as system messages"""
        sep = "\n-------------------\n"
        goal_instructions = "\n\n".join([
            f"{goal.name}:{sep}{goal.description}{sep}"
            for goal in goals
        ])
        return [{"role": "system", "content": goal_instructions}]

    def format_memory(self, memory: Memory) -> List:
        """Format memory items as conversation messages"""
        items = memory.get_memories()
        mapped_items = []
        
        for item in items:
            content = item.get("content", None)
            if not content:
                content = json.dumps(item, indent=4)

            if item["type"] == "assistant":
                mapped_items.append({"role": "assistant", "content": content})
            elif item["type"] == "environment":
                mapped_items.append({"role": "assistant", "content": content})
            else:
                mapped_items.append({"role": "user", "content": content})

        return mapped_items

    def format_actions(self, actions: List[Action]) -> List:
        """Format actions as OpenAI function tools"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description[:1024],
                    "parameters": action.parameters,
                },
            } for action in actions
        ]
        return tools

    def construct_prompt(self,
                         actions: List[Action],
                         environment: Environment,
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        """Construct complete prompt with goals, memory, and tools"""
        prompt = []
        prompt += self.format_goals(goals)
        prompt += self.format_memory(memory)
        tools = self.format_actions(actions)
        return Prompt(messages=prompt, tools=tools)

    def parse_response(self, response: str) -> dict:
        """Parse LLM response into structured format"""
        try:
            return json.loads(response)
        except Exception:
            return {
                "tool": "terminate",
                "args": {"message": response}
            }
