"""Memory broker for inter-agent communication and shared memory"""


class MemoryBroker:
    """Facilitates memory sharing between agents"""
    
    def __init__(self):
        self.shared_memories = {}
    
    def share_memory(self, agent_id: str, memory: dict):
        """Share a memory from an agent"""
        if agent_id not in self.shared_memories:
            self.shared_memories[agent_id] = []
        self.shared_memories[agent_id].append(memory)
    
    def get_shared_memories(self, agent_id: str = None) -> list:
        """Get shared memories, optionally filtered by agent"""
        if agent_id:
            return self.shared_memories.get(agent_id, [])
        
        all_memories = []
        for memories in self.shared_memories.values():
            all_memories.extend(memories)
        return all_memories
    
    def clear_agent_memories(self, agent_id: str):
        """Clear memories for a specific agent"""
        if agent_id in self.shared_memories:
            self.shared_memories[agent_id] = []
    
    def clear_all_memories(self):
        """Clear all shared memories"""
        self.shared_memories = {}
