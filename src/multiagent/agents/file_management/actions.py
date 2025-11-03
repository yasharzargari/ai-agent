"""File Management Agent actions"""

from typing import List
from pathlib import Path

from ...tools.registry import register_tool


# Get the project root directory (assuming this file is in src/multiagent/agents/file_management/)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


@register_tool(tags=["file_operations", "read"])
def read_txt_file(filename: str) -> str:
    """Reads and returns the content of a specified .txt file from the data folder.

    Opens the file in read mode and returns its entire contents as a string.
    Raises FileNotFoundError if the file doesn't exist.

    Args:
        filename: The name of the .txt file to read (e.g., "Jenifer-Aniston.txt")

    Returns:
        The contents of the file as a string
    """
    # Ensure filename ends with .txt
    if not filename.endswith(".txt"):
        filename = f"{filename}.txt"
    
    file_path = DATA_DIR / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@register_tool(tags=["file_operations", "list"])
def list_txt_files() -> List[str]:
    """Lists all .txt files in the data folder.

    Scans the data directory and returns a sorted list of all files
    that end with '.txt'.

    Returns:
        A sorted list of .txt filenames in the data folder
    """
    if not DATA_DIR.exists():
        return []
    
    return sorted([file.name for file in DATA_DIR.iterdir() 
                   if file.is_file() and file.name.endswith(".txt")])


@register_tool(tags=["file_operations", "query"])
def answer_question_about_files(question: str, file_contents: str = None) -> str:
    """Answers questions about the content of .txt files in the data folder.

    This action helps answer questions about the files. If file_contents is provided,
    it will use that content to answer. Otherwise, it will need to read the files first.

    Args:
        question: The question to answer about the files
        file_contents: Optional pre-read content from files to answer the question

    Returns:
        An answer to the question based on the file contents
    """
    if file_contents:
        # If content is provided, use it to answer
        # This is a simple implementation - in a real system, you might use an LLM here
        return f"Answering question: {question}\n\nBased on the file contents provided, I can help answer your question. Please provide more specific file content or use read_txt_file to read specific files first."
    else:
        # Suggest reading files first
        available_files = list_txt_files()
        if available_files:
            return f"To answer your question '{question}', I need to read the relevant files first. Available files: {', '.join(available_files)}. Use read_txt_file to read specific files."
        else:
            return f"No .txt files found in the data folder to answer your question: {question}"


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."

