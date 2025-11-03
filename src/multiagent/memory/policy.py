"""Memory retention policies"""


class RetentionPolicy:
    """Defines when to keep or discard memories"""
    
    def should_retain(self, memory: dict) -> bool:
        """Determine if a memory should be retained"""
        return True


class RecentRetentionPolicy(RetentionPolicy):
    """Keep only recent N memories"""
    
    def __init__(self, max_items: int = 100):
        self.max_items = max_items
    
    def apply(self, memories: list) -> list:
        """Keep only most recent memories"""
        return memories[-self.max_items:]
