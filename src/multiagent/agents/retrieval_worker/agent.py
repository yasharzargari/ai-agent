from ...core.agent import Agent
from ...core.language import AgentFunctionCallingActionLanguage
from ...core.environment import Environment
from ...core.llm import generate_response
from ...tools.registry import PythonActionRegistry, register_tool
from .goals import RETRIEVAL_WORKER_GOALS


@register_tool(tags=["retrieval"], terminal=False)
def fetch_from_web(url: str) -> str:
    """
    Fetch content from a web URL.
    
    Args:
        url: The URL to fetch content from
    """
    # Placeholder - would implement actual web fetching
    return f"Fetched content from {url}: [Sample web content]"


@register_tool(tags=["retrieval"], terminal=False)
def query_database(query: str) -> str:
    """
    Execute a database query.
    
    Args:
        query: The database query to execute
    """
    # Placeholder - would implement actual database querying
    return f"Query results for '{query}': [Sample database results]"


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
