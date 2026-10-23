---
id: testing
scope: glob
globs: ["**/*.spec.ts", "**/e2e/**", "**/*.e2e.ts", "**/playwright.config.*", "**/cypress/**"]
description: "Testing rules for unit and e2e tests"
---
# Testing Rules
- Runner: **{{Vitest | Jest | Karma+Jasmine}}**; globals {{on/off}} -> import `{ describe, it, expect, vi }` from 'vitest' {{if off}}.
- Style: {{TestBed + CDK harnesses | Angular Testing Library (`render`, `screen`)}}.
- Zoneless tests: {{yes}} -> `await fixture.whenStable()`; no `fakeAsync/tick` {{unless zone.js present}}.
- HTTP: `provideHttpClient()`, `provideHttpClientTesting()`, `HttpTestingController`; assert method/URL/body; `verify()` in afterEach.
- Stores: {{SignalStore via TestBed.inject | NgRx MockStore | facade with mocked API}}.
- Test names reference requirement IDs: `it('[REQ-2.1] shows empty state when no methods', …)`.
- Selectors: roles/labels first; `data-testid` only when no accessible handle exists.
- E2E: {{Playwright}} in `{{E2E_PATH}}`; `{{E2E_CMD}}`; never depend on test order.
- Coverage gate: {{N}}% lines on changed files. Commands: single `{{TEST_ONE_CMD}}`; all `{{TEST_CMD}}`.
- Copy structure from exemplar spec: `{{EXEMPLAR_SPEC_PATH}}`.

## Definition of Done
- [ ] Lint, typecheck, unit tests, build (and e2e if touched) green via tech.md commands; no new warnings; budgets unchanged
- [ ] Strings localized; AXE clean; every EARS criterion maps to >=1 test
- [ ] No unapproved deps; generated code untouched; tasks.md updated
