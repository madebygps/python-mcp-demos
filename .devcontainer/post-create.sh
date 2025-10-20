#!/usr/bin/env bash
set -e

# Install Python dependencies
echo "📦 Installing Python dependencies..."
uv sync > /dev/null 2>&1

# Install MCP Inspector globally (no prompts)
echo "🔧 Installing MCP Inspector..."
npm install -g @modelcontextprotocol/inspector@latest > /dev/null 2>&1

# Set HOST variable for Inspector
echo 'export HOST=0.0.0.0' >> ~/.bashrc

# Create convenient launch script with -y flag
cat > inspector.sh << 'EOF'
#!/usr/bin/env bash
echo "🚀 Starting MCP Inspector with your Python server..."
echo "📍 Inspector UI will be available at: http://localhost:6274"
echo "🔑 Copy the session token from the output below"
echo ""

# Ensure HOST is set for network binding
export HOST=0.0.0.0

# Start inspector with your server (-y flag auto-confirms)
npx -y @modelcontextprotocol/inspector .venv/bin/python -u main.py
EOF
chmod +x inspector.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 To use MCP Inspector:"
echo "   Run: ./inspector.sh"
echo ""
echo "🎯 To use with Copilot Chat:"
echo "   Open Copilot Chat → Agent mode → Tools"
echo ""