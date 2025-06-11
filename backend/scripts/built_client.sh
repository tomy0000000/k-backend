#!/usr/bin/env bash
set -euo pipefail
# Usage: scripts/built_client.sh

TMP_FILE="$(mktemp)"

# Download openapi.json
wget 'http://localhost:8000/openapi.json' -O "${TMP_FILE}"

# Remove tmp file on exit
trap 'rm -f "${TMP_FILE}"' EXIT

# Convert openapi.json
poetry run scripts/convert_openapi.py "${TMP_FILE}"

# Generate client
cd "../frontend"
pnpm run generate-client --input "${TMP_FILE}"
