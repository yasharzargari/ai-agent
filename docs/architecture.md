# Multiagent System Architecture

## Overview

This system implements a flexible multi-agent architecture for intelligent query processing and response synthesis, based on the GAME (Goals-Actions-Memory-Environment) framework.

## Core Framework: GAME Loop

Every agent in this system follows the GAME loop:

1. **Goals**: Define what the agent should accomplish
2. **Actions**: Tools and functions the agent can execute
3. **Memory**: Conversation history and context
4. **Environment**: Executes actions and returns results

The agent iteratively:
- Constructs a prompt from goals, actions, and memory
- Gets a decision from the LLM
- Executes the chosen action
- Updates memory with results
- Repeats until termination condition is met

## Agent Roles

### 1. Orchestrator/Router

**Responsibility**: Query analysis and task distribution

**Key Functions**:
- Parses user requests to understand intent
- Determines scope and time windows
- Dispatches subtasks to appropriate agents
- Coordinates overall workflow

**Tools**:
- Query parsing and classification
- Task decomposition
- Agent selection and routing

### 2. Retrieval Worker

**Responsibility**: Parallel data fetching from multiple sources

**Key Functions**:
- Executes source-specific retrieval operations
- Fetches data from files, web APIs, databases
- Normalizes results into consistent format
- Handles errors and retries

**Tools**:
- File operations (read, search)
- Web scraping and API calls
- Database queries
- Result normalization

### 3. Synthesizer/Reporter

**Responsibility**: Information consolidation and report generation

**Key Functions**:
- Deduplicates retrieved information
- Clusters content by topic or ticket
- Generates structured summaries
- Formats final reports with source attribution

**Tools**:
- Text similarity and deduplication
- Topic clustering
- Summary generation
- Report formatting

### 4. File Management Agent

**Responsibility**: Demonstration agent for project analysis

**Key Functions**:
- Lists and reads project files
- Analyzes code structure
- Generates documentation
- Demonstrates core framework capabilities

**Tools**:
- File listing
- File reading
- Content analysis

## Communication Flow

```
User Query
    ↓
Orchestrator (analyzes and decomposes)
    ↓
Retrieval Worker (parallel fetching)
    ↓
Synthesizer (consolidation and formatting)
    ↓
Final Response
```

## Memory Architecture

Each agent maintains:
- **Working Memory**: Current conversation context (Memory class)
- **Shared Memory**: Inter-agent communication channel (MemoryBroker)
- **Persistent Memory**: Long-term storage (optional, via MemoryStore)

### Shared Memory System

The `MemoryBroker` enables agents to share information:

```python
broker = MemoryBroker()
broker.share_memory("agent_1", {"type": "result", "content": "..."})
memories = broker.get_shared_memories("agent_1")
```

This allows for:
- Inter-agent communication
- Context preservation across agent handoffs
- Collaborative problem-solving

## Extension Points

- **Add new tools**: Use `@register_tool` decorator with tags
- **Create specialized agents**: Subclass `Agent` or use factory pattern
- **Implement custom orchestration**: Extend `BaseOrchestrator`
- **Add memory backends**: Implement `MemoryStore` interface
- **Share context between agents**: Use `MemoryBroker`

## Example: Creating a New Agent

```python
from src.multiagent.core.agent import Agent
from src.multiagent.core.language import Goal, AgentFunctionCallingActionLanguage
from src.multiagent.tools.registry import PythonActionRegistry, register_tool

# 1. Define goals
GOALS = [
    Goal(priority=1, name="Task", description="What to do"),
    Goal(priority=2, name="Terminate", description="When to stop")
]

# 2. Register tools
@register_tool(tags=["my_agent"])
def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

@register_tool(tags=["my_agent"], terminal=True)
def terminate(message: str) -> str:
    """Terminate execution"""
    return f"{message}\nDone!"

# 3. Create agent factory
def create_my_agent():
    action_registry = PythonActionRegistry(tags=["my_agent"])
    return Agent(
        name="MyAgent",
        goals=GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )

# 4. Use the agent
agent = create_my_agent()
memory = agent.run("Do something")
```
