# AiDocs MCP

FastAPI + FastMCP server that lets you **upload documents** and **save them** under the `outputs/` directory.

## Setup

```bash
cd aidocs-mcp
python -m venv env
.\env\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Run

```bash
rav run dev
```

Server runs at **http://127.0.0.1:8123**.

## What it does

- **REST**
  - `GET /` — info message
  - `POST /upload` — upload a file (multipart); saved to `outputs/<filename>`

- **MCP** (at `/mcp`)
  - `save_document(filename, content)` — save a text document to `outputs/<filename>`
  - `list_saved_documents()` — list filenames in `outputs/`

## Example: upload via REST

```bash
curl -X POST -F "file=@/path/to/doc.pdf" http://127.0.0.1:8123/upload
```

## Example: save via MCP tool

From an MCP client (e.g. Cursor), call the tool:

- `save_document(filename="note.txt", content="Hello world")`
- `list_saved_documents()`

## Using the MCP Inspector

**Yes — you can use the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) with this project.**

This app exposes MCP over **HTTP/SSE** at `/mcp`. The Inspector can connect to that URL.

1. **Start the server:**  
   `rav run dev` (server at http://127.0.0.1:8123).

2. **Open the Inspector** (pick one):
   - **CLI:** `npx @modelcontextprotocol/inspector`
   - **Web:** open the Inspector in your browser (e.g. the official or community hosted version).

3. **Connect to this server:**  
   Use **transport: SSE** (or HTTP) and **URL:**  
   `http://127.0.0.1:8123/mcp`

4. You can then list and call tools (`save_document`, `list_saved_documents`) from the Inspector.

CORS is enabled on this app so the browser-based Inspector can call the server. The [FastMCP CLI `inspector`](https://gofastmcp.com/python-sdk/fastmcp-cli-cli#inspector) is for running a server *with* the Inspector; here we run the server with uvicorn and connect the Inspector to the URL above.

## Layout

Mirrors **fastapi-fastmcp**: one combined FastAPI app, MCP at `/mcp`, `rav run dev` uses `working_dir: src` and `uvicorn main:app`.
