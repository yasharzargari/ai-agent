# Multi-Agent System: Comprehensive Technical Documentation

## Executive Summary

This project implements a production-grade multi-agent orchestration system built on the **GAME (Goals–Actions–Memory–Environment)** architecture pattern. The system provides a flexible framework for coordinating specialized AI agents that collaborate to solve complex tasks requiring data retrieval, file operations, and intelligent synthesis.

**Key Capabilities:**
- Modular multi-agent coordination with specialized roles
- LLM-agnostic design supporting OpenAI-compatible function calling APIs
- Extensible tool registry with decorator-based registration
- Shared memory management for inter-agent communication
- Production-ready error handling and execution environment

---

## Installation and Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- OpenAI API key (or compatible LLM provider)

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yasharzargari/ai-agent
cd ai-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Add your OpenAI API key to the `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

### Running the Application

**Run the multi-agent demo:**
```bash
python main.py
```

This will execute the orchestrator agent which:
- Delegates a web query to the RetrievalWorker agent
- Delegates a file query to the FileManagementAgent
- Synthesizes results from both agents
- Returns a comprehensive answer

**Expected Output:**
```
================================================================================
MULTIAGENT SYSTEM - FILE MANAGEMENT AGENT DEMO
================================================================================

✓ Registered agent: FileManagementAgent
✓ Registered agent: RetrievalWorker
Task: What is the population of Richmond? and what is the name of the person 
      who lives in Richmond?

Agent is now working...
...
FINAL OUTPUT:
Richmond, Virginia, has a population of 226,610 as of the 2020 census. 
Additionally, Peter Parker is mentioned as residing in Richmond.
================================================================================
```

**Alternative Entry Points:**

Run the chatbot pipeline (if configured):
```bash
python -m src.runtime.run_chatbot_pipeline
```

Or use the Makefile shortcuts:
```bash
make run-file-agent
make run-chatbot
```

---

## 1. Architectural Overview

### 1.1 The GAME Loop Pattern

The foundation of this system is the GAME loop, which every agent executes:

```
┌──────────────────────────────────────────┐
│  GAME Loop (Agent.run())                 │
├──────────────────────────────────────────┤
│  1. Goals      → Define objectives       │
│  2. Actions    → Available tools         │
│  3. Memory     → Conversation history    │
│  4. Environment→ Action execution layer  │
└──────────────────────────────────────────┘
```

**Execution Flow:**
1. **Construct Prompt**: Combine goals, available actions, and memory into an LLM prompt
2. **LLM Decision**: Query the language model to select the next action
3. **Execute Action**: Run the selected tool in the environment with error handling
4. **Update Memory**: Store the action and result for context in subsequent iterations
5. **Check Termination**: Repeat until a terminal action is invoked or max iterations reached

This pattern ensures agents are:
- **Goal-oriented**: Every action serves defined objectives
- **Context-aware**: Full conversation history informs decisions
- **Recoverable**: Errors are captured and can guide agent behavior
- **Observable**: Every decision and result is logged in memory

### 1.2 Multi-Agent Architecture

The system implements a hierarchical multi-agent pattern with specialized roles:

```
┌─────────────────────────────────────────────────┐
│                 User Query                      │
└─────────────────────┬────────────────────-──────┘
                      │
                      ▼
         ┌────────────────────────┐
         │    Orchestrator        │  ← Task decomposition
         │  (Coordinator Agent)   │     & routing logic
         └────────┬───────────────┘
                  │
         ┌────────┴──────────┐
         │                   │
         ▼                   ▼
┌─────────────────┐  ┌──────────────────┐
│ Retrieval Worker│  │ File Management  │
│  (Web/API Data) │  │   Agent (Files)  │
└────────┬────────┘  └────────┬─────────┘
         │                    │
         └──────────┬─────────┘
                    │
                    ▼
            ┌──────────────┐
            │ Final Result │
            └──────────────┘
