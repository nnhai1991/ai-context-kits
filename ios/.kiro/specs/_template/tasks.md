# Implementation Plan: {{Feature}}
- [ ] 1. Domain: `Card` model + `CardsRepository` protocol (+ tests) — _Requirements: 1.1_
- [ ] 2. Data: `CardDTO`, `CardMapper`, `DefaultCardsRepository` via `APIClient`; mapping/error tests — _1.1, 1.3_
- [ ] 3. `FetchSavedCardsUseCase` with sorting; tests — _1.1_
- [ ] 4. `PaymentMethodsViewModel` (loading/empty/error) + tests — _1.2, 1.3, 1.6_
- [ ] 5. `PaymentMethodsView` with DesignSystem, a11y labels, localized strings; snapshots — _1.5, 1.6_
- [ ] 6. DI in `PaymentsAssembly`, route in `AppRouter`, flag `payments_saved_cards` — _1.4_
- [ ] 7. Verify: build + test + lint commands from tech.md; zero new warnings
Rule: every task leaves the project compiling; tests ship in the same task as the code.
