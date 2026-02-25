# first-mcp

Weather MCP server (stdio transport).

## Run

### 1. Install and build

```bash
cd first-mcp
npm install
npm run build
```

### 2. Run the server

The server uses **stdio** (stdin/stdout), so it’s intended to be started by a host (e.g. Cursor), not for interactive use in a terminal.

- **Run the built script directly:**
  ```bash
  node build/index.js
  ```
- **Or use the package binary** (after `npm install`):
  ```bash
  npx weather
  ```

When run, it listens on stdio and waits for MCP messages.

### 3. Use from Cursor

1. Add the server in Cursor’s MCP settings (e.g. `.cursor/mcp.json` or Cursor Settings → MCP).
2. Set the **command** to run this server, for example:
   - `node` with args: path to `first-mcp/build/index.js`, or
   - `npx` with args: `weather` and `cwd`: path to `first-mcp`.

### 4. Inspect with MCP Inspector

To test the server with the official inspector:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

(or configure the inspector to use the same command in its UI).
