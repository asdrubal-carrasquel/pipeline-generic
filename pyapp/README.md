# pyapp

App de prueba en Python para el pipeline CI/CD: lint (Ruff), tests unitarios (pytest + cobertura), tests funcionales (API con TestClient).

Todo lo necesario para este proyecto está en esta carpeta.

## Requisitos

- Python 3.11+
- uv (recomendado) o pip

## Instalación

```bash
cd pyapp
uv sync --all-extras    # instala deps + dev (pytest, ruff, etc.)
# o con pip:
# pip install -e ".[dev]"
```

## Comandos

Ejecutar siempre desde esta carpeta (`pyapp/`):

```bash
# Lint
uv run ruff check .

# Tests unitarios con cobertura (umbral 80 %)
uv run pytest tests/unit -m unit --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80

# Tests funcionales (API)
uv run pytest tests/functional -m functional

# Todos los tests
uv run pytest
```

## Estructura

- `src/pyapp/` — Código (calculator, FastAPI main)
- `tests/unit/` — Tests unitarios (marcados con `@pytest.mark.unit`)
- `tests/functional/` — Tests funcionales contra la API (marcados con `@pytest.mark.functional`)
- Cobertura: `htmlcov/` o `coverage/` (generados, en .gitignore)

## API (desarrollo)

```bash
uv run uvicorn pyapp.main:app --reload
```

Endpoints: `GET /health`, `GET /greet/{name}`, `GET /add?a=1&b=2`.
