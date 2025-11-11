from typing import List, Dict, Any
from ..core.agent import Agent
from ..core.memory import Memory


class BaseOrchestrator:
    """Base class for multi-agent orchestration"""
    
    def __init__(self, agents: List[Agent]):
        self.agents = {agent.name: agent for agent in agents}
        self.shared_memory = Memory()

    def get_agent(self, name: str) -> Agent:
        """Get an agent by name"""
        return self.agents.get(name)

    def coordinate(self, user_input: str) -> str:
        """Coordinate agents to fulfill user request"""
        raise NotImplementedError("Subclasses must implement coordinate()")
