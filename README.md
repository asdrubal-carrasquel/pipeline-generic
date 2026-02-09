# pipeline-generic

Repositorio base con CI/CD en GitHub Actions (enfoque SRE/DevOps) y aplicaciones organizadas por carpetas.

## Regla de organización

- **En la raíz solo va lo compartido** por todos los proyectos: CI/CD (`.github/`), `.gitignore` y este README.
- **Cada proyecto es una carpeta autocontenida** con su propio código, configs, tests y dependencias. Nada propio del proyecto queda en la raíz.

Así se pueden añadir más proyectos (por ejemplo `backoffice/`, `api/`) sin mezclar cosas y reutilizando un solo pipeline.

## Estructura

```
.
├── .github/workflows/     # Compartido: CI/CD para el repo
├── .gitignore             # Compartido: reglas para todo el repo
├── README.md              # Compartido: este archivo
└── fronttest/             # Proyecto autocontenido (Vue.js)
    ├── src/
    ├── e2e/
    ├── package.json
    ├── vite.config.ts
    ├── vitest.config.ts
    └── ...
```

Cada proyecto (por ejemplo `fronttest`) tiene dentro todo lo suyo: `package.json`, configuraciones, tests, código. El pipeline ejecuta **desde la carpeta del proyecto** (`working-directory: fronttest`). Los artefactos generados (coverage, dist, test-results) quedan dentro de esa carpeta si ejecutas los comandos desde ella (`cd fronttest`).

## Cómo trabajar con fronttest

```bash
cd fronttest
npm install
npm run dev        # Desarrollo
npm run lint       # ESLint
npm run test:unit  # Vitest (unit + coverage)
npm run test:e2e   # Playwright
npm run build      # Build producción → dist/
```

## Variables y secrets en GitHub (por proyecto)

Configurar en **Settings → Secrets and variables → Actions** del repositorio. El pipeline actual usa estas configuraciones para **fronttest**; al añadir más proyectos se puede reutilizar la misma lógica o usar variables por environment.

### Variables (pestaña Variables)

| Variable | Uso | Valor por defecto | Proyecto |
|----------|-----|-------------------|----------|
| `NODE_VERSION` | Versión de Node.js en CI/CD | `20` | fronttest |
| `COVERAGE_MIN_PERCENT` | Umbral mínimo de cobertura (%) para que pase el CI | `80` | fronttest |
| `API_URL_CI` | URL base para tests E2E/integración (mock o staging) | `http://localhost:3000` | fronttest |
| `DEPLOY_ENVIRONMENT` | Nombre del environment de deploy (approvals, protection rules) | `production` | fronttest |

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

1. Crear una nueva carpeta en la raíz (por ejemplo `mi-app/`) con su propio `package.json` y scripts: `lint`, `test:unit`, `test:e2e`, `build`.
2. Para que el CI/CD la incluya:
   - **Opción A:** Añadir la carpeta a una matriz en `.github/workflows/ci.yml` (véase `.github/workflows/README.md`).
   - **Opción B:** Crear un workflow específico (por ejemplo `ci-mi-app.yml`) con `paths: ['mi-app/**']` y `working-directory: mi-app`.

Documentación detallada del pipeline: [.github/workflows/README.md](.github/workflows/README.md).
