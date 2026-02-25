from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastmcp import FastMCP

def start_greeting(name: str) -> str:
    msg = f"Hello! {name}"
    print(msg)
    return msg

def end_greeting(name: str) -> None:
    print(f"Goodbye {name}!")

user_profile = {}

@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    # before the app starts
    user_profile["name"] = start_greeting  # store the function for greet_user / API
    start_greeting("App")  # run startup greeting
    yield
    # after the app stops
    end_greeting("App")
    print("FastAPI lifespan: goodbye!")


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

@mcp.tool()
def greet_user(name: str) -> str:
    """
    Greet the user
    """
    result = user_profile["name"](name)
    return result

@api.get("/")
def read_root():
    return {"message": "Hello, World!"}

@api.get("/greet_user")
def greet_user(name: str):
    """
    Greet the user
    """
    result = user_profile["name"](name)
    return {"message": result}

@asynccontextmanager
async def global_lifespan(app: FastAPI):
    async with fastapi_lifespan(app):
        async with mcp_app.lifespan(app):
            yield


app = FastAPI(
    title="FastAPI FastMCP",
    routes=[
        *mcp_app.routes,
        *api.routes,
    ],
    lifespan=global_lifespan,
)