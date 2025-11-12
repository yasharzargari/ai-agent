"""File Management Agent actions"""

import json
from typing import List
from pathlib import Path

from ...core.action import ActionContext

from ...tools.registry import register_tool


# Get the project root directory (assuming this file is in src/agents/file_management/)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"


@register_tool(tags=["file_operations", "read"])
def read_txt_file(action_context: ActionContext, filename: str) -> str:
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
def list_txt_files(action_context: ActionContext) -> List[str]:
    """Lists all .txt files in the data folder.

    Scans the data directory and returns a sorted list of all files
    that end with '.txt'.

    Returns:
        A sorted list of .txt filenames in the data folder
    """
    print('>>>>>>>>', DATA_DIR)

    
    return sorted([file.name for file in DATA_DIR.iterdir() 
                   if file.is_file() and file.name.endswith(".txt")])


# @register_tool(tags=["file_operations", "answer"])
# def answer_question_about_files(action_context: ActionContext, question: str, file_contents: str = None) -> str:
#     """Answers questions about the content of .txt files in the data folder.

#     This action helps answer questions about the files. If file_contents is provided,
#     it will use that content to answer. Otherwise, it will need to read the files first.

#     Args:
#         question: The question to answer about the files
#         file_contents: Optional pre-read content from files to answer the question

#     Returns:
#         An answer to the question based on the file contents
#     """
#     if file_contents:
#         result = {
#             "question": question,
#             "status": "content_received",
#             "answer": (
#                 "Based on the provided file contents, here's a placeholder answer. "
#                 "Replace this logic with actual reasoning over the text."
#             ),
#         }
#         return json.dumps(result)

#     available_files = list_txt_files()
#     result = {
#         "question": question,
#         "status": "needs_content",
#         "message": (
#             "To answer the question, provide file_contents from the relevant files."
#             if available_files
#             else "No .txt files were found in the data directory."
#         ),
#         "available_files": available_files,
#     }
#     return json.dumps(result)


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."

