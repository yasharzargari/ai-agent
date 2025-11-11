from typing import Callable, Dict, Optional
from dataclasses import dataclass

@dataclass
class RegisteredAgent:
    """Information about a registered agent."""
    name: str
    run_function: Callable
    description: str

class AgentRegistry:
    """Registry for managing and accessing agents."""
    
    def __init__(self):
        self._agents: Dict[str, RegisteredAgent] = {}
    
    def register_agent(
        self, 
        name: str, 
        run_function: Callable,
        description: str = ""
    ) -> None:
        """
        Register an agent's run function.
        
        Args:
            name: Unique name for the agent
            run_function: The agent's run function
            description: Description of what the agent does
        """
        if name in self._agents:
            raise ValueError(f"Agent '{name}' is already registered")
            
        self._agents[name] = RegisteredAgent(
            name=name,
            run_function=run_function,
            description=description
        )
        print(f"✓ Registered agent: {name}")
    
    def get_agent(self, name: str) -> Optional[Callable]:
        """Get an agent's run function by name."""
        agent = self._agents.get(name)
        return agent.run_function if agent else None
    
    def get_agent_info(self, name: str) -> Optional[RegisteredAgent]:
        """Get full information about an agent."""
        return self._agents.get(name)
    
    def list_agents(self) -> list[str]:
        """List all registered agent names."""
        return list(self._agents.keys())
    
    def get_agents_description(self) -> str:
        """Get a formatted description of all available agents."""
        if not self._agents:
            return "No agents registered."
        
        descriptions = []
        for name, agent in self._agents.items():
            desc = agent.description or "No description"
            descriptions.append(f"- {name}: {desc}")
        
        return "Available agents:\n" + "\n".join(descriptions)