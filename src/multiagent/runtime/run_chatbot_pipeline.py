"""Main chatbot pipeline with three agents"""

from ..agents.orchestrator.agent import create_orchestrator_agent
from ..agents.retrieval_worker.agent import create_retrieval_worker_agent
from ..agents.synthesizer.agent import create_synthesizer_agent
from ..orchestrators.coordinators.chatbot_pipeline import ChatbotPipelineOrchestrator


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║         MULTIAGENT CHATBOT SYSTEM                            ║
║         3-Agent Architecture                                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create the three agents
    orchestrator = create_orchestrator_agent()
    retrieval_worker = create_retrieval_worker_agent()
    synthesizer = create_synthesizer_agent()
    
    # Create pipeline orchestrator
    pipeline = ChatbotPipelineOrchestrator(
        agents=[orchestrator, retrieval_worker, synthesizer]
    )
    
    # Example query
    user_query = """
    I need a summary of all Python files in the current directory.
    For each file, tell me what it does and list any important functions or classes.
    """
    
    print(f"User Query: {user_query}\n")
    
    # Run the pipeline
    result = pipeline.coordinate(user_query)
    
    print("\n" + "=" * 60)
    print("FINAL RESPONSE TO USER:")
    print("=" * 60)
    print(result)
    print("\n")


if __name__ == "__main__":
    main()
