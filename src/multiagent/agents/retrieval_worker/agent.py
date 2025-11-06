from ...core.agent import Agent
from ...core.language import AgentFunctionCallingActionLanguage
from ...core.environment import Environment
from ...core.llm import generate_response
from ...tools.registry import PythonActionRegistry, register_tool
from .goals import RETRIEVAL_WORKER_GOALS

import requests
from bs4 import BeautifulSoup



@register_tool(tags=["retrieval"], terminal=False)
def query_database(query: str) -> str:
    """
    Execute a database query.
    
    Args:
        query: The database query to execute
    """
    # Placeholder - would implement actual database querying
    return f"Query results for '{query}': [Sample database results]"


@register_tool(tags=["retrieval"], terminal=False)
def fetch_from_web(url: str) -> str:
    """
    Fetches the first two paragraphs from a Wikipedia article.
    
    Args:
        url (str): The Wikipedia article URL
        
    Returns:
        list: A list containing the first two paragraphs as strings
    """
    # Add headers to avoid 403 error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Send GET request with headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all paragraphs
    all_paragraphs = soup.find_all('p')
    
    # Extract first two non-empty paragraphs
    paragraphs = []
    for p in all_paragraphs:
        text = p.get_text().strip()
        if text:  # Only add non-empty paragraphs
            paragraphs.append(text)
            if len(paragraphs) == 2:  # Stop after getting 2
                break
    
    return paragraphs


@register_tool(tags=["retrieval"], terminal=True)
def return_retrieval_results(results: str) -> str:
    """
    Return all normalized retrieval results.
    
    Args:
        results: JSON string of normalized retrieval results
    """
    return f"Retrieval complete. Results: {results}"


def create_retrieval_worker_agent():
    """Factory function to create a Retrieval Worker agent"""
    # Include both retrieval and file operation tools
    action_registry = PythonActionRegistry(tags=["retrieval", "file_operations"])
    
    return Agent(
        name="RetrievalWorker",
        goals=RETRIEVAL_WORKER_GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
