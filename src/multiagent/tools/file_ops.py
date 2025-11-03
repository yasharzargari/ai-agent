import os
from typing import List
from .registry import register_tool


@register_tool(tags=["file_operations", "read"])
def read_file(filepath: str) -> str:
    """Read and return the contents of a file"""
    with open(filepath, "r") as f:
        return f.read()


@register_tool(tags=["file_operations", "list"])
def list_files(directory: str = ".") -> List[str]:
    """List all files in a directory"""
    return sorted([f for f in os.listdir(directory) 
                  if os.path.isfile(os.path.join(directory, f))])


@register_tool(tags=["file_operations", "list"])
def list_python_files(directory: str = ".") -> List[str]:
    """List all Python files in a directory"""
    return sorted([f for f in os.listdir(directory) 
                  if f.endswith(".py")])


@register_tool(tags=["file_operations", "write"])
def write_file(filepath: str, content: str) -> str:
    """Write content to a file"""
    with open(filepath, "w") as f:
        f.write(content)
    return f"Successfully wrote to {filepath}"


@register_tool(tags=["file_operations", "search"])
def search_in_file(filepath: str, search_term: str) -> str:
    """Search for a term in a file and return matching lines"""
    matches = []
    with open(filepath, "r") as f:
        for line_num, line in enumerate(f, 1):
            if search_term in line:
                matches.append(f"Line {line_num}: {line.strip()}")
    return "\n".join(matches) if matches else "No matches found"


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminate execution with a final message"""
    return f"{message}\nTerminating..."
