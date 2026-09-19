#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 is required."
    exit 1
fi

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
MAJOR="${PYTHON_VERSION%%.*}"
MINOR="${PYTHON_VERSION#*.}"
if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]; }; then
    echo "ERROR: Python 3.10+ is required (found $PYTHON_VERSION)."
    exit 1
fi

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete. Run: ./mac/run.sh"
