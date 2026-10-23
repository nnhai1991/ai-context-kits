# Code index — Angular specifics

## Generate / query
    python3 scripts/ai/build_code_index.py --platform angular --root . --out docs/ai/code-index [--check]
    python3 scripts/ai/query_code_index.py impact <file.ts> [...]

## Naming note
The index's "directory" facet is a folder, never an `NgModule`. Legacy `NgModule` classes are ordinary nodes of kind `di-module`.
A component's `.ts`, `.html`, `.scss` and `.spec.ts` are grouped under its class file (one node, one row); template selectors (`<app-x>`) become high-confidence `calls` edges.

## What is an entry point here (one flow each)
Routed components (`loadComponent`, `component:` in a `Routes` array, `loadChildren` targets), `*-page.ts` / `*.page.ts` / `Container|Shell|Layout` components,
HTTP interceptors and guards are NOT entries (they appear as shared files). Annotate `"entry": true` for bootstrapped root components and web workers.

## Directory buckets
`dir` = the file's folder; small folders collapse into their parent (`--min-rows`). Nx projects are optional: when present, the project root
(`libs/cards/feature/...`) is the leading path and `rules/allowed-edges.json` should mirror the `@nx/enforce-module-boundaries` depConstraints
(e.g. `"dirs": [{"from": "libs/*/feature*", "to": "libs/*/feature*", "allow": false}]`).

## Tools that replace the regex extractors (use when available; record the tool in `graph.json › extractor`)
- Nx: `nx graph --file=graph.json` and `project.json` tags → authoritative project-level `imports`; `nx show projects`.
- Angular CLI MCP (`ng mcp`): `list_projects`; TypeScript program (`ts-morph`, `tsc --listFiles`, `madge --json src`) → exact file-level `imports` including path aliases from `tsconfig.paths`.
- Angular compiler (`ngc` with `extendedDiagnostics`) or `@angular/language-service` → template references (component usage, pipes, directives) with high confidence.
- Routing: `Routes` arrays, `provideRouter`, `withComponentInputBinding` → `defines_route`; `router.navigate`, `routerLink` → `navigates_to`.
- HTTP: `HttpClient` calls, `httpResource()`, generated OpenAPI clients → `consumes_endpoint`. State: NgRx actions/effects, SignalStore methods, services with signals → `emits`/`observes`.
- Tests: `*.spec.ts` (Vitest/Jasmine), `e2e/` → `tested_by`.

## Card extras for Angular (write them in the prose sections when relevant)
Change detection (`OnPush` vs `Eager`), zoneless safety, SSR/hydration constraints (`window`, `document`), signal vs RxJS boundary, i18n keys owned, accessibility contract of shared components.
