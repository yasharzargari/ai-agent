import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "50"))

# Paths
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "./workspace")
LOGS_DIR = os.getenv("LOGS_DIR", "./logs")

# API Keys (loaded from .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
