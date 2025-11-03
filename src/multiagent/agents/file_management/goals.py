from ...core.language import Goal

FILE_MANAGEMENT_GOALS = [
    Goal(
        priority=1,
        name="List Available Files",
        description="List all .txt files available in the ./data folder to see what information is available"
    ),
    Goal(
        priority=2,
        name="Read Text Files",
        description="Read .txt files from the ./data folder to gather information and answer questions about their content"
    ),
    Goal(
        priority=3,
        name="Answer Questions",
        description="Answer questions about the content of the .txt files in the data folder using the read file contents"
    ),
    Goal(
        priority=4,
        name="Terminate",
        description="Call terminate when done and provide a complete answer or summary in the message parameter"
    )
]
