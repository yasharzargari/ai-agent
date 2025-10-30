from core.goal import Goal


def retrival_goals():
    """Get goals for file management agent."""
    return [
        Goal(
            priority=1,
            name="Gather Information",
            description="Read each file in the project in order to build a deep understanding of the project in order to write a README"
        ),
        Goal(
            priority=1,
            name="Terminate",
            description="Call terminate when done and provide a complete README for the project in the message parameter"
        )
    ]