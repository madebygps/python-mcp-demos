# Python MCP Demos

This repository implements a **minimal MCP expense tracker**.

The Model Context Protocol (MCP) is an open standard that enables LLMs to connect to external data sources and tools.

## Getting Started

### Environment Setup

Choose ONE of the following approaches depending on where you're running this:

#### 1. GitHub Codespaces (zero manual setup)
Codespaces will automatically:
- Build the dev container defined in `.devcontainer/devcontainer.json`
- Install dependencies via `uv sync` (configured as `postCreateCommand`)
- Provide Python extensions

You can start using the MCP server immediately; no extra steps required.

#### 2. Local VS Code Dev Container
Requirements: Docker + VS Code + Dev Containers extension.

Steps:
1. Open the folder in VS Code.
2. When prompted, reopen in container (or run: “Dev Containers: Reopen in Container”).
3. Wait for container build. 

#### 3. Local Machine Without a Dev Container
If you prefer a plain local environment:

Primary (fast & reproducible): **uv**
```bash
uv sync
```

Fallback (if uv unavailable): Standard venv + pip
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```


### Running the MCP Server

You do NOT need to run anything manually if you're using a compatible MCP client (e.g. VS Code, Claude Desktop). The repository includes a configuration file at `.vscode/mcp.json`:

```json
{
   "servers": {
      "expenses": {
         "type": "stdio",
         "command": "uv",
         "args": ["run", "main.py"]
      }
   },
   "inputs": []
}
```

The client will automatically start the `expenses` server via `uv run main.py` using stdio when it loads this workspace.

#### VS Code Usage

1. Open the file: `.vscode/mcp.json` in the editor.
2. Click on "Start" / ▶ button shown in the MCP view.
3. Confirm the server appears in the MCP panel with tools/resources listed.

##### GitHub Copilot Chat Integration
To interact with the server through Copilot:
1. Open the GitHub Copilot Chat panel (bottom right, or via Command Palette: `GitHub Copilot: Focus Chat`).
2. Click the **Tools** (wrench) icon in the chat sidebar.
3. Ensure the `expenses` MCP server is enabled/selected in the list of available tools.
4. Ask Copilot to invoke the tool, e.g.:
   - "Use add_expense to record a $12 lunch today paid with visa"
   - "Read the expenses resource"
5. If the server isn't listed, ensure it started successfully (see steps above) and reload the window: `Developer: Reload Window`.
6. You can refine prompts using the `create_expense_prompt` by asking Copilot to call that prompt first.

To stop it, use `MCP: Stop Server` or the stop button in the MCP panel.

#### MCP Inspector (Optional Visual & Protocol Testing)

The MCP Inspector is a browser-based visual testing & debugging tool for MCP servers. This repo’s dev container installs it globally during creation. It does NOT auto-launch; you start it when you need it.

#### 1. Launch Inspector (UI only)
```bash
npx @modelcontextprotocol/inspector
```
By default it picks its standard client/proxy ports (e.g. 6274 / 6277). You’ll see them in the output.

#### 2. Launch Wrapping the Expenses Server
```bash
npx @modelcontextprotocol/inspector -- uv run main.py
```
The `--` separates inspector options/env injections from the server command.

#### 3. Custom Ports
```bash
CLIENT_PORT=8080 SERVER_PORT=9000 npx @modelcontextprotocol/inspector -- uv run main.py
```

#### 4. Pass Environment Variables to Server
Use one or more `-e KEY=VALUE` tokens before `--`:
```bash
npx @modelcontextprotocol/inspector -e EXPENSES_FILE=/tmp/expenses.csv -- uv run main.py
```

#### 5. Wrap Other Servers
```bash
npx @modelcontextprotocol/inspector -- npx @modelcontextprotocol/server-filesystem /path/to/dir
npx @modelcontextprotocol/inspector -- uvx mcp-server-git --repository ~/code/mcp/servers.git
```

#### 6. UI Features At A Glance
* Resources: list & view content (`expenses.csv`).
* Tools: execute `add_expense` with JSON inputs.
* Prompts: explore `create_expense_prompt` argument handling.
* Notifications: watch capability negotiation + server logs.

#### 7. Edge Case Testing Ideas
* Omit required fields (e.g. `amount`).
* Invalid payment method (`bitcoin`).
* Large numeric values for stress.
* Rapid concurrent tool calls.

#### 8. Quick Tips
* Restart after changes: just rerun the same command.
* Compare results with VS Code MCP panel.
* Use custom ports if default clashes with other processes.
* Keep proxy port private—avoid exposing to untrusted networks.

#### 9. Next Improvements (Optional)
* Add analytics MCP tools (monthly totals / category breakdown).
* CI health check invoking handshake + sample tool call.
* Configurable CSV path via env var.
* Structured error contract & tests.

---



## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.