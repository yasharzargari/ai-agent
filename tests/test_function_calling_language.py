"""Tests for function calling language"""

import pytest
from multiagent.core.language import AgentFunctionCallingActionLanguage, Goal
from multiagent.core.memory import Memory
from multiagent.core.action import Action


def test_format_goals():
    """Test goal formatting"""
    language = AgentFunctionCallingActionLanguage()
    goals = [Goal(priority=1, name="Test", description="Test goal")]
    
    messages = language.format_goals(goals)
    assert len(messages) == 1
    assert messages[0]["role"] == "system"
    assert "Test" in messages[0]["content"]


def test_format_memory(sample_memory):
    """Test memory formatting"""
    language = AgentFunctionCallingActionLanguage()
    messages = language.format_memory(sample_memory)
    
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
