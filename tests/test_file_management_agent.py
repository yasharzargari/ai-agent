"""Tests for File Management agent"""

import pytest
from agents.file_management.agent import create_file_management_agent
from core.memory import Memory


def test_create_file_management_agent():
    """Test file management agent creation"""
    agent = create_file_management_agent()
    assert agent.name == "FileManagementAgent"
    assert len(agent.goals) > 0


def test_agent_has_actions():
    """Test agent has required actions"""
    agent = create_file_management_agent()
    action_names = agent.actions.get_action_names()
    assert "list_project_files" in action_names
    assert "read_project_file" in action_names
    assert "terminate" in action_names
