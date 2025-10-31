#!/usr/bin/env bash
set -euo pipefail

# Defaults (can be overridden by environment)
APP_DIR=${APP_DIR:-/srv/gestao_contratos}
VENV_DIR=${VENV_DIR:-$APP_DIR/venv}

echo "[deploy] Using APP_DIR=$APP_DIR"
echo "[deploy] Using VENV_DIR=$VENV_DIR"

cd "$APP_DIR"

"$VENV_DIR/bin/python" manage.py migrate --noinput
"$VENV_DIR/bin/python" manage.py collectstatic --noinput

echo "[deploy] Migrations and collectstatic completed."