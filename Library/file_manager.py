from pathlib import Path
import json
import time


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

def save_params(params: dict, config_path: str | Path) -> None:
    path = Path(config_path).expanduser().resolve()

    if path.exists() and not path.is_file():
        raise ValueError(f"Config path is not a file: {path}")

    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(params, f, indent=2)
    except Exception as e:
        raise IOError(f"Failed to save config to {path}: {e}") from e
    
def init_run_logging(project_root: Path, params: dict):

    run_name = params.get("run_name", f"run_{int(time.time())}")
    run_dir = project_root / "log" / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    metrics = {
        "run_name": run_name,
        "episodes": 0,
        "goals": 0,
        "best_avg_goal_rate": 0.0,
        "epsilon": None,
        "learning_rate": None,
    }

    with (run_dir / "config.json").open("w", encoding="utf-8") as f:
        json.dump(params, f, indent=2)

    return run_dir, metrics


def save_metrics(run_dir: Path | None, metrics: dict | None):
    if run_dir is None or metrics is None:
        return

    with (run_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)