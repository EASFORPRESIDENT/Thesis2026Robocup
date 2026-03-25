#!/usr/bin/env bash

# Usage:
# ./run_sim.sh <Nr_Offensive_agents> <Nr_Defensive_agents>
#
# Example:
# ./run_sim.sh 2 1

set -e

# Check arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <Nr_Offensive_agents> <Nr_Defensive_agents>"
    exit 1
fi

NR_OFFENSIVE_AGENTS="$1"
NR_DEFENSIVE_AGENTS="$2"


# Basic validation: must be integers
if ! [[ "$NR_OFFENSIVE_AGENTS" =~ ^[0-9]+$ ]] || ! [[ "$NR_DEFENSIVE_AGENTS" =~ ^[0-9]+$ ]]; then
    echo "Error: both arguments must be non-negative integers."
    exit 1
fi

# Change this to your project folder if needed
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Project directory: $PROJECT_DIR"
echo "Starting HFO with $NR_OFFENSIVE_AGENTS offensive agents and $NR_DEFENSIVE_AGENTS defensive NPCs"

# Start HFO server in its own terminal
gnome-terminal -- bash -c "
cd '$PROJECT_DIR' || exit 1
source .venv/bin/activate
HFO/./bin/HFO --offense-agents=$NR_OFFENSIVE_AGENTS --defense-npcs=$NR_DEFENSIVE_AGENTS --no-sync
"

# Optional: wait a bit so HFO has time to start
sleep 2


# Start one DummyAgent terminal per offensive agent
for ((i=1; i<=NR_OFFENSIVE_AGENTS; i++)); do
    gnome-terminal -- bash -c "
    cd '$PROJECT_DIR' || exit 1
    source .venv/bin/activate
    echo 'Starting DummyAgent $i/$NR_OFFENSIVE_AGENTS'
    python Agents/DummyAgent/DummyAgent.py
    "
done

