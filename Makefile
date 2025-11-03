.PHONY: install test run-file-agent run-chatbot clean help

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src/multiagent

run-file-agent:
	python main.py

run-chatbot:
	python -m src.multiagent.runtime.run_chatbot_pipeline

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Run tests"
	@echo "  make run-file-agent - Run the file management agent demo"
	@echo "  make run-chatbot    - Run the chatbot pipeline"
	@echo "  make clean          - Clean build artifacts"
