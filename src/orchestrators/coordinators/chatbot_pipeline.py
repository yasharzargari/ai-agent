from ...core.memory import Memory
from ..base import BaseOrchestrator
from ..protocols import MessageProtocol


class ChatbotPipelineOrchestrator(BaseOrchestrator):
    """Orchestrator for the 3-agent chatbot pipeline"""
    
    def coordinate(self, user_input: str) -> str:
        """
        Coordinate the three-agent pipeline:
        1. Orchestrator analyzes and dispatches
        2. Retrieval Worker fetches data
        3. Synthesizer consolidates and reports
        """
        print("\n" + "="*80)
        print("CHATBOT PIPELINE STARTED")
        print("="*80)
        
        # Phase 1: Orchestrator analyzes query
        print("\n--- PHASE 1: ORCHESTRATION ---")
        orchestrator = self.get_agent("Orchestrator")
        orchestrator_memory = Memory()
        
        orchestration_task = f"""
        Analyze this user query and determine what information needs to be retrieved:
        
        User Query: {user_input}
        
        Dispatch appropriate retrieval tasks to gather the needed information.
        """
        
        orchestrator_memory = orchestrator.run(
            orchestration_task, 
            memory=orchestrator_memory,
            max_iterations=10
        )
        
        # Extract orchestrator's plan
        retrieval_tasks = self._extract_retrieval_tasks(orchestrator_memory)
        
        # Phase 2: Retrieval Worker fetches data
        print("\n--- PHASE 2: RETRIEVAL ---")
        retrieval_worker = self.get_agent("RetrievalWorker")
        retrieval_memory = Memory()
        
        retrieval_task = f"""
        Execute the following retrieval tasks:
        
        {retrieval_tasks}
        
        Fetch all required information and normalize the results.
        """
        
        retrieval_memory = retrieval_worker.run(
            retrieval_task,
            memory=retrieval_memory,
            max_iterations=15
        )
        
        # Extract retrieval results
        retrieval_results = self._extract_retrieval_results(retrieval_memory)
        
        # Phase 3: Synthesizer consolidates and formats
        print("\n--- PHASE 3: SYNTHESIS ---")
        synthesizer = self.get_agent("Synthesizer")
        synthesizer_memory = Memory()
        
        synthesis_task = f"""
        Consolidate the following retrieved information and create a comprehensive summary:
        
        {retrieval_results}
        
        Remove duplicates, cluster by topic, and generate a well-structured report
        that answers the user's original question: {user_input}
        """
        
        synthesizer_memory = synthesizer.run(
            synthesis_task,
            memory=synthesizer_memory,
            max_iterations=10
        )
        
        # Extract final result
        final_result = self._extract_final_result(synthesizer_memory)
        
        print("\n" + "="*80)
        print("CHATBOT PIPELINE COMPLETED")
        print("="*80 + "\n")
        
        return final_result

    def _extract_retrieval_tasks(self, memory: Memory) -> str:
        """Extract retrieval tasks from orchestrator memory"""
        # Look for dispatch_retrieval_tasks calls
        for item in reversed(memory.items):
            if item.get("type") == "environment":
                import json
                try:
                    content = json.loads(item["content"])
                    if "Dispatched retrieval tasks" in content.get("result", ""):
                        return content["result"]
                except:
                    pass
        return "Read all relevant files and fetch any referenced web content"

    def _extract_retrieval_results(self, memory: Memory) -> str:
        """Extract results from retrieval worker memory"""
        # Look for return_retrieval_results calls
        for item in reversed(memory.items):
            if item.get("type") == "environment":
                import json
                try:
                    content = json.loads(item["content"])
                    result = content.get("result", "")
                    if "Retrieval complete" in result:
                        return result
                except:
                    pass
        
        # Fallback: collect all file read results
        results = []
        for item in memory.items:
            if item.get("type") == "environment":
                import json
                try:
                    content = json.loads(item["content"])
                    if content.get("tool_executed"):
                        results.append(str(content.get("result", "")))
                except:
                    pass
        return "\n\n".join(results)

    def _extract_final_result(self, memory: Memory) -> str:
        """Extract final result from synthesizer memory"""
        last_memory = memory.get_last_memory()
        if last_memory and last_memory.get("type") == "environment":
            import json
            try:
                result = json.loads(last_memory["content"])
                return result.get("result", "No result generated")
            except:
                pass
        return "Synthesis completed"
