# CI/CD con GitHub Actions (enfoque SRE / DevOps)

Pipeline de integración y despliegue continuo para aplicaciones Vue.js, diseñado para entornos de producción y buenas prácticas de ingeniería de confiabilidad (SRE).

## Estructura del repositorio

Cada aplicación vive en su propia carpeta en la raíz del repo para poder añadir varios proyectos:

- **`fronttest/`** — App de prueba Vue.js (lint, unit tests, e2e, build). El CI/CD actual ejecuta todos los jobs sobre esta carpeta (`working-directory: fronttest`).
- Futuros proyectos (por ejemplo `backoffice/`, `api/`) pueden añadirse como nuevas carpetas; para ejecutar CI/CD sobre ellos se puede usar una matriz de proyectos o workflows separados por `paths`.

## Resumen de workflows

| Workflow | Archivo | Disparo | Propósito |
|----------|---------|---------|-----------|
| **CI** | `ci.yml` | Push / PR a `main`, `develop` | Lint, unit tests, cobertura, integration/e2e tests, quality gate |
| **CD** | `cd.yml` | Cuando CI termina con éxito en `main` | Build, artifact versionado, deploy (configurable) |

---

## Etapas del pipeline CI

### 1. Checkout & Setup

- **Job:** `setup`
- Checkout del repositorio (`actions/checkout@v4`), configuración de Node.js con **cache de npm** para reducir tiempos, e instalación reproducible con `npm ci`.
- Los jobs siguientes (`lint`, `unit-tests`, `integration-tests`) dependen de `setup` y repiten checkout + cache + `npm ci` en paralelo donde aplica, para **fail fast** y reutilización de cache.

### 2. Linter / Static Analysis

- **Job:** `lint`
- Ejecuta `npm run lint` (ESLint u otra herramienta configurada en el proyecto).
- El pipeline **debe fallar** si hay errores; se recomienda configurar el script con `--max-warnings 0` para que los warnings también fallen en CI.
- **Herramientas recomendadas (Vue):** ESLint, `eslint-plugin-vue`, `@vue/eslint-config-typescript` si usas TypeScript.

### 3. Unit Tests + Cobertura

- **Job:** `unit-tests`
- Ejecuta `npm run test:unit -- --coverage` (Vitest o Jest).
- **Umbral mínimo de cobertura:** por defecto 80 %, configurable con la variable `COVERAGE_MIN_PERCENT`. Si la cobertura está por debajo, el job falla.
- Se espera un reporte en `coverage/coverage-summary.json` (por ejemplo con Vitest y reporter `json-summary`). El step "Check coverage threshold" valida ese fichero.
- El reporte de cobertura se sube como artifact (retención 7 días) para inspección o integración con Sonar, etc.

**Validar cobertura desde CLI (ejemplo Vitest):**

```bash
npx vitest run --coverage
# Umbral en vitest.config: coverage: { lines: 80, functions: 80, branches: 80, statements: 80 }
```

### 4. Functional / Integration Tests

- **Job:** `integration-tests`
- Ejecuta `npm run test:e2e` (o `test:integration`) con variables de entorno de CI (`NODE_ENV=test`, `VITE_API_URL`, etc.).
- Si los tests necesitan base de datos o servicios, se pueden añadir con `services:` en el job o con un step que levante mocks (por ejemplo `json-server`).
- **Herramientas recomendadas:** Playwright o Cypress para E2E con Vue.

### 5. Quality Gate

- **Job:** `quality-gate`
- Depende de `lint`, `unit-tests` e `integration-tests`. Solo se ejecuta si **los tres** terminan con éxito.
- No ejecuta pruebas adicionales; representa la decisión de “todo OK para seguir a build/deploy”. Si algún job anterior falla, el workflow falla y el quality gate no se ejecuta (o falla por dependencias).

**Concepto:** El quality gate es el punto único donde se considera que el CI está verde (lint OK, tests OK, cobertura OK). En `main`, solo cuando el CI (y por tanto este gate) pasa se dispara el CD.

---

## Etapas del pipeline CD

### 6. Build & Artifact

- **Job:** `build`
- Solo corre cuando el workflow **CI** ha terminado con éxito en la rama **main** (`workflow_run` con `conclusion == 'success'`).
- Hace checkout del commit que pasó el CI (`workflow_run.head_sha`), instala dependencias, ejecuta `npm run build` y sube el directorio `dist/` como artifact con nombre `app-vue-<SHA>` (retención 30 días).

