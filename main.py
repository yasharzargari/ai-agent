"""
Main entry point for the multiagent system.
Demonstrates the file management agent reading and analyzing project files.
"""

from src.agents.file_management.agent import create_file_management_agent
from src.agents.retrieval_worker.agent import create_retrieval_worker_agent
from src.agents.orchestrator.agent import create_orchestrator_agent
from src.core.agent_registry import AgentRegistry

def main(): 
    """Run the file management agent demo"""
    print("=" * 80)
    print("MULTIAGENT SYSTEM - FILE MANAGEMENT AGENT DEMO")
    print("=" * 80)
    print()
    
    # Create the agent
    file_management_agent = create_file_management_agent()
    retrieval_worker_agent = create_retrieval_worker_agent()
    orchestrator_agent = create_orchestrator_agent()

    agent_registry = AgentRegistry()
    agent_registry.register_agent(file_management_agent.name, file_management_agent.run)
    agent_registry.register_agent(retrieval_worker_agent.name, retrieval_worker_agent.run)
    user_input = "What is the population of Richmond? and what is the name of the person who lives in Richmond?"

    print(f"Task: {user_input}")
    print()
    print("Agent is now working...")
    print("=" * 80)
    print()
    
    # Run the agent
    final_memory = orchestrator_agent.run(
        user_input,
        max_iterations=13,
        action_context_props={
            "agent_registry": agent_registry
        }
    )
    
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
