"""Tests for memory broker"""

import pytest
from memory.broker import MemoryBroker


def test_share_memory(memory_broker):
    """Test sharing memory"""
    memory_broker.share_memory("agent_1", {"type": "user", "content": "test"})
    memories = memory_broker.get_shared_memories("agent_1")
    assert len(memories) == 1
    assert memories[0]["content"] == "test"


def test_get_all_shared_memories(memory_broker):
    """Test getting all shared memories"""
    memory_broker.share_memory("agent_1", {"type": "user", "content": "test1"})
    memory_broker.share_memory("agent_2", {"type": "user", "content": "test2"})
    
    all_memories = memory_broker.get_shared_memories()
    assert len(all_memories) == 2


def test_clear_agent_memories(memory_broker):
    """Test clearing agent memories"""
    memory_broker.share_memory("agent_1", {"type": "user", "content": "test"})
    memory_broker.clear_agent_memories("agent_1")
    
    memories = memory_broker.get_shared_memories("agent_1")
    assert len(memories) == 0
