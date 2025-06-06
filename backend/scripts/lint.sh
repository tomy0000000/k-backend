#!/usr/bin/env bash
set -euo pipefail
# Usage: poetry run scripts/lint.sh

mypy kayman
ruff check kayman
ruff format kayman --check
