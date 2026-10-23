# Implementation Plan — {{Feature}}

- [ ] 1. Domain model + mapper + mapper tests (from generated `{{PaymentMethodDto}}`) — _Requirements: 1.1, NFR-1_
- [ ] 2. API service + `HttpTestingController` tests (list/create/setDefault/delete); use `{{API_BASE_URL_TOKEN}}`; no manual auth headers — _1.1, 2.3, 3.1, 4.2_
- [ ] 3. Store/facade with status signals + tests (optimistic default + rollback) — _1.2–1.4, 2.5, 3.1–3.2, 4.2–4.3_ ; depends on 2
- [ ] 4. Presentational `payment-method-card` + tests (inputs/outputs, a11y) — _1.1, 3.1, 4.1, NFR-2_
- [ ] 5. Add-card form (validation, pending state, PSP wrapper) + tests — _2.1–2.6, NFR-1_
- [ ] 6. Page component, route file, lazy registration in `{{APP_ROUTES}}` with existing auth guard + tests — _1.1–1.5, NFR-3, NFR-4_ ; depends on 3,4,5
- [ ] 7. Remove-confirmation dialog + default-reassignment rule + flag gate + tests — _4.1–4.4_
- [ ] 8. E2E happy path + run all gates (`{{LINT_CMD}}`, `{{TYPECHECK_CMD}}`, `{{TEST_CMD}}`, `{{BUILD_CMD}}`) — _all_

Rule: every task leaves the project compiling; tests ship in the same task; state dependencies.
