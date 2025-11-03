"""Base classes for memory systems"""

from typing import List, Dict, Any


class MemoryStore:
    """Abstract base for memory storage"""
    
    def store(self, key: str, value: Any):
        raise NotImplementedError
    
    def retrieve(self, key: str) -> Any:
        raise NotImplementedError
    
    def search(self, query: str) -> List[Any]:
        raise NotImplementedError
