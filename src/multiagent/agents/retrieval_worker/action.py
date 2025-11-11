
from typing import Optional
import json
from ...tools.registry import register_tool
import requests
from bs4 import BeautifulSoup
from ...core.action import ActionContext


ALLOWED_URLS = {
    "richmond": "https://en.wikipedia.org/wiki/Richmond,_Virginia",
}


@register_tool(tags=["web_operations", "fetch"])
def fetch_from_web(action_context: ActionContext,url: Optional[str] = None) -> str:
    """Fetches the first two paragraphs from approved Wikipedia articles.

    Opens the URL and extracts the first two non-empty paragraphs. If no URL is
    supplied, the default Richmond page is used. Only URLs from the allow-list are fetched.

    Returns:
        The first two paragraphs concatenated as a single string.
    """
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/91.0.4472.124 Safari/537.36')
    }

    # ✅ Respect the allow-list and default correctly
    normalized_url = (url or "").strip()
    if not normalized_url:
        normalized_url = ALLOWED_URLS["richmond"]
    elif normalized_url not in ALLOWED_URLS.values():
        raise ValueError(f"URL '{normalized_url}' is not permitted. Use one of the approved URLs.")

    response = requests.get(normalized_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text:
            paragraphs.append(text)
        if len(paragraphs) == 2:
            break

    # ✅ Always return a string (never a list)
    return "\n\n".join(paragraphs)


# @register_tool(tags=["web_operations"])
# def answer_question_from_web(action_context: ActionContext,question: str, web_content: str = None) -> str:
#     """Answers questions about the content fetched from web pages.
    
#     This action helps answer questions about web content. If web_content is provided,
#     it will use that content to answer. Otherwise, it will need to fetch the content first.
    
#     Args:
#         question: The question to answer about the web content
#         web_content: Optional pre-fetched content from web pages to answer the question
    
#     Returns:
#         An answer to the question based on the web content in JSON format
#     """
#     if web_content:
#         # If content is provided, use it to answer
#         # This is a simple implementation - in a real system, you might use an LLM here
#         result = {
#             "question": question,
#             "answer": "Based on the web content provided, I can help answer your question. Please provide more specific web content or use fetch_from_web to fetch from specific URLs first.",
#             "status": "content_received"
#         }
#         return json.dumps(result)
#     else:
#         # Suggest fetching content first
#         result = {
#             "question": question,
#             "message": f"To answer your question '{question}', I need to fetch the relevant web content first. Please provide a URL and use fetch_from_web to retrieve the content from that URL.",
#             "status": "needs_content"
#         }
#         return json.dumps(result)





@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."