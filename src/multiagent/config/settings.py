"""Settings management"""

DEFAULT_SETTINGS = {
    "max_iterations": 50,
    "default_model": "openai/gpt-4o",
    "max_tokens": 1024,
    "temperature": 0.7,
}


def get_setting(key: str, default=None):
    """Get a configuration setting"""
    return DEFAULT_SETTINGS.get(key, default)
