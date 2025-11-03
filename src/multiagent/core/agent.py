import json
from typing import List, Callable

from .language import Goal, Prompt, AgentLanguage
from .action import ActionRegistry
from .memory import Memory
from .environment import Environment


class Agent:
    """Base agent implementation with GAME loop"""
    
    def __init__(self,
                 goals: List[Goal],
                 agent_language: AgentLanguage,
                 action_registry: ActionRegistry,
                 generate_response: Callable[[Prompt], str],
                 environment: Environment,
                 name: str = "Agent"):
        self.name = name
        self.goals = goals
        self.generate_response = generate_response
        self.agent_language = agent_language
        self.actions = action_registry
        self.environment = environment

    def construct_prompt(self, goals: List[Goal], memory: Memory, 
                        actions: ActionRegistry) -> Prompt:
        """Build prompt with memory context"""
        return self.agent_language.construct_prompt(
            actions=actions.get_actions(),
            environment=self.environment,
            goals=goals,
            memory=memory
        )

    def get_action(self, response: str):
        """Parse response and get corresponding action"""
        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def should_terminate(self, response: str) -> bool:
        """Check if response indicates termination"""
        action_def, _ = self.get_action(response)
        return action_def and action_def.terminal

    def set_current_task(self, memory: Memory, task: str):
        """Set the current task in memory"""
        memory.add_memory({"type": "user", "content": task})

    def update_memory(self, memory: Memory, response: str, result: dict):
        """Update memory with agent decision and environment response"""
        new_memories = [
            {"type": "assistant", "content": response},
            {"type": "environment", "content": json.dumps(result)}
        ]
        for m in new_memories:
            memory.add_memory(m)

    def prompt_llm_for_action(self, full_prompt: Prompt) -> str:
        """Get action from LLM"""
        return self.generate_response(full_prompt)

    def run(self, user_input: str, memory: Memory = None, 
            max_iterations: int = 50) -> Memory:
        """Execute the GAME loop"""
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for iteration in range(max_iterations):
            print(f"\n[{self.name}] Iteration {iteration + 1}/{max_iterations}")
            
            prompt = self.construct_prompt(self.goals, memory, self.actions)
            response = self.prompt_llm_for_action(prompt)
            print(f"[{self.name}] Decision: {response[:200]}...")

            action, invocation = self.get_action(response)
            if not action:
                print(f"[{self.name}] Unknown action, terminating")
                break

            result = self.environment.execute_action(action, invocation["args"])
            print(f"[{self.name}] Result: {str(result)[:200]}...")

            self.update_memory(memory, response, result)

            if self.should_terminate(response):
                print(f"[{self.name}] Terminating")
                break

        return memory
