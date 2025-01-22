#!/usr/bin/env bash
set -euo pipefail

coverage run -m pytest
coverage report
coverage xml
coverage html
