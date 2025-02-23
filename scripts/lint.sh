#!/usr/bin/env bash
set -euo pipefail
# Usage: poetry run scripts/lint.sh

mypy k_backend
ruff check k_backend
ruff format k_backend --check
