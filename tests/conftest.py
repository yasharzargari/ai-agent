"""Pytest configuration and fixtures"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_memory():
    """Create a sample memory for testing"""
    from core.memory import Memory
    memory = Memory()
    memory.add_memory({"type": "user", "content": "Hello"})
    memory.add_memory({"type": "assistant", "content": "Hi there"})
    return memory


@pytest.fixture
def sample_environment():
    """Create a sample environment"""
    from core.environment import Environment
    return Environment()


@pytest.fixture
def memory_broker():
    """Create a memory broker for testing"""
    from memory.broker import MemoryBroker
    return MemoryBroker()
