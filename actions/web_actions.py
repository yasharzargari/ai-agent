import os
from typing import List
from actions.tool_actions import register_tool
import requests
from bs4 import BeautifulSoup



@register_tool(tags=["web_operations", "read"])
def read_website_content() -> str:
    """Reads and returns the first paraghraph of the specified website.
    Raises FileNotFoundError if the website doesn't exist.

    Returns:
        The first paraghraph of the specified website as a string
    """
    url = "https://en.wikipedia.org/wiki/Friends"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; FirstParagraphBot/1.0; +https://github.com/yasharzargari)"
    }

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")

    # Wikipedia article text lives under .mw-parser-output
    content = soup.select_one("#mw-content-text .mw-parser-output")

    first_paragraph = None
    if content:
        for p in content.find_all("p", recursive=False):
            text = p.get_text(strip=True)
            if text:  # skip empty/short lead-ins
                first_paragraph = text
                break

    # Fallback: look deeper if the first layer had no <p> with text
    if not first_paragraph and content:
        for p in content.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                first_paragraph = text
                break
    return first_paragraph or ">>>> No paragraph found."


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."