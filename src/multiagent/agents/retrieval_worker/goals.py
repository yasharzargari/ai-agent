from ...core.language import Goal

RETRIEVAL_WORKER_GOALS = [
    Goal(
        priority=1,
        name="Execute Retrieval Tasks",
        description="""
        Execute all assigned retrieval tasks in parallel:
        - Read from files if file sources specified
        - Fetch from web if URLs provided
        - Query databases if database access needed
        - Handle errors gracefully with fallbacks
        """
    ),
    Goal(
        priority=2,
        name="Normalize Results",
        description="""
        Normalize all retrieved data into a consistent format:
        - Extract key information from each source
        - Tag data with source metadata
        - Ensure consistent structure across different source types
        """
    ),
    Goal(
        priority=3,
        name="Return Results",
        description="""
        Return normalized results using the return_retrieval_results tool.
        Include all fetched data with proper attribution.
        """
    )
]
