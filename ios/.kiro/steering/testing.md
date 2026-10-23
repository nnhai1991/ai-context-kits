---
inclusion: fileMatch
fileMatchPattern: ["**/*Tests/**/*.swift", "**/Tests/**/*.swift"]
---
# Testing & Quality Gates
- Framework: {{Swift Testing for new tests (`@Test`, `#expect`) | XCTest}}; never mix in one file.
- Mocks: {{hand-written `MockXRepository` in TestSupport/}} | {{@Dependency test values}}.
- Snapshots: {{swift-snapshot-testing}}; UI tests: {{XCUITest via accessibility identifiers}}.
- Must test: VM/reducer logic, use cases, mappers, repository error paths.
- Every EARS criterion maps to ≥1 test referencing its ID. Coverage target: {{≥80% Domain/Presentation}}.
- CI: {{.github/workflows/ci.yml: lint → build → unit → snapshot}}.
## Definition of Done
- [ ] Builds and tests pass via tech.md commands; lint clean; no new warnings
- [ ] Strings localized; a11y labels; design tokens used
- [ ] No unapproved dependencies/permissions; tasks.md updated; requirement IDs in PR
