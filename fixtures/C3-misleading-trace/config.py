import json
from pathlib import Path


def load_config(path="settings.json"):
    """Load server configuration from a JSON file."""
    raw = json.loads(Path(path).read_text())
    return {
        "host": raw.get("host", "0.0.0.0"),
        "port": raw.get("port", 8000),
        "workers": raw.get("workers", 1),
    }
