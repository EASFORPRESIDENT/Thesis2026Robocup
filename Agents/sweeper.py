import os
import signal
import subprocess
import sys
import random
from pathlib import Path
from collections.abc import Sequence
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Library.file_manager import load_params, save_params

RUN_CONFIG = PROJECT_ROOT / "configs" / "trial_config.json"
HFO_SCRIPT = PROJECT_ROOT / "HFO" / "bin" / "HFO"

def print_params(params: dict):
    print("Current parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")

def cleanup_hfo_processes():
    subprocess.run(["killall", "-9", "rcssserver"], check=False)
    subprocess.run(["pkill", "-f", "/HFO/bin/HFO"], check=False)
    time.sleep(1)

def main():
    sweep_config = load_params(PROJECT_ROOT / "configs" / "sweep.json")
    params = sweep_config["parameters"]
    print(f"Starting hyperparameter sweep with {sweep_config['num_trials']} trials...")
    
    num_trials = sweep_config.get("num_trials", 10)
    for trial in range(num_trials):
        trial_params = {
            "n_O_agents":                   random.choice(params["n_O_agents"]) if isinstance(params["n_O_agents"], Sequence) else params["n_O_agents"],
            "n_D_agents":                   random.choice(params["n_D_agents"]) if isinstance(params["n_D_agents"], Sequence) else params["n_D_agents"],
            "training":                     random.choice(params["training"]) if isinstance(params["training"], Sequence) else params["training"],
            "logging":                      random.choice(params["logging"]) if isinstance(params["logging"], Sequence) else params["logging"],
            "plotting":                     random.choice(params["plotting"]) if isinstance(params["plotting"], Sequence) else params["plotting"],
            "duration":                     random.choice(params["duration"]) if isinstance(params["duration"], Sequence) else params["duration"],
            "learning_rate":                random.choice(params["learning_rate"]) if isinstance(params["learning_rate"], Sequence) else params["learning_rate"],
            "min_learning_rate":            random.choice(params["min_learning_rate"]) if isinstance(params["min_learning_rate"], Sequence) else params["min_learning_rate"],
            "learning_rate_decay":          random.choice(params["learning_rate_decay"]) if isinstance(params["learning_rate_decay"], Sequence) else params["learning_rate_decay"],
            "epsilon_start":                random.choice(params["epsilon_start"]) if isinstance(params["epsilon_start"], Sequence) else params["epsilon_start"],
            "epsilon_min":                  random.choice(params["epsilon_min"]) if isinstance(params["epsilon_min"], Sequence) else params["epsilon_min"],
            "epsilon_decay":                random.choice(params["epsilon_decay"]) if isinstance(params["epsilon_decay"], Sequence) else params["epsilon_decay"],
            "number_of_samples":            random.choice(params["number_of_samples"]) if isinstance(params["number_of_samples"], Sequence) else params["number_of_samples"],
            "burn_in_steps":                random.choice(params["burn_in_steps"]) if isinstance(params["burn_in_steps"], Sequence) else params["burn_in_steps"],
            "training_steps":               random.choice(params["training_steps"]) if isinstance(params["training_steps"], Sequence) else params["training_steps"],
            "bootstrap_steps":              random.choice(params["bootstrap_steps"]) if isinstance(params["bootstrap_steps"], Sequence) else params["bootstrap_steps"],
            "discount_factor":              random.choice(params["discount_factor"]) if isinstance(params["discount_factor"], Sequence) else params["discount_factor"],
            "target_update_interval":       random.choice(params["target_update_interval"]) if isinstance(params["target_update_interval"], Sequence) else params["target_update_interval"],
            "max_grad_norm":                random.choice(params["max_grad_norm"]) if isinstance(params["max_grad_norm"], Sequence) else params["max_grad_norm"],
            "duplicate_positive_episodes":  random.choice(params["duplicate_positive_episodes"]) if isinstance(params["duplicate_positive_episodes"], Sequence) else params["duplicate_positive_episodes"],
            "max_duplication":              random.choice(params["max_duplication"]) if isinstance(params["max_duplication"], Sequence) else params["max_duplication"],
            "duplication_scale_factor":     random.choice(params["duplication_scale_factor"]) if isinstance(params["duplication_scale_factor"], Sequence) else params["duplication_scale_factor"]
        }
        save_params(trial_params, RUN_CONFIG)
        print(f"\n=== Starting trial {trial + 1}/{num_trials} ===")
        print_params(trial_params)

        hfo_process = None
        try:
            cleanup_hfo_processes()

            cmd = [
                "./bin/HFO",
                f"--offense-agents={trial_params['n_O_agents']}",
                f"--defense-npcs={trial_params['n_D_agents']}",
                "--port=6000",
                "--headless",
                "--fullstate"
            ]

            hfo_process = subprocess.Popen(
                cmd,
                cwd=PROJECT_ROOT / "HFO",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )

            time.sleep(2)

            if hfo_process.poll() is not None:
                stdout, stderr = hfo_process.communicate()
                print("HFO failed to start.")
                print("stdout:")
                print(stdout)
                print("stderr:")
                print(stderr)
                raise RuntimeError("HFO did not stay running")

            subprocess.run(
                [sys.executable, "Team.py", "--config", str(RUN_CONFIG)],
                cwd=PROJECT_ROOT / "Agents",
                check=True
            )

            print(f"Trial {trial + 1} completed successfully.")

        finally:
            if hfo_process is not None and hfo_process.poll() is None:
                try:
                    os.killpg(hfo_process.pid, signal.SIGTERM)
                    hfo_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(hfo_process.pid, signal.SIGKILL)

            cleanup_hfo_processes()

if __name__ == "__main__":
    main()
