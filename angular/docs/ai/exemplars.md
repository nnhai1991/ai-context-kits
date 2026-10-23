---
id: exemplars
scope: auto
description: "Golden-path reference files to copy when creating or changing an Angular feature, page, component, store, service, form, or test"
---
# Golden-Path Exemplars — copy these patterns, not tutorials

Exemplar feature: **{{EXEMPLAR_FEATURE}}** (chosen by scan: recent, idiomatic, tested, touches all layers).

| Layer | File | What to copy |
|---|---|---|
| Routes | `{{PATH}}/{{feature}}.routes.ts` | lazy loading, route providers, guards |
| Page (smart) | `{{PATH}}` | injection, store wiring, template states |
| Store/Facade | `{{PATH}}` | state shape, loading/error, methods |
| API service | `{{PATH}}` | HttpClient usage, URLs, typing |
| Mapper | `{{PATH}}` | DTO->model |
| Presentational | `{{PATH}}` | inputs/outputs, a11y |
| Form | `{{PATH}}` | form API & validation display |
| Unit test | `{{PATH}}` | test setup idiom |
| E2E | `{{PATH}}` | selectors, fixtures |

(In Kiro you may use live refs: `#[[file:path]]`.)

## Shared infrastructure (reuse)
| Need | Use |
|---|---|
| Auth / interceptors / error handler | `{{core/auth…}}` / `{{core/interceptors…}}` / `{{core/error-handler.ts}}` |
| Layout shell / notifications / logger | `{{PATH}}` / `{{PATH}}` / `{{PATH}}` |
| Design-system lib public API | `{{@acme/shared/ui}}` |
| Testing utils / mock factories | `{{PATH}}` |

## Anti-exemplars (do NOT copy)
- `{{PATHS}}` — {{reason, e.g. "src/app/legacy/orders — NgModule/zone; frozen"}}
