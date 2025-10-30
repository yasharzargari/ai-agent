from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Prompt:
    """Container for LLM prompt with messages, tools, and metadata."""
    messages: List[Dict] = field(default_factory=list)
    tools: List[Dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)