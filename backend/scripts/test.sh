#!/usr/bin/env bash
set -euo pipefail
# Usage: poetry run scripts/test.sh

export POSTGRES_PASSWORD=dummy
pytest
