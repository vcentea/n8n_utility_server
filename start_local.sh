#!/usr/bin/env bash
set -euo pipefail

echo "Starting Utility Service Platform..."
echo

if [[ ! -f ".env" ]]; then
  echo "ERROR: .env file not found!"
  echo "Please copy .env.example to .env and configure it."
  exit 1
fi

set -a
# shellcheck source=/dev/null
. ./.env
set +a

PORT="${PORT:-2277}"

if [[ -n "${POPPLER_PATH:-}" ]]; then
  if [[ -d "${POPPLER_PATH}" ]]; then
    echo "Adding POPPLER_PATH to PATH: ${POPPLER_PATH}"
    export PATH="${POPPLER_PATH}:${PATH}"
  else
    echo "Warning: POPPLER_PATH is set but directory does not exist: ${POPPLER_PATH}"
  fi
fi

PYTHON_BIN="python3"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

if [[ ! -d "venv" ]]; then
  echo "Creating virtual environment..."
  "${PYTHON_BIN}" -m venv venv
fi

# shellcheck source=/dev/null
. venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "Starting server on http://localhost:${PORT}"
echo "API Documentation: http://localhost:${PORT}/docs"
echo
echo "Press Ctrl+C to stop the server"
echo

uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" --reload

