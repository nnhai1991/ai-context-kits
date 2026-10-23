---
inclusion: fileMatch
fileMatchPattern: ["**/*.ts", "**/*.html", "**/*.scss", "**/*.css"]
---
# Coding Conventions

## Components
- Standalone {{default}}; do NOT write `standalone: true` (default since v19/20).
- Change detection: {{v22+: omit `changeDetection` (OnPush default); keep existing `ChangeDetectionStrategy.Eager` untouched | <v22: always set OnPush}}.
- APIs: `input()`, `input.required()`, `output()`, `model()`, `viewChild()`, `contentChild()`; no `@Input/@Output/@ViewChild` in new code {{unless legacy area}}.
- Host bindings in `host: {}`; never `@HostBinding`/`@HostListener`.
- Template-only members `protected`; signals `readonly`. Import only directives/pipes used; never `CommonModule`.
- Images: `NgOptimizedImage` (`ngSrc`) for static images.

## Templates
- `@if / @for (…; track item.id) / @switch / @let`; never `*ngIf/*ngFor/*ngSwitch` (deprecated since v20).
- `[class.x]` / `[style.x]` instead of `ngClass` / `ngStyle`. Signals are called: `items()`. No side-effecting function calls in templates.
- Every interactive element is a native `<button>`/`<a>` or uses {{Angular Aria / CDK a11y}}; labels for every input.

## TypeScript
- No `any` (use `unknown` + narrowing). No non-null `!` to silence errors. Prefer inference.
- Naming: files {{kebab-case, suffix style per structure.md}}; classes PascalCase; signals nouns (`paymentMethods`), events (`deleted`, `delete`).

## Styling
- {{SCSS + design tokens from {{PATH}} | Tailwind | Material theming API}}; no hard-coded colours.

## Lint/format are law
- Code must pass `{{LINT_CMD}}` and `{{FORMAT_CHECK_CMD}}` with zero new warnings. Do not disable rules inline without asking.
