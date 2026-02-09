"""Módulo de ejemplo para tests unitarios."""


def add(a: int | float, b: int | float) -> int | float:
    """Suma dos números."""
    return a + b


def greet(name: str) -> str:
    """Devuelve un saludo."""
    if not name or not name.strip():
        raise ValueError("name must be non-empty")
    return f"Hello, {name.strip()}!"


def is_even(n: int) -> bool:
    """Indica si un entero es par."""
    return n % 2 == 0
