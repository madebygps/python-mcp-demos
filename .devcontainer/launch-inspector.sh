#!/usr/bin/env bash
set -euo pipefail

# Get the Codespaces URL base (if running in Codespaces)
if [ -n "${CODESPACE_NAME:-}" ]; then
    CODESPACE_URL="https://${CODESPACE_NAME}-6274.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    echo "🚀 Launching MCP Inspector for GitHub Codespaces..."
    echo "   UI Origin: $CODESPACE_URL"
    echo ""
    echo "📝 Inspector Configuration:"
    echo "   Proxy Address: https://${CODESPACE_NAME}-6277.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    echo "   Command: uv"
    echo "   Arguments: run main.py"
    echo ""
    echo "⚠️  Make sure port 6277 is set to PUBLIC in the Ports tab!"
    echo ""
    
    DANGEROUSLY_OMIT_AUTH=true \
    ALLOWED_ORIGINS="$CODESPACE_URL" \
    npx -y @modelcontextprotocol/inspector
else
    # Running locally
    echo "🚀 Launching MCP Inspector locally..."
    DANGEROUSLY_OMIT_AUTH=true npx -y @modelcontextprotocol/inspector
fi
