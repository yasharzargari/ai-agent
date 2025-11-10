from ...tools.agent_tools import build_agent
from ...tools.registry import register_tool
from .goals import SYNTHESIZER_GOALS


@register_tool(tags=["synthesis"], terminal=False)
def deduplicate_content(content: str) -> str:
    """
    Deduplicate similar content items.
    
    Args:
        content: Content to deduplicate
    """
    return f"Deduplicated content: {content[:200]}..."


@register_tool(tags=["synthesis"], terminal=False)
def cluster_by_topic(content: str, num_clusters: int) -> str:
    """
    Cluster content into topics.
    
    Args:
        content: Content to cluster
        num_clusters: Number of topic clusters to create
    """
    return f"Created {num_clusters} topic clusters"


@register_tool(tags=["synthesis"], terminal=True)
def return_synthesis_result(summary: str) -> str:
    """
    Return the final synthesized summary.
    
    Args:
        summary: The complete summary report
    """
    return f"Synthesis complete:\n\n{summary}"


def create_synthesizer_agent():
    """Factory function to create a Synthesizer agent."""
    return build_agent(
        name="Synthesizer",
        goals=SYNTHESIZER_GOALS,
        tags=["synthesis"],
    )
