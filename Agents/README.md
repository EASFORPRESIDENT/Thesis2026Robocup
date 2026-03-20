# Agents playing HFO
## Python environment for VS Code

From `Thesis2026Robocup/`:

```
sudo apt install python3-venv -y
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install ./HFO
```

In VS Code, in `Thesis2026Robocup/` folder:
* Press ```Ctrl+Shift+P```
* Run Python: Select Interpreter
* Choose `Thesis2026Robocup/.venv/bin/python`

## Run Dummy agent
In `Thesis2026Robocup/`, run:
```
source .venv/bin/activate
python Agents/DummyAgent/DummyAgent.py
```
