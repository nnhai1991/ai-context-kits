# Implementation Plan — {{Feature}}

- [ ] 1. Network contract
  - [ ] 1.1 Add `{{X}}Dto` + `{{X}}Api` per OpenAPI; mapper `toDomain()` + mapper tests — _Requirements: 1.1, 1.6_
- [ ] 2. Persistence (STOP: confirm migration approach with tech lead before starting)
  - [ ] 2.1 `{{X}}Entity`, `{{X}}Dao`, migration v{{n}}->v{{n+1}} + migration test — _Requirements: 1.1_
- [ ] 3. Repository — depends on 1, 2
  - [ ] 3.1 `{{OfflineFirstXRepository}}` (observe DB, refresh, setDefault, delete with rollback) + tests with fakes
  - [ ] 3.2 Bind in `{{XDataModule}}` — _Requirements: 1.1–1.4, 2.1–2.2, 3.2_
- [ ] 4. Domain — depends on 3
  - [ ] 4.1 `{{SetDefaultUseCase}}`, `{{DeleteUseCase}}` (default-card rule) + tests — _Requirements: 2.1, 3.3_
- [ ] 5. ViewModel + UiState + SavedStateHandle + Turbine tests — depends on 4 — _Requirements: 1.*, 2.*, 3.*, 4.1_
- [ ] 6. Compose UI: `{{XScreen}}` (design-system components, strings, semantics, previews) + UI test + screenshot tests — depends on 5 — _Requirements: 1.5, 1.6, 3.1, 3.4, 4.2, 4.3_
- [ ] 7. Navigation registration + feature flag gate + entry point — depends on 6 — _Requirements: 3.4_
- [ ] 8. Gate: run format, detekt, lint{{Variant}}, test{{Variant}}UnitTest, screenshot verify; fix all failures; zero new warnings

Rule: every task leaves the project compiling; tests ship in the same task as the code; state dependencies so parallel runs don't collide.
