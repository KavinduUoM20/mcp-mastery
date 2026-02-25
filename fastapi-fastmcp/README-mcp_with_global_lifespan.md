# mcp_with_global_lifespan.py — FastAPI + FastMCP with custom lifespan

This module extends the minimal setup by adding **custom application lifespan**: your own startup and shutdown logic runs together with FastMCP’s lifespan, so you can initialize and clean up shared state (e.g. greeting functions, config) used by both REST and MCP.

## What it does

- **Same as main.py**: One app serving REST and MCP at `/` and `/mcp`, with `add` and `multiply` MCP tools.
- **Extra behavior**:
  - **Startup**: Runs a greeting (e.g. “Hello! App”), and stores the greeting function in shared state (`user_profile`) so both the MCP tool and the REST endpoint can use it.
  - **Shutdown**: Runs a goodbye greeting (e.g. “Goodbye App!”) and a final log message.
  - **Unified lifespan**: A single `global_lifespan` runs your FastAPI lifespan first, then FastMCP’s lifespan, so both run in one place.

- **Additional MCP tool**: `greet_user(name)` — uses the stored greeting function to return a greeting string.
- **Additional REST route**: `GET /greet_user?name=...` — same greeting, returned as JSON `{"message": "Hello! …"}`.

## Why “global” lifespan?

- **FastAPI** has its own lifespan (e.g. `fastapi_lifespan`: startup greeting, store function, shutdown goodbye).
- **FastMCP** has its own lifespan (internal setup/teardown).
- **global_lifespan** composes them: it enters your FastAPI lifespan, then FastMCP’s lifespan, and yields. On shutdown it exits in reverse order. So you get one place to define “app start” and “app stop” while still using FastMCP’s lifecycle.

## How it’s structured

1. **Greeting helpers**: `start_greeting(name)` and `end_greeting(name)` for startup/shutdown messages; `start_greeting` is also stored and used for `greet_user`.
2. **fastapi_lifespan**: Sets `user_profile["name"] = start_greeting`, runs `start_greeting("App")` on startup, and `end_greeting("App")` on shutdown.
3. **global_lifespan**: `async with fastapi_lifespan(app):` then `async with mcp_app.lifespan(app):`, then `yield`.
4. The **combined app** uses `lifespan=global_lifespan` so this single lifespan runs for the whole app.

## How to run

Point your process at this module’s combined app, e.g. in `rav.yaml`:

```yaml
# example: dev script for this file
cmd: uvicorn mcp_with_global_lifespan:app --reload --port 8123
```

(with `working_dir: src`). Then:

- **REST**: `http://127.0.0.1:8123/`, `http://127.0.0.1:8123/greet_user?name=...`
- **MCP**: `http://127.0.0.1:8123/mcp` (tools: `add`, `multiply`, `greet_user`)

Use this file when you need **shared state or custom startup/shutdown** that both REST and MCP should use; use `main.py` when you only need the minimal combined app with no custom lifespan.
