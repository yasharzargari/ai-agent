"""Tests for tool registry"""

from multiagent.tools.registry import register_tool, tools, PythonActionRegistry


def test_register_tool():
    """Test tool registration"""
    @register_tool(tags=["test"])
    def test_function(x: int) -> int:
        """Test function"""
        return x * 2
    
    assert "test_function" in tools
    assert tools["test_function"]["description"] == "Test function"


def test_python_action_registry():
    """Test action registry creation"""
    registry = PythonActionRegistry(tags=["file_operations"])
    actions = registry.get_actions()
    assert len(actions) > 0
