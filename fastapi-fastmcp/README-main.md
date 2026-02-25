# main.py — FastAPI + FastMCP (minimal)

This module is the **minimal setup** for serving both a FastAPI web app and an MCP (Model Context Protocol) server in one process.

## What it does

- **Single ASGI app** that combines:
  - **REST API**: FastAPI routes (e.g. `GET /` returning a JSON message).
  - **MCP over HTTP**: FastMCP tools exposed at `/mcp` for AI clients (e.g. Cursor, GPT) to call.

- **MCP tools** (callable via the `/mcp` endpoint):
  - `add(a, b)` — returns `(a + b) * 1000`.
  - `multiply(a, b)` — returns `(a * b) * 1000`.

- **Lifespan**: Uses FastMCP’s lifespan only (no custom startup/shutdown logic).

## How it’s structured

1. A base **FastAPI** app (`api`) and a **FastMCP** app are created and wired with `from_fastapi(api)`.
2. The MCP HTTP app is created with `mcp.http_app(path="/mcp")`.
3. A single **combined** FastAPI app (`app`) is built with:
   - Routes from both `mcp_app` and `api`.
   - Lifespan from `mcp_app`.

## How to run

From the project root:

```bash
rav run dev
```

This runs `uvicorn main:app --reload --port 8123` from the `src` directory, so:

- **REST**: `http://127.0.0.1:8123/`
- **MCP**: `http://127.0.0.1:8123/mcp`

Use `main:app` (the combined app), not `main:api`, so that both the REST and MCP routes are served.
