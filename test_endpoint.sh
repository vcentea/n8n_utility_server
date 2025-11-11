#!/usr/bin/env bash
set -euo pipefail

echo "Testing PDF-to-Images Endpoint"
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
API_KEY="${API_KEY:-}"

if [[ -n "${API_KEY}" ]]; then
  echo "Using API_KEY from .env file"
else
  read -r -p "Enter your API_KEY: " API_KEY
fi

read -r -p "Enter path to PDF file: " PDF_FILE

if [[ ! -f "${PDF_FILE}" ]]; then
  echo "ERROR: File not found: ${PDF_FILE}"
  exit 1
fi

echo
echo "Sending request to http://localhost:${PORT}/api/v1/pdf-to-images..."
echo

curl -X POST "http://localhost:${PORT}/api/v1/pdf-to-images" \
  -H "x-api-key: ${API_KEY}" \
  -F "file=@${PDF_FILE};type=application/pdf"

echo

