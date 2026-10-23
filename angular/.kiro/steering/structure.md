---
inclusion: always
---
# Project Structure

## Workspace map

    {{e.g.
    src/app/
      core/            # singletons: auth, interceptors, error handler, config tokens
      shared/ui/       # presentational, design-system wrappers
      features/<name>/
        <name>.routes.ts
        pages/         # routed smart components
        ui/            # presentational components
        data-access/   # store/facade + API service + mappers
        models/        # domain types
    }}

## Placement rules
| Artifact | Location | File name pattern |
|---|---|---|
| Routed page | {{FEATURE_ROOT}}/<feature>/pages/ | {{payment-methods-page.ts}} |
| Presentational component | {{.../ui/}} | {{payment-method-card.ts}} |
| Store / facade | {{.../data-access/}} | {{payment-methods.store.ts / payment-methods-facade.ts}} |
| API service | {{.../data-access/}} | {{payment-methods-api.ts}} |
| DTO (generated) | {{GENERATED_API_PATH}} — never edit | — |
| Mapper | {{.../data-access/}} | {{payment-method.mapper.ts}} |
| Domain model | {{.../models/}} | {{payment-method.ts}} |
| Unit test | next to source | `*.spec.ts` |

## File naming style
- Suffixes: {{"suffix-less (v20 style: user.ts)" OR "suffixed (user.component.ts)"}} — match neighbouring files.
- Selector prefix: `{{PREFIX}}-`; class names: {{PaymentMethodsPage OR PaymentMethodsPageComponent}}.

## Import rules
- Path aliases: {{@app/core/*, @acme/shared/ui}}. No deep relative imports across features (`../../../`).
- Features may import: core, shared, own folder. Features may NOT import other features' internals.
- Nx tags (if Nx): {{type:feature|ui|data-access|util; scope:<domain>}} enforced by `@nx/enforce-module-boundaries`.

## Do-not-touch
`{{GENERATED_API_PATH}}`, `dist/**`, `.angular/**`, `{{legacy islands}}`, lockfile (except via package manager), `nx.json` depConstraints.
