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
        description="Use read_txt_file to collect the contents of any files needed to answer the user question."
    ),
    Goal(
        priority=3,
        name="Answer in JSON",
        description=(
            "Call answer_question_about_files with the original question and the gathered file text so the final "
            "response is returned in JSON format."
        )
    ),
    Goal(
        priority=4,
        name="Terminate",
        description="Once the JSON answer is ready, call terminate and include that JSON in the message."
    )
]
