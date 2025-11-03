from ...core.language import Goal

ORCHESTRATOR_GOALS = [
    Goal(
        priority=1,
        name="Analyze Query",
        description="""
        Analyze the user's request to understand:
        - Intent and desired outcome
        - Information sources needed (files, web, databases)
        - Time windows or constraints
        - Required retrieval strategies
        """
    ),
    Goal(
        priority=2,
        name="Dispatch Tasks",
        description="""
        Break down the query into subtasks and dispatch to the Retrieval Worker:
        - Specify which sources to query
        - Define parallel retrieval tasks
        - Set parameters for each retrieval operation
        Use the dispatch_retrieval_tasks tool to send tasks.
        """
    ),
    Goal(
        priority=3,
        name="Coordinate Synthesis",
        description="""
        After retrieval is complete, coordinate the Synthesizer to:
        - Consolidate retrieved information
        - Generate structured summary
        - Format final response
        Use the request_synthesis tool when ready.
        """
    )
]
