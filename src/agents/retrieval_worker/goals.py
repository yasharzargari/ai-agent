from ...core.language import Goal

RETRIEVAL_WORKER_GOALS = [
    Goal(
        priority=1,
        name="Fetch Content",
        description="Use fetch_from_web to retrieve the relevant web page content."
    ),
    Goal(
        priority=1,
        name="Answer in JSON",
        description=(
            "After fetching content, call answer_question_from_web with the original question and the fetched "
            "text so the response is emitted in JSON format."
        ),
    ),
    Goal(
        priority=1,
        name="Terminate",
        description="Call terminate once the JSON answer is ready and include that JSON in the message."
    ),
]