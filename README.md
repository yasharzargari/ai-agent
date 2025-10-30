.
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── llm/
│   ├── __init__.py
│   └── litellm_provider.py
├── core/
│   ├── __init__.py
│   ├── action.py
│   ├── agent.py
│   ├── agent_language.py
│   ├── errors.py
│   ├── goal.py
│   ├── memory.py
│   ├── prompt.py
│   ├── schema.py
│   └── utils.py
├── memory/
│   ├── __init__.py
│   └── vector_store.py
├── goals/
│   ├── __init__.py
│   ├── planning.py
│   ├── retrieval.py
│   └── synthesis.py
├── actions/
│   ├── __init__.py
│   ├── file_actions.py
│   └── web_actions.py
├── agents/
│   ├── __init__.py
│   ├── planner_router.py
│   ├── retriever_aggregator.py
│   └── synthesizer_verifier.py
├── environment/
│   ├── __init__.py
│   └── base_env.py
├── orchestration/
│   ├── __init__.py
│   ├── parallel.py
│   └── pipeline.py
└── tests/
