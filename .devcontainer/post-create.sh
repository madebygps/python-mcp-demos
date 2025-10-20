#!/usr/bin/env bash
set -euo pipefail

echo "📦 Syncing Python dependencies (uv)..."
uv sync -q

# Append HOST export only once.
if ! grep -q 'export HOST=0.0.0.0' ~/.bashrc; then
	echo 'export HOST=0.0.0.0' >> ~/.bashrc
fi
