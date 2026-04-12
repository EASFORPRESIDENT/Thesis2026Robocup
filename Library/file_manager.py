from pathlib import Path
import json


def load_params(config_path: str | Path) -> dict:
    path = Path(config_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Config path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            params = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file {path}: {e}") from e

    if not isinstance(params, dict):
        raise ValueError(f"Top-level JSON object must be a dictionary, got {type(params).__name__}")

    return params