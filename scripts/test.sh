#!/usr/bin/env bash
set -euo pipefail

export POSTGRES_PASSWORD=dummy
pytest
