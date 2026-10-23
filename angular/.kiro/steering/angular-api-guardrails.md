---
inclusion: always
---
# Angular API Guardrails (version-gated) — repo version: {{ANGULAR_MAJOR}}

## Precedence (highest first)
1. Explicit instruction in the current task/spec. 2. This repo's steering + exemplar code.
3. Official Angular guidance (angular.dev best practices, MCP `get_best_practices`, angular/skills). 4. Training memory — verify with `search_documentation`.

## Never "modernize" by side effect
Only apply modern APIs in files you were asked to create/change. Don't convert NgModules, decorators, `*ngIf`, constructor DI, zone code or reactive forms elsewhere.

## Version gates — use an API only if repo major >= gate
| API / behaviour | Min major | Notes |
|---|---|---|
| `@if/@for/@switch` | 17 | `track` mandatory |
| `input()/output()/model()`, `linkedSignal` | 19–20 | — |
| `standalone` default (omit flag) | 19 | — |
| Suffix-less generated names | 20 | Only if repo uses them |
| `provideZonelessChangeDetection()` stable | 20.2 | Zoneless default for NEW apps from 21 |
| Vitest via `@angular/build:unit-test` | 21 | Only if repo uses it |
| `provideHttpClient()` optional | 21 | Don't remove existing calls |
| Signal Forms stable; `resource/rxResource/httpResource` stable | 22 | Experimental in 21 — ask before using there |
| OnPush default; `Eager` strategy name | 22 | Keep `Eager` annotations |
| `@Service()`, `injectAsync()` | 22 | `@Service` requires `inject()` |
| HttpClient Fetch default, `withXhr()` | 22 | Upload progress needs XHR |
| `strictTemplates` default true | 22 | Respect explicit `false` |
| `debounced()` | 22 (experimental) | Ask before use |

## Hard bans (all versions)
- No NgModules in standalone code; no `standalone: true`; no `CommonModule` imports.
- No direct DOM access (`document.querySelector`, `nativeElement.innerHTML =`). Use bindings, `Renderer2`, CDK.
- No `window`/`document`/`localStorage` outside {{PLATFORM_SAFE_SERVICE}} or `afterNextRender` when SSR = {{true}}.
- No inventing APIs: if unsure an Angular/Material/NgRx API exists in version {{X}}, query `search_documentation` or ask.
- No new dependencies without approval. Zoneless repos: view-driving state is a signal; no reliance on zone-triggered CD.
