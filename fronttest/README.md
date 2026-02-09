# fronttest

App de prueba Vue.js para el pipeline CI/CD: lint, tests unitarios (Vitest), tests E2E (Playwright) y build.

Todo lo necesario para este proyecto está en esta carpeta; la raíz del repo solo contiene lo compartido (`.github`, `.gitignore`, README del repo).

## Requisitos

- Node.js 20 (o la versión indicada en CI)
- npm

## Comandos

Ejecutar siempre desde esta carpeta (`fronttest/`):

```bash
npm install
npm run dev        # Servidor desarrollo (Vite)
npm run lint       # ESLint (max-warnings 0)
npm run test:unit  # Vitest + cobertura
npm run test:e2e   # Playwright (arranca dev server)
npm run build      # Build producción → dist/
```

## Estructura

- `src/` — Código Vue (App, componentes, assets)
- `e2e/` — Tests E2E (Playwright)
- Tests unitarios junto a componentes (`*.spec.ts`)
- Cobertura y build: `coverage/` y `dist/` (generados, en .gitignore)