```

**Agent Roles:**

1. **Orchestrator**: 
   - Analyzes user intent and decomposes complex queries
   - Routes sub-tasks to appropriate specialist agents
   - Synthesizes results from multiple agents
   - Enforces execution order and dependencies

2. **Retrieval Worker**:
   - Fetches data from external sources (web, APIs, databases)
   - Normalizes heterogeneous data formats
   - Returns structured JSON responses

3. **File Management Agent**:
   - Reads, analyzes, and manipulates project files
   - Provides file system operations as tools
   - Demonstrates the framework's extensibility

---

## 2. Core Components Deep Dive

### 2.1 Agent (`src/core/agent.py`)

The `Agent` class is the heart of the system, implementing the GAME loop.

**Key Methods:**

```python
class Agent:
    def run(self, user_input: str, memory: Memory = None, 
            max_iterations: int = 13, action_context_props=None) -> Memory:
        """
        Main execution loop. Returns final memory state.
        Iteration limit prevents infinite loops.
        """
        
    def construct_prompt(self, goals: List[Goal], memory: Memory, 
                        actions: ActionRegistry) -> Prompt:
        """
        Builds LLM prompt from goals, memory, and available actions.
        Delegates formatting to AgentLanguage protocol.
        """
        
    def get_action(self, response: str) -> Tuple[Action, dict]:
        """
        Parses LLM response and retrieves corresponding Action.
        Returns both Action definition and invocation parameters.
        """
```

**Design Decisions:**

- **Dependency Injection**: All dependencies (language protocol, LLM client, environment) are injected, enabling easy testing and swapping
- **Memory Persistence**: Returns final memory state, allowing orchestrators to chain agents
- **Configurable Iterations**: Prevents runaway execution while allowing complex tasks
- **Action Context**: Passes shared state (agent registry, memory) to actions via `ActionContext`

### 2.2 Actions & Tools (`src/core/action.py`, `src/tools/registry.py`)

The action system provides a plugin architecture for extending agent capabilities.

**Action Definition:**

```python
class Action:
    name: str                    # Unique identifier
    function: Callable           # Implementation
    description: str             # LLM-readable documentation
    parameters: Dict             # JSON Schema for arguments
    terminal: bool               # Marks end of execution
    accepts_action_context: bool # Receives shared state
```

**Tool Registration Pattern:**

```python
@register_tool(
    tags=["orchestrator_delegation"],
    terminal=False
)
def run_retrieval_worker_agent(
    action_context: ActionContext,
    task: str
) -> str:
    """
    Delegate a task to the RetrievalWorker agent.
    Tags enable selective tool loading per agent.
    """
    result = call_agent(
        action_context=action_context,
        agent_name="RetrievalWorker",
        task=task
    )
    return json.dumps(result)
```

**Registry Architecture:**

- **Global Tool Registry**: Decorator pattern registers tools at import time
- **Tag-Based Filtering**: `PythonActionRegistry(tags=["web_operations"])` loads only relevant tools
- **Automatic Schema Generation**: Introspects function signatures to generate JSON Schema
- **Context Injection**: Detects `action_context` parameter and injects shared state

**Benefits:**

- New tools added by decorating functions—no registry modifications needed
- Type hints automatically generate parameter schemas
- Tags prevent tool pollution (orchestrator doesn't see file tools)
- Context allows tools to access memory, LLM, and other agents

### 2.3 Memory System (`src/core/memory.py`)

Memory architecture:

**Agent Memory** (`Memory`):
- Per-agent conversation history
- Three message types: `user`, `assistant`, `environment`
- Simple list-based storage with optional windowing
- Can be passed between agents for context transfer

```python
# Agent memory example
memory = Memory()
memory.add_memory({"type": "user", "content": "What is the population?"})
memory.add_memory({"type": "assistant", "content": "tool: fetch_from_web, args: {}"})
memory.add_memory({"type": "environment", "content": '{"result": "population data"}'})
```

**Future Extensions:**

The current memory system can be extended with vector database integration for semantic search and long-term memory:

- **Vector Store Integration**: Add Pinecone, Weaviate, or Chroma for embedding-based retrieval
- **Semantic Search**: Query past conversations by meaning rather than exact matches
- **Long-term Memory**: Persist important information across sessions
- **Memory Summarization**: Compress old conversations while retaining key facts
- **Cross-agent Memory**: Share relevant context between agents via semantic similarity

This would enable agents to:
- Recall relevant information from thousands of past interactions
- Learn from previous task executions
- Build knowledge bases from accumulated experiences

### 2.4 Language Protocol (`src/core/language.py`)

Abstracts LLM communication formats for portability.

**AgentFunctionCallingActionLanguage:**
- Implements OpenAI-style function calling
- Converts `Goal` objects into system prompts
- Formats `Memory` as conversation messages
- **Transforms `Action` definitions into function schemas for LLM function calling**

**How Actions Are Passed to the LLM:**

The core mechanism of the system is that **all registered actions are converted to function schemas and passed to the LLM as available tools**. This enables the LLM to decide which action to invoke based on the current goals and context.

```python
# Actions are converted from this:
@register_tool(tags=["web_operations"])
def fetch_from_web(url: str) -> str:
    """Fetches content from approved Wikipedia URLs"""
    # ... implementation

# Into this function schema for the LLM:
{
  "type": "function",
  "function": {
    "name": "fetch_from_web",
    "description": "Fetches content from approved Wikipedia URLs",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {"type": "string"}
      },
      "required": ["url"]
    }
  }
}
```

**Complete Prompt Structure:**

The agent constructs a complete prompt with both conversation history and available actions:

```python
Prompt:
  messages: [
    {"role": "system", "content": "Goal 1: Fetch data\n---\nDescription..."},
    {"role": "user", "content": "What is the population of Richmond?"},
    {"role": "assistant", "content": '{"tool": "fetch_from_web", "args": {}}'},
    {"role": "assistant", "content": '{"result": "population data"}'}
  ]
  tools: [  # ← Actions converted to function schemas
    {"type": "function", "function": {"name": "fetch_from_web", ...}},
    {"type": "function", "function": {"name": "terminate", ...}}
  ]
```

**Sending to the LLM:**

This prompt structure is then sent to the LLM via the function calling API:

```python
response = litellm.completion(
    model=os.getenv("MODEL", "gpt-4o"),
    messages=prompt.messages,
    tools=prompt.tools,  # ← Actions passed as tools parameter
    temperature=0.7
)
```

When the LLM receives this prompt, it can call any of the provided functions. The agent then:
1. Parses the function call from the LLM response
2. Executes the corresponding action via the Environment
3. Adds the result to memory
4. Repeats until a terminal action is called

**Extensibility**: Implement `AgentLanguage` interface to support:
- Claude/Anthropic tool use format
- ReAct prompting patterns
- Custom DSLs for specialized domains

### 2.5 Environment (`src/core/environment.py`)

Sandboxed execution layer with standardized error handling.

```python
class Environment:
    def execute_action(self, action: Action, args: dict, 
                      action_context=None) -> dict:
        """
        Executes action with error recovery.
        Returns standardized result format.
        """
        try:
            result = action.execute(action_context=action_context, **args)
            return {
                "tool_executed": True,
                "result": result,
                "timestamp": "2026-01-11T..."
            }
        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
```

**Key Features:**

- **Exception Isolation**: Action failures don't crash the agent
- **Structured Results**: Consistent format enables LLM understanding
- **Observability**: Timestamps and tracebacks aid debugging
- **Future Extensions**: Can add sandboxing, rate limiting, cost tracking

---

## 3. Agent Implementations

### 3.1 Orchestrator Agent

**Purpose**: Coordinates multiple specialist agents to solve complex, multi-step tasks.

**Goals** (prioritized):

1. **Collect Retrieval Data**: Delegate web/API queries to RetrievalWorker
2. **Collect File Data**: Delegate file operations to FileManagementAgent
3. **Aggregate Results**: Synthesize data from both agents
4. **Deliver Final Output**: Return comprehensive answer

**Tools**:
- `run_retrieval_worker_agent(task: str)` - Spawns retrieval worker
- `run_file_management_agent(task: str)` - Spawns file agent
- `synthesize_results(web_results: str, file_results: str)` - Merges data
- `terminate(message: str)` - Returns final answer

**Execution Pattern**:

```
Orchestrator receives: "What is the population of Richmond and who lives there?"
  ↓
1. Calls run_retrieval_worker_agent("What is the population of Richmond?")
   → RetrievalWorker fetches from Wikipedia
   → Returns: {"population": "226,610"}
  ↓
2. Calls run_file_management_agent("Find person living in Richmond")
   → FileManagementAgent reads data/richmond.txt
   → Returns: {"resident": "Peter Parker"}
  ↓
3. Calls synthesize_results(web_data, file_data)
   → Merges information
  ↓
4. Calls terminate("Richmond population: 226,610, Resident: Peter Parker")
```

**Configuration** (`config/agents.yaml`):
```yaml
orchestrator:
  name: Orchestrator
  model: openai/gpt-4o
  max_iterations: 10
  temperature: 0.7  # Higher for creative routing
```

### 3.2 Retrieval Worker Agent

**Purpose**: Fetches and structures data from external sources.

**Goals**:
1. **Fetch Content**: Use web fetching tools
2. **Answer in JSON**: Structure response for programmatic use
3. **Terminate**: Return structured result

**Tools**:
- `fetch_from_web(url: Optional[str])` - Retrieves Wikipedia articles
- `terminate(message: str)` - Returns final JSON

**Security Features**:
- **URL Allowlist**: Only approved URLs (prevents SSRF attacks)
- **Content Limits**: Extracts first 2 paragraphs (prevents excessive data)
- **User-Agent**: Proper headers for respectful scraping

**Example Tool Implementation**:

```python
@register_tool(tags=["web_operations", "fetch"])
def fetch_from_web(action_context: ActionContext, 
                   url: Optional[str] = None) -> str:
    ALLOWED_URLS = {
        "richmond": "https://en.wikipedia.org/wiki/Richmond,_Virginia"
    }
    
    normalized_url = (url or "").strip() or ALLOWED_URLS["richmond"]
    if normalized_url not in ALLOWED_URLS.values():
        raise ValueError(f"URL '{normalized_url}' not permitted")
    
    response = requests.get(normalized_url, headers={...})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text:
            paragraphs.append(text)
        if len(paragraphs) == 2:
            break
    
    return "\n\n".join(paragraphs)
```

### 3.3 File Management Agent

**Purpose**: Demonstrates framework capabilities through file operations.

**Goals**:
1. **Read Files**: Access project files
2. **Analyze Content**: Extract relevant information
3. **Return Results**: Provide structured responses

**Tools** (example):
- `read_file(path: str)` - Reads file contents
- `list_files(directory: str)` - Lists directory contents
- `search_in_files(pattern: str)` - Searches file contents
- `terminate(message: str)` - Returns final result

**Use Cases**:
- Project analysis and documentation generation
- Code search and refactoring assistance
- Configuration file validation
- Dependency auditing

---

## 4. Agent Registry & Delegation

### 4.1 Agent Registry (`src/core/agent_registry.py`)

Enables dynamic agent discovery and invocation.

```python
class AgentRegistry:
    def register_agent(self, name: str, agent_runner: Callable):
        """Register agent's run function by name"""
        
    def get_agent(self, name: str) -> Optional[Callable]:
        """Retrieve agent runner by name"""
        
    def run_agent(self, name: str, task: str, 
                  max_iterations: int, **kwargs) -> Memory:
        """Execute agent and return memory"""
```

**Usage Pattern**:

```python
# Setup in main.py
registry = AgentRegistry()
registry.register_agent("RetrievalWorker", retrieval_agent.run)
registry.register_agent("FileManagementAgent", file_agent.run)

# Pass to orchestrator
orchestrator.run(
    user_input="...",
    action_context_props={"agent_registry": registry}
)

# Tools can now delegate
def run_retrieval_worker_agent(action_context: ActionContext, task: str):
    registry = action_context.get_agent_registry()
    agent_runner = registry.get_agent("RetrievalWorker")
    memory = agent_runner(task, max_iterations=15)
    return extract_result(memory)
```

### 4.2 Agent Communication Protocol

**ActionContext** carries shared state:

```python
ActionContext:
  context_id: str               # Unique execution ID
  properties: {
    "memory": Memory,           # Current agent's memory
    "llm": Callable,            # LLM client
    "agent_registry": Registry  # For delegation
  }
```

**call_agent Helper** (`src/tools/agent_tools.py`):

```python
def call_agent(action_context: ActionContext, 
               agent_name: str, 
               task: str) -> dict:
    """
    Standard delegation pattern:
    1. Retrieve agent from registry
    2. Execute with fresh memory
    3. Extract result from final memory state
    4. Return structured response
    """
    registry = action_context.get_agent_registry()
    agent_runner = registry.get_agent(agent_name)
    
    final_memory = agent_runner(
        user_input=task,
        max_iterations=config.max_iterations,
        action_context_props=action_context.properties
    )
    
    return {
        "agent": agent_name,
        "result": extract_final_result(final_memory),
        "success": True
    }
```

---

## 5. Configuration & LLM Integration

### 5.1 Configuration System (`src/config/`)

**agents.yaml**: Per-agent configuration
```yaml
orchestrator:
  model: openai/gpt-4o      # LiteLLM model identifier
  max_iterations: 10        # Safety limit
  temperature: 0.7          # Creativity vs consistency

retrieval_worker:
  model: openai/gpt-4o-mini # Cost optimization
  max_iterations: 15
  temperature: 0.5          # More deterministic
```

**settings.py**: System-wide settings
- API keys and credentials
- Logging configuration
- Rate limits and timeouts
- Feature flags

### 5.2 LLM Integration (`src/core/llm.py`)

**LiteLLM Wrapper**: Model-agnostic LLM client

```python
def generate_response(prompt: Prompt) -> str:
    """
    Sends prompt to LLM and returns structured response.
    Uses LiteLLM for multi-provider support (OpenAI, Anthropic, etc.)
    """
    response = litellm.completion(
        model=os.getenv("MODEL", "gpt-4o"),
        messages=prompt.messages,
        tools=prompt.tools,
        temperature=0.7
    )
    
    # Parse function call from response
    tool_call = response.choices[0].message.tool_calls[0]
    return json.dumps({
        "tool": tool_call.function.name,
        "args": json.loads(tool_call.function.arguments)
    })
```

**Supported Providers** (via LiteLLM):
- OpenAI (GPT-4, GPT-4o, GPT-3.5)
- Anthropic (Claude 3 Opus/Sonnet/Haiku)
- Azure OpenAI
- Google Vertex AI
- Ollama (local models)

---

## 6. Execution Flow Example

**Scenario**: User asks "What is the population of Richmond and who lives there?"

### Step-by-Step Execution

```
================================================================================
MULTIAGENT SYSTEM - FILE MANAGEMENT AGENT DEMO
================================================================================

✓ Registered agent: FileManagementAgent
✓ Registered agent: RetrievalWorker
Task: What is the population of Richmond? and what is the name of the person 
      who lives in Richmond?

Agent is now working...
================================================================================

[Orchestrator] Iteration 1/13
[Orchestrator] Decision: run_retrieval_worker_agent
                         task: "Find the current population of Richmond"

  [RetrievalWorker] Iteration 1/13
  [RetrievalWorker] Decision: fetch_from_web
                               url: "https://en.wikipedia.org/wiki/Richmond,_Virginia"
  [RetrievalWorker] Result: Richmond is the capital city of Virginia...
  
  [RetrievalWorker] Iteration 2/13
  [RetrievalWorker] Decision: terminate
                               message: "The current population of Richmond, Virginia,
                                        as of the 2020 census, is 226,610..."
  [RetrievalWorker] Terminating

[Orchestrator] Result: Successfully retrieved population data from RetrievalWorker

[Orchestrator] Iteration 2/13
[Orchestrator] Decision: run_file_management_agent
                         task: "Find the name of any person currently living in Richmond"

  [FileManagementAgent] Iteration 1/13
  [FileManagementAgent] Decision: list_txt_files
  [FileManagementAgent] Result: ['richmond.txt']
  
  [FileManagementAgent] Iteration 2/13
  [FileManagementAgent] Decision: read_txt_file
                                   filename: "richmond.txt"
  [FileManagementAgent] Result: 'Peter Parker lives in Richmond. He is 25'
  
  [FileManagementAgent] Iteration 3/13
  [FileManagementAgent] Decision: terminate
                                   answer: "Peter Parker lives in Richmond."
  [FileManagementAgent] Terminating

[Orchestrator] Result: Successfully retrieved resident data from FileManagementAgent

[Orchestrator] Iteration 3/13
[Orchestrator] Decision: synthesize_results
                         web_results: "Population of Richmond is 226,610"
                         file_results: "Peter Parker lives in Richmond"
[Orchestrator] Result: Data synthesized and ready for final answer

[Orchestrator] Iteration 4/13
[Orchestrator] Decision: terminate
[Orchestrator] Terminating

================================================================================
AGENT EXECUTION COMPLETE
================================================================================

FINAL OUTPUT:
--------------------------------------------------------------------------------
Richmond, Virginia, has a population of 226,610 as of the 2020 census. 
The Richmond metropolitan area has over 1.37 million residents. 
Additionally, Peter Parker is mentioned as residing in Richmond.

[Orchestrator completed]
--------------------------------------------------------------------------------

