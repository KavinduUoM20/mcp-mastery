from fastapi import FastAPI
from fastmcp import FastMCP

api = FastAPI()
mcp = FastMCP("mcptest").from_fastapi(api)
mcp_app = mcp.http_app(path="/mcp")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers together
    """
    return (a + b) * 1000   

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together
    """
    return (a * b) * 1000

@api.get("/")
def read_root():
    return {"message": "Hello, World!"}

app = FastAPI(
    title="FastAPI FastMCP",
    routes=[
        *mcp_app.routes,
        *api.routes,
    ],
    lifespan=mcp_app.lifespan,
)