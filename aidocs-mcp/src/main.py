"""
FastAPI + FastMCP server: upload documents and save them to outputs/.
"""
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

# outputs/ at project root (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

api = FastAPI()
mcp = FastMCP("aidocs-mcp").from_fastapi(api)
mcp_app = mcp.http_app(path="/mcp")


@api.get("/")
def read_root():
    return {"message": "AiDocs MCP — upload documents to save in outputs/"}


@api.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document; it is saved under outputs/ using the original filename.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")
    path = OUTPUTS_DIR / file.filename
    try:
        content = await file.read()
        path.write_bytes(content)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}") from e
    return {"filename": file.filename, "path": str(path), "size": len(content)}


@mcp.tool()
def save_document(filename: str, content: str) -> str:
    """
    Save a text document to the outputs/ directory.
    Use this to store document content (e.g. from a path or pasted text) under the given filename.
    """
    if not filename:
        return "Error: filename is required."
    path = OUTPUTS_DIR / filename
    try:
        path.write_text(content, encoding="utf-8")
        return f"Saved to {path} ({len(content)} bytes)."
    except OSError as e:
        return f"Error saving file: {e}"


@mcp.tool()
def list_saved_documents() -> str:
    """
    List document filenames currently saved in the outputs/ directory.
    """
    if not OUTPUTS_DIR.exists():
        return "Outputs directory is empty or missing."
    names = sorted(p.name for p in OUTPUTS_DIR.iterdir() if p.is_file())
    if not names:
        return "No documents in outputs/."
    return "\n".join(names)


app = FastAPI(
    title="AiDocs MCP",
    routes=[
        *mcp_app.routes,
        *api.routes,
    ],
    lifespan=mcp_app.lifespan,
)
# Allow browser-based MCP Inspector (e.g. modelcontextprotocol/inspector) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
