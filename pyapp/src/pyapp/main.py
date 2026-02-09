"""API mínima para tests funcionales."""

from fastapi import FastAPI

from pyapp.calculator import add, greet

app = FastAPI(title="pyapp", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Health check."""
    return {"status": "ok"}


@app.get("/greet/{name}")
def greet_endpoint(name: str) -> dict[str, str]:
    """Saludo por nombre."""
    return {"message": greet(name)}


@app.get("/add")
def add_endpoint(a: int, b: int) -> dict[str, int]:
    """Suma dos enteros (query params)."""
    return {"result": add(a, b)}
