from ...core.language import Goal

ORCHESTRATOR_GOALS = [
    Goal(
        priority=1,
        name="Collect Retrieval Data",
        description=(
            "Call the `run_retrieval_worker_agent` tool with the user’s web-information task. "
            "Do not proceed until you have a successful response from the RetrievalWorker agent."
        ),
    ),
    Goal(
        priority=2,
        name="Collect File Data",
        description=(
            "Call the `run_file_management_agent` tool with the user’s file-analysis task. "
            "Do not proceed until you have a successful response from the FileManagementAgent."
        ),
    ),
    Goal(
        priority=3,
        name="Aggregate Results",
        description=(
            "After both agents respond, call `synthesize_results` to combine their outputs into a single summary."
        ),
    ),
    Goal(
        priority=4,
        name="Deliver Final Output",
        description=(
            "Finish by invoking `terminate`, citing only information sourced from the delegated agents."
        ),
    ),
]