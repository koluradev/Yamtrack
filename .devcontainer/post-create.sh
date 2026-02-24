#!/usr/bin/env bash
set -e

echo "🔧 Post-create setup startet..."

# Python deps
echo "🐍 Installiere Python requirements..."
python -m pip install -U pip
pip install -r requirements-dev.txt
pre-commit install

# Node check
if ! command -v node >/dev/null 2>&1; then
  echo "❌ Node ist nicht installiert – devcontainer Feature fehlt"
  exit 1
fi

echo "✅ Post-create setup fertig."