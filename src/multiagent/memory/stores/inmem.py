"""In-memory storage implementation"""

from typing import Any, List
from ..base import MemoryStore


class InMemoryStore(MemoryStore):
    """Simple in-memory key-value store"""
    
    def __init__(self):
        self.data = {}
    
    def store(self, key: str, value: Any):
        self.data[key] = value
    
    def retrieve(self, key: str) -> Any:
        return self.data.get(key)
    
    def search(self, query: str) -> List[Any]:
        """Simple substring search"""
        results = []
        for key, value in self.data.items():
            if query.lower() in str(value).lower():
                results.append({key: value})
        return results
