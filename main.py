from core.goal import Goal
from core.agent import Agent
from core.agent_language import AgentFunctionCallingActionLanguage
from actions.tool_actions import PythonActionRegistry
from environment.base_env import Environment
from llm.litellm_provider import generate_response
# The below line is neccessary 
from actions.file_actions import read_file_chunk, list_project_files, terminate


def main():
    # Define the agent's goals
    goals = [
        Goal(priority=1,
             name="Gather Information",
             description="Get the file names in the folder and find the one that is related to the user question"),
        Goal(priority=1,
             name="Answer question",
             description="Answer questions about the found file"),
        Goal(priority=1,
             name="Terminate",
             description="Call terminate when done")
    ]

    # Create an agent instance with tag-filtered actions
    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        # The ActionRegistry now automatically loads tools with these tags
        action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
        generate_response=generate_response,
        environment=Environment()
    )

    # Run the agent with user input
    user_input = "first list the files and then tell, which file is related about an actress and The actress name and when was she born"
    final_memory = agent.run(user_input)
    print(final_memory.get_memories())


if __name__ == "__main__":
    main()