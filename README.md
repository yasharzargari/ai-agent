# Multiagent Chatbot System

A flexible multiagent system with specialized agents for intelligent query processing and response synthesis.

## Architecture

This system uses a multi-agent architecture with:

1. **Orchestrator/Router**: Analyzes user requests, sets scope and time windows, and dispatches queries to appropriate workers
2. **Retrieval Worker**: Executes source-specific tools in parallel to fetch data from files, web, or other sources
3. **Synthesizer/Reporter**: Deduplicates and clusters information by topic, then generates comprehensive summaries
4. **File Management Agent**: Demonstrates the core agent framework by reading and analyzing project files

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
```

## Quick Start

```bash
# Run the file management agent demo
python main.py

# Or run the full chatbot pipeline
python -m src.multiagent.runtime.run_chatbot_pipeline

# Or use the Makefile
make run-file-agent
make run-chatbot
```

## Project Structure

```
multiagent/
├── main.py            # Main entry point for file management agent
├── src/multiagent/
│   ├── core/          # Core agent framework (GAME loop)
│   ├── agents/        # Specialized agent implementations
│   ├── orchestrators/ # Coordination logic
│   ├── tools/         # Available tools for agents
│   └── runtime/       # Entry points
├── tests/             # Test suite
├── docs/              # Documentation
└── examples/          # Example projects
```

## Configuration

Edit `src/multiagent/config/agents.yaml` to customize agent behaviors and `config.py` for system-wide settings.

## Creating New Agents

1. Define goals in `agents/your_agent/goals.py`
2. Create agent factory in `agents/your_agent/agent.py`
3. Register tools with `@register_tool` decorator
4. Run with the shared memory system

## License

MIT License
