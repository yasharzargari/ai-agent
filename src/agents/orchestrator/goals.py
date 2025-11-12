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
            "After gathering web results, call `run_file_management_agent`  "
            "targeted at the user's request. Continue invoking it (with clarified instructions if needed) "
            "until you receive a successful response from the FileManagementAgent."
        ),
    ),
    Goal(
        priority=3,
        name="Aggregate Results",
        description=(
            "Only once both agents have produced successful results, call `synthesize_results` to merge them "
            "into a unified summary. If either result is missing or unsuccessful, loop back and resolve it first."
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