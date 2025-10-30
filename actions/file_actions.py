import os
from typing import List
from actions.tool_actions import register_tool


@register_tool(tags=["file_operations", "read"])
def read_file_chunk(name: str) -> str:
    """Reads and returns the content of a specified project file.

    Opens the file in read mode and returns its entire contents as a string.
    Raises FileNotFoundError if the file doesn't exist.

    Args:
        name: The name of the file to read

    Returns:
        The contents of the file as a string
    """
    log_path = os.path.join("data", name)

    if not os.path.exists(log_path):
        raise FileNotFoundError(f"File not found: {log_path}")

    with open(log_path, "r", encoding="utf-8") as f:
        return f.read()


@register_tool(tags=["file_operations", "list"])
def list_project_files() -> List[str]:
    """Lists all Python files in the current project directory.

    Scans the current directory and returns a sorted list of all files
    that end with '.txt'.

    Returns:
        A sorted list of Python filenames
    """
    return sorted([file for file in os.listdir("./data")
                  if file.endswith(".txt")])


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."