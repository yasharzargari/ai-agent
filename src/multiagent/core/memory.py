from typing import List, Dict, Optional


class Memory:
    """Manages agent memory and conversation history"""
    
    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        """Add a memory item"""
        self.items.append(memory)

    def get_memories(self, limit: int = None) -> List[Dict]:
        """Get memory items, optionally limited"""
        if limit:
            return self.items[-limit:]
        return self.items

    def copy_without_system_memories(self):
        """Return a copy without system memories"""
        filtered_items = [m for m in self.items if m.get("type") != "system"]
        memory = Memory()
        memory.items = filtered_items
        return memory

    def clear(self):
        """Clear all memory"""
        self.items = []

    def get_last_memory(self) -> Optional[Dict]:
        """Get the most recent memory item"""
        return self.items[-1] if self.items else None