Memory items created: 9
```

### Memory State at Each Stage

**After Orchestrator Iteration 1:**
```python
[
  {"type": "user", "content": "What is the population of Richmond? and what is the name of the person who lives in Richmond?"},
  {"type": "assistant", "content": '{"tool": "run_retrieval_worker_agent", "args": {"task": "Find the current population of Richmond, including any recent official estimates or data."}}'},
  {"type": "environment", "content": '{"success": true, "agent": "RetrievalWorker", "result": "The current population of Richmond, Virginia, as of the 2020 census, is 226,610..."}'}
]
```

**After Orchestrator Iteration 2:**
```python
[
  ...(previous items),
  {"type": "assistant", "content": '{"tool": "run_file_management_agent", "args": {"task": "Find the name of any person currently living in Richmond."}}'},
  {"type": "environment", "content": '{"success": true, "agent": "FileManagementAgent", "result": "Peter Parker lives in Richmond."}'}
]
```

**After Orchestrator Iteration 3:**
```python
[
  ...(previous items),
  {"type": "assistant", "content": '{"tool": "synthesize_results", "args": {"web_results": "The current population of Richmond, Virginia, as of the 2020 census, is 226,610...", "file_results": "Peter Parker lives in Richmond."}}'},
  {"type": "environment", "content": '{"web_information": "...", "file_information": "...", "synthesis": "Use both sources...", "status": "ready_for_final_answer"}'}
]
```

**After Orchestrator Iteration 4 (Final):**
```python
[
  ...(previous items),
  {"type": "assistant", "content": '{"tool": "terminate", "args": {"message": "Richmond, Virginia, has a population of 226,610 as of the 2020 census. The Richmond metropolitan area has over 1.37 million residents. Additionally, Peter Parker is mentioned as residing in Richmond."}}'},
  {"type": "environment", "content": '{"tool_executed": true, "result": "Richmond, Virginia, has a population of 226,610 as of the 2020 census... Peter Parker is mentioned as residing in Richmond. [Orchestrator completed]"}'}
]
```

---

## 7. Design Patterns & Best Practices

### 7.1 Factory Pattern (Agent Creation)

Each agent has a factory function that encapsulates instantiation logic:

```python
def create_orchestrator_agent() -> Agent:
    # Import actions to trigger decorator registration
    _ = orchestrator_actions
    
    # Create filtered action registry
    action_registry = PythonActionRegistry(
        tags=["orchestrator", "system", "orchestrator_delegation"]
    )
    action_registry.register_terminate_tool()
    
    # Instantiate agent with dependencies
    return Agent(
        name="Orchestrator",
        goals=ORCHESTRATOR_GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
```

**Benefits:**
- Encapsulates complexity
- Makes testing easier (can mock dependencies)
- Centralized configuration
- Clear separation of concerns

### 7.2 Registry Pattern (Tools & Agents)

Two registries enable loose coupling:

**Tool Registry**: Decorators register functions globally
**Agent Registry**: Orchestrators discover agents dynamically

**Advantages:**
- No hard-coded dependencies between agents
- Easy to add new agents without modifying orchestrators
- Supports dynamic agent composition
- Testable in isolation

### 7.3 Strategy Pattern (Agent Language)

The `AgentLanguage` interface allows swapping communication protocols:

```python
class AgentLanguage:
    def construct_prompt(...) -> Prompt: ...
    def parse_response(response: str) -> dict: ...

# Current implementation
class AgentFunctionCallingActionLanguage(AgentLanguage):
    # OpenAI function calling format

# Future implementations
class ClaudeToolUseLanguage(AgentLanguage):
    # Anthropic tool use format

class ReActLanguage(AgentLanguage):
    # ReAct prompting pattern
```

**Benefits:**
- Model-agnostic agent code
- Easy to migrate between LLM providers
- Can A/B test different prompting strategies
- Supports custom DSLs

### 7.4 Command Pattern (Actions)

Actions encapsulate operations as first-class objects:

```python
class Action:
    name: str
    function: Callable
    description: str
    parameters: Dict
    terminal: bool
    accepts_action_context: bool
    
    def execute(self, action_context=None, **args) -> Any:
        if self.accepts_action_context:
            return self.function(action_context=action_context, **args)
        return self.function(**args)
```

**Benefits:**
- Uniform interface for all operations
- Easy to log, audit, and replay actions
- Supports undo/redo (if implemented)
- Enables action scheduling and prioritization

### 7.5 Error Handling Strategy

**Graceful Degradation:**

1. **Action-Level**: Environment catches exceptions and returns structured errors
2. **Agent-Level**: LLM sees error in memory and can retry or adjust strategy
3. **System-Level**: Max iterations prevent infinite loops

**Example Error Flow:**

```python
# Action fails
def fetch_from_web(url):
    raise ValueError("URL not allowed")

# Environment catches and formats
{
  "tool_executed": False,
  "error": "URL not allowed",
  "traceback": "..."
}

# LLM sees error in next iteration and adapts
LLM Decision: "I need to use an allowed URL. Let me try without specifying a URL."
```

---

## 8. Extensibility & Customization

### 8.1 Adding a New Agent

**1. Define Goals** (`agents/my_agent/goals.py`):

```python
from core.language import Goal

MY_AGENT_GOALS = [
    Goal(
        priority=1,
        name="Primary Objective",
        description="Detailed description of what the agent must accomplish..."
    ),
    Goal(
        priority=2,
        name="Secondary Objective",
        description="Follow-up tasks..."
    )
]
```

**2. Create Tools** (`agents/my_agent/actions.py`):

```python
from tools.registry import register_tool
from core.action import ActionContext

@register_tool(tags=["my_agent_operations"])
def my_tool(action_context: ActionContext, param1: str, param2: int) -> str:
    """
    Tool description that the LLM will read.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    # Implementation
    return f"Processed {param1} with {param2}"

@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    return message
```

**3. Create Factory** (`agents/my_agent/agent.py`):

```python
from core.agent import Agent
from core.language import AgentFunctionCallingActionLanguage
from core.environment import Environment
from core.llm import generate_response
from tools.registry import PythonActionRegistry
from . import actions as my_actions
from .goals import MY_AGENT_GOALS

def create_my_agent():
    _ = my_actions  # Trigger decorator registration
    action_registry = PythonActionRegistry(tags=["my_agent_operations", "system"])
    action_registry.register_terminate_tool()
    
    return Agent(
        name="MyAgent",
        goals=MY_AGENT_GOALS,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
```

**4. Register and Use**:

```python
from agents.my_agent.agent import create_my_agent

my_agent = create_my_agent()
registry = AgentRegistry()
registry.register_agent("MyAgent", my_agent.run)

# Now callable from other agents
@register_tool(tags=["orchestrator_delegation"])
def run_my_agent(action_context: ActionContext, task: str) -> str:
    result = call_agent(action_context, "MyAgent", task)
    return json.dumps(result)
```

---

## 9. Production Considerations

### 9.1 Observability

**Logging Strategy:**

```python
# Enhanced agent with structured logging
import logging
import structlog

logger = structlog.get_logger()

class ObservableAgent(Agent):
    def run(self, user_input: str, **kwargs) -> Memory:
        logger.info("agent_started", 
                   agent_name=self.name,
                   user_input=user_input,
                   max_iterations=kwargs.get("max_iterations"))
        
        try:
            memory = super().run(user_input, **kwargs)
            logger.info("agent_completed",
                       agent_name=self.name,
                       memory_items=len(memory.items))
            return memory
        except Exception as e:
            logger.error("agent_failed",
                        agent_name=self.name,
                        error=str(e))
            raise
```

**Metrics to Track:**

- Agent execution time (per agent, per iteration)
- LLM token usage (input/output)
- Action execution counts (by action type)
- Error rates (by agent, by action)
- Cost per query (based on token usage)

### 9.2 Rate Limiting & Cost Control

**LLM Call Throttling:**

```python
# core/llm.py
from functools import wraps
import time

class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def acquire(self):
        now = time.time()
        # Remove calls older than 1 minute
        self.calls = [t for t in self.calls if now - t < 60]
        
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0])
            time.sleep(sleep_time)
        
        self.calls.append(time.time())

limiter = RateLimiter(calls_per_minute=60)

def generate_response(prompt: Prompt) -> str:
    limiter.acquire()
    return litellm.completion(...)
```

**Cost Tracking:**

```python
class CostTracker:
    COSTS = {
        "gpt-4o": {"input": 0.005, "output": 0.015},  # per 1k tokens
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006}
    }
    
    def __init__(self):
        self.total_cost = 0.0
        self.calls = []
    
    def track_call(self, model: str, input_tokens: int, output_tokens: int):
        cost = (
            input_tokens / 1000 * self.COSTS[model]["input"] +
            output_tokens / 1000 * self.COSTS[model]["output"]
        )
        self.total_cost += cost
        self.calls.append({
            "model": model,
            "cost": cost,
            "timestamp": time.time()
        })
```

### 9.3 Security Considerations

**1. Action Sandboxing:**

```python
class SandboxedEnvironment(Environment):
    ALLOWED_PATHS = ["/data", "/tmp"]
    
    def execute_action(self, action, args, action_context):
        # Validate file paths
        if "path" in args:
            if not any(args["path"].startswith(p) for p in self.ALLOWED_PATHS):
                return {
                    "tool_executed": False,
                    "error": "Access denied: path outside allowed directories"
                }
        
        # Execute with timeout
        import signal
        signal.alarm(30)  # 30 second timeout
        try:
            result = super().execute_action(action, args, action_context)
        finally:
            signal.alarm(0)
        
        return result
```

**2. Input Validation:**

```python
@register_tool(tags=["file_operations"])
def read_file(action_context: ActionContext, path: str) -> str:
    # Prevent path traversal
    if ".." in path or path.startswith("/"):
        raise ValueError("Invalid path")
    
    # Limit file size
    file_size = os.path.getsize(path)
    if file_size > 10 * 1024 * 1024:  # 10MB limit
        raise ValueError("File too large")
    
    with open(path, "r") as f:
        return f.read()
```

**3. LLM Prompt Injection Protection:**

```python
def sanitize_user_input(user_input: str) -> str:
    # Remove potential instruction injections
    dangerous_patterns = [
        r"ignore previous instructions",
        r"system:",
        r"assistant:",
        r"<\|im_start\|>",
    ]
    
    for pattern in dangerous_patterns:
        user_input = re.sub(pattern, "", user_input, flags=re.IGNORECASE)
    
    return user_input
```

### 9.4 Scalability

**Async Agent Execution:**

```python
import asyncio

class AsyncAgent(Agent):
    async def run_async(self, user_input: str, **kwargs) -> Memory:
        # Async version of GAME loop
        memory = Memory()
        action_context = ActionContext(...)
        
        for iteration in range(kwargs.get("max_iterations", 10)):
            prompt = self.construct_prompt(self.goals, memory, self.actions)
            
            # Async LLM call
            response = await self.generate_response_async(prompt)
            
            # Async action execution
            action, invocation = self.get_action(response)
            result = await self.environment.execute_action_async(
                action, invocation["args"], action_context
            )
            
            self.update_memory(memory, response, result)
            
            if self.should_terminate(response):
                break
        
        return memory

# Run multiple agents in parallel
async def parallel_orchestration(tasks):
    agents = [create_retrieval_worker_agent() for _ in tasks]
    results = await asyncio.gather(*[
        agent.run_async(task) for agent, task in zip(agents, tasks)
    ])
    return results
```

**Distributed Agent Registry:**

```python
# Use Redis for distributed agent registry
import redis

class DistributedAgentRegistry:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    def register_agent(self, name: str, agent_endpoint: str):
        """Register agent's API endpoint"""
        self.redis.set(f"agent:{name}", agent_endpoint)
    
    async def run_agent(self, name: str, task: str) -> dict:
        """Call remote agent via HTTP"""
        endpoint = self.redis.get(f"agent:{name}")
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json={"task": task}) as resp:
                return await resp.json()
```

---

## 10. Conclusion

This multi-agent system provides a robust, extensible foundation for building collaborative AI applications. The GAME loop architecture ensures agents are goal-oriented, context-aware, and observable, while the modular design enables rapid prototyping of new agent types and tool categories.

**Key Takeaways:**

✅ **Production-Ready**: Comprehensive error handling, rate limiting, and security features  
✅ **Extensible**: Add new agents, tools, and protocols with minimal code changes  
✅ **Observable**: Structured memory and logging enable debugging and optimization  
✅ **Model-Agnostic**: Abstract language protocols support any LLM provider  
✅ **Scalable**: Async execution and distributed registries support high-throughput workloads  

**Getting Started Checklist:**

1. Review core components (`src/core/`)
2. Study existing agents (`src/agents/`)
3. Experiment with tool creation (`@register_tool`)
4. Build a custom agent following the factory pattern
5. Extend the orchestrator for your use case

**Resources:**

- Example implementations: `examples/sample_project/`
- Test suite: `tests/`
- Configuration: `src/config/agents.yaml`
- Architecture diagrams: `docs/architecture_structure.md`

For questions or contributions, refer to the project's GitHub repository and contribution guidelines.

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Maintained By**: AI Agent Framework Team

