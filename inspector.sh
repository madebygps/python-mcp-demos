#!/usr/bin/env bash
echo "🚀 Starting MCP Inspector with your Python server..."
echo "📍 Inspector UI will be available at: http://localhost:6274"
echo "🔑 Copy the session token from the output below"
echo ""

# Start inspector with your server
npx @modelcontextprotocol/inspector .venv/bin/python -u main.py
