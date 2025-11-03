"""Module B - Utilities"""


def format_output(data):
    """Format data for output"""
    return ", ".join(map(str, data))


def load_config(filepath):
    """Load configuration from file"""
    # Placeholder
    return {"setting": "value"}


def save_results(data, filepath):
    """Save results to file"""
    with open(filepath, "w") as f:
        f.write(str(data))
