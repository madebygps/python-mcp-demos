#!/usr/bin/env bash
set -e

# Install Python dependencies
uv sync > /dev/null 2>&1

# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector@latest > /dev/null 2>&1

echo "✓ Terminal ready to use"