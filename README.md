# pipeline-generic

Repositorio base con CI/CD en GitHub Actions (enfoque SRE/DevOps) y aplicaciones organizadas por carpetas.

## Regla de organización

- **En la raíz solo va lo compartido** por todos los proyectos: CI/CD (`.github/`), `.gitignore` y este README.
- **Cada proyecto es una carpeta autocontenida** con su propio código, configs, tests y dependencias. Nada propio del proyecto queda en la raíz.

Así se pueden añadir más proyectos (por ejemplo `backoffice/`, `api/`) sin mezclar cosas y reutilizando un solo pipeline.

## Estructura

```
.
├── .github/workflows/     # Compartido: CI/CD (un workflow por proyecto)
├── .gitignore             # Compartido: reglas para todo el repo
├── README.md              # Compartido: este archivo
├── fronttest/             # Proyecto Vue.js (lint, unit, e2e, build)
│   ├── src/, e2e/, package.json, vite.config.ts, ...
│   └── README.md
└── pyapp/                 # Proyecto Python (lint, unit, functional)
    ├── src/pyapp/, tests/, pyproject.toml, ...
    └── README.md
```

Cada proyecto tiene dentro todo lo suyo (código, configs, tests). Los workflows de CI se ejecutan **solo cuando cambian archivos de ese proyecto** (`paths: ['fronttest/**']` o `paths: ['pyapp/**']`).

## Cómo trabajar con cada proyecto

### fronttest (Vue.js)

```bash
cd fronttest
npm install
npm run dev        # Desarrollo
npm run lint       # ESLint
npm run test:unit  # Vitest (unit + coverage)
npm run test:e2e   # Playwright
npm run build      # Build producción → dist/
```

### pyapp (Python)

```bash
cd pyapp
uv sync --all-extras   # o: pip install -e ".[dev]"
uv run ruff check .    # Lint
uv run pytest tests/unit -m unit --cov=src --cov-fail-under=80
uv run pytest tests/functional -m functional
```

## Gestión de CI/CD con varios proyectos en el mismo repo

**Recomendación: workflows separados por proyecto** (como en este repo), no un único workflow mezclado.

| Enfoque | Ventajas | Inconvenientes |
|--------|----------|-----------------|
| **Workflows separados** (uno por proyecto, con `paths`) | Cada stack (Node, Python, etc.) tiene su runtime y sus pasos. Solo corre el CI del proyecto que cambió. YAML más simple y mantenible. | Varios archivos en `.github/workflows/`. |
| **Un solo workflow con matriz** | Un único archivo. | Mezcla runtimes (Node + Python) en el mismo job o obliga a muchos jobs condicionales; más complejo y frágil. |
| **Un solo workflow sin matriz** | Muy simple si solo hay un proyecto. | Con varios proyectos distintos (lenguajes/frameworks) se vuelve un “todo en uno” difícil de leer y de cachear bien. |

En este repo:

- **`ci.yml`** — Solo para **fronttest** (Vue/Node). Se dispara con `paths: ['fronttest/**']`.
- **`ci-pyapp.yml`** — Solo para **pyapp** (Python). Se dispara con `paths: ['pyapp/**']`.
- **`cd.yml`** — Build/deploy (hoy solo fronttest; se puede duplicar o extender para pyapp si hace falta).

Así, un push que solo toque `pyapp/` ejecuta solo el CI de Python; uno que solo toque `fronttest/` ejecuta solo el CI de Vue. Si en el futuro añades más proyectos (por ejemplo otro front o una API), crea un nuevo `ci-<nombre>.yml` con `paths: ['<carpeta>/**']` y `working-directory: <carpeta>`.

## Variables y secrets en GitHub (por proyecto)

Configurar en **Settings → Secrets and variables → Actions** del repositorio.

### Variables (pestaña Variables)

| Variable | Uso | Valor por defecto | Proyecto |
|----------|-----|-------------------|----------|
| `NODE_VERSION` | Versión de Node.js en CI/CD | `20` | fronttest |
| `COVERAGE_MIN_PERCENT` | Umbral mínimo de cobertura (%) | `80` | fronttest |
| `API_URL_CI` | URL base para tests E2E/integración | `http://localhost:3000` | fronttest |
| `DEPLOY_ENVIRONMENT` | Environment de deploy (approvals, etc.) | `production` | fronttest |
| `PYTHON_VERSION` | Versión de Python en CI | `3.12` | pyapp |
| `COVERAGE_MIN_PERCENT_PYAPP` | Umbral de cobertura para pyapp (opcional; si no existe se usa `COVERAGE_MIN_PERCENT`) | `80` | pyapp |

No es obligatorio definirlas: si no existen, se usan los valores por defecto del workflow.

### Secrets (pestaña Secrets)

Solo son necesarios cuando actives un paso de deploy real en `.github/workflows/cd.yml`. Ejemplos según destino:

| Secret | Cuándo usarlo |
|--------|----------------|
| `DEPLOY_KEY` | Deploy por SSH (clave privada) |
| `DEPLOY_HOST` | Deploy por SSH (host) |
| `DEPLOY_USER` | Deploy por SSH (usuario) |
| `AWS_ACCESS_KEY_ID` | Deploy a AWS (p. ej. S3) |
| `AWS_SECRET_ACCESS_KEY` | Deploy a AWS |

Para GitHub Pages suele bastar con `GITHUB_TOKEN` (ya disponible en el job). **Nunca** pongas credenciales en el YAML; solo en Secrets.

## Añadir otro proyecto

1. Crear una nueva carpeta en la raíz con su propio código, dependencias y tests (por ejemplo `mi-app/`).
2. Añadir un **workflow propio** `.github/workflows/ci-mi-app.yml` con:
   - `on.push.paths` y `on.pull_request.paths`: `['mi-app/**']` (y opcionalmente el propio archivo del workflow).
   - `defaults.run.working-directory: mi-app` en los jobs.
   - Jobs equivalentes: setup, lint, unit-tests, (functional/e2e si aplica), quality-gate.

Documentación detallada del pipeline: [.github/workflows/README.md](.github/workflows/README.md).