### 7. Deploy

- **Job:** `deploy`
- Descarga el artifact del job `build` y ejecuta los pasos de despliegue. Por defecto incluye solo un placeholder; hay ejemplos comentados para GitHub Pages, S3 o SSH.
- **Secrets:** Todas las credenciales deben ir en GitHub Secrets (`secrets.DEPLOY_KEY`, `secrets.AWS_ACCESS_KEY_ID`, etc.), nunca en el YAML en claro.
- **Protección del entorno:** El job usa `environment: ${{ env.DEPLOY_ENVIRONMENT }}` (por defecto `production`). En **Settings → Environments** puedes:
  - Exigir **approval** manual antes de desplegar.
  - Definir **protection rules** (ramas permitidas, etc.).
  - Restringir qué usuarios pueden aprobar.

---

## Variables configurables

Definir en **Settings → Secrets and variables → Actions → Variables** (o en el YAML con `vars.*`):

| Variable | Uso | Valor por defecto |
|----------|-----|-------------------|
| `COVERAGE_MIN_PERCENT` | Umbral mínimo de cobertura (%) | `80` |
| `NODE_VERSION` | Versión de Node.js | `20` |
| `API_URL_CI` | URL base para tests de integración (mock/staging) | `http://localhost:3000` |
| `DEPLOY_ENVIRONMENT` | Nombre del environment de deploy | `production` |

En el YAML se usan así:

```yaml
env:
  COVERAGE_MIN_PERCENT: ${{ vars.COVERAGE_MIN_PERCENT || '80' }}
  NODE_VERSION: ${{ vars.NODE_VERSION || '20' }}
```

---

## Buenas prácticas SRE aplicadas

- **Fail fast:** Lint y unit tests se ejecutan en paralelo tras el setup; los fallos se detectan pronto.
- **Jobs paralelos:** `lint` y `unit-tests` comparten `needs: setup` para reducir tiempo total.
- **Observabilidad:** Artifacts de cobertura y de build; logs por job; opcionalmente se puede añadir un job summary con enlaces o métricas.
- **Reintentos:** Los steps críticos no usan `continue-on-error`; se puede añadir `timeout-minutes` en jobs pesados y, si hace falta, `retries` en acciones de terceros.
- **Separación CI vs CD:** Dos workflows; el CD solo se dispara cuando el CI ha pasado en `main`.
- **Seguridad:** Permisos mínimos (`contents: read` en CI; en CD solo los necesarios para deploy); credenciales en Secrets; uso de Environments para aprobaciones y reglas.

---

## Escalar a más apps o frameworks

El repo está organizado por carpetas (por ejemplo `fronttest/`). Para más proyectos:

- **Opción A — Matriz:** Un solo workflow CI con `strategy.matrix: project: [fronttest, otro-proyecto]` y en cada job `working-directory: ${{ matrix.project }}`, y `cache-dependency-path: ${{ matrix.project }}/package-lock.json`. Los artefactos usarían `path: ${{ matrix.project }}/dist/` y `path: ${{ matrix.project }}/coverage/`.
- **Opción B — Workflows por app:** Crear `ci-fronttest.yml`, `ci-otro.yml`, etc., con `paths: ['fronttest/**']` o `['otro-proyecto/**']` para que cada workflow solo se dispare cuando cambien archivos de esa app.
- **Reusable workflows:** Un workflow base (por ejemplo `ci-base.yml`) que reciba `app-path` y `node-version`; cada app invoca ese workflow con sus parámetros para reutilizar la misma estructura (lint, unit, integration, quality gate).

---

## Prerrequisitos en el repositorio

Para que el CI funcione, el `package.json` de la app debe exponer al menos:

- `lint` — Linter (ESLint recomendado; fallar con errores y, si quieres, con warnings).
- `test:unit` — Tests unitarios con cobertura (Vitest/Jest); salida en `coverage/coverage-summary.json` si se usa el step de umbral.
- `test:e2e` o `test:integration` — Tests funcionales o E2E (Playwright/Cypress).
- `build` — Build de producción (por ejemplo Vite; salida en `dist/`).

Al añadir una app Vue u otra en Node, conviene actualizar el `.gitignore` con: `node_modules/`, `dist/`, `coverage/`, `.env.local`, etc.
