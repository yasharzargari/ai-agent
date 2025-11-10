"""
Main entry point for the multiagent system.
Demonstrates the file management agent reading and analyzing project files.
"""

import os
from src.multiagent.agents.file_management.agent import create_file_management_agent
from src.multiagent.agents.retrieval_worker.agent import create_retrieval_worker_agent


def main():
    """Run the file management agent demo"""
    print("=" * 80)
    print("MULTIAGENT SYSTEM - FILE MANAGEMENT AGENT DEMO")
    print("=" * 80)
    print()
    
    # Create the agent
    agent = create_file_management_agent()
    # agent = create_retrieval_worker_agent()
    
    # Define the task
    user_input = "Read all .txt files from the data folder and tell me when and were was she born."
    # user_input = "Fetch the information from the wikipedia page provided to you and only answer using that infor tell me who are the actors in frients series."
    # user_input = (
    #     "Fetch information from https://en.wikipedia.org/wiki/Zonuz and extract the following: "
    #     "city name, 2016 census population, and number of households. "
        
    # )

    print(f"Task: {user_input}")
    print()
    print("Agent is now working...")
    print("=" * 80)
    print()
    
    # Run the agent
    final_memory = agent.run(user_input, max_iterations=50)
    
    # Display results
    print()
    print("=" * 80)
    print("AGENT EXECUTION COMPLETE")
    print("=" * 80)
    print()
    
    # Extract and display the final result
    last_memory = final_memory.get_last_memory()
    if last_memory:
        import json
        if last_memory.get("type") == "environment":
            try:
                result = json.loads(last_memory["content"])
                if "result" in result:
                    print("FINAL OUTPUT:")
                    print("-" * 80)
                    print(result["result"])
                    print("-" * 80)
            except:
                print(last_memory.get("content", "No output generated"))
    
    print()
    print("Memory items created:", len(final_memory.items))
    print()


if __name__ == "__main__":
    main()
