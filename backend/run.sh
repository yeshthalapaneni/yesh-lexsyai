#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate || true
exec uvicorn app.main:app --host ${BACKEND_HOST:-0.0.0.0} --port ${BACKEND_PORT:-8000}
