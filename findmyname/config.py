"""Loading of the central config.json file."""

import json
from pathlib import Path

from . import REPO_ROOT

CONFIG_PATH = REPO_ROOT / "config.json"


def load_config(tool_name=None, config_path=None):
    """Load the configuration for one tool, or the whole config."""
    path = Path(config_path) if config_path else CONFIG_PATH

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if tool_name is None:
        return config

    return dict(config.get("tools", {}).get(tool_name, {}))
