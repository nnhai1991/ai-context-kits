---
id: testing
scope: glob
globs: ["**/src/test/**", "**/src/androidTest/**", "**/src/screenshotTest/**", "**/*Test.kt"]
description: "Testing rules for unit, UI and screenshot tests"
---
# Testing rules

## Stack
- Unit: {{JUnit4 | JUnit5 (jupiter)}}, kotlinx-coroutines-test (`runTest`), Turbine for Flow, {{Truth | AssertK | kotlin.test}}.
- Doubles: prefer hand-written fakes from `{{:core:testing}}`; {{MockK | Mockito-Kotlin}} only for {{framework/third-party boundaries}}.
- Main dispatcher: `{{MainDispatcherRule}}` at `{{path}}`.
- Robolectric: {{allowed for Android-framework unit tests / not used}}.
- Compose UI tests: `createAndroidComposeRule<ComponentActivity>()`; find by `testTag`/semantics, not raw localized text.
- Screenshot: {{Roborazzi | Paparazzi | Compose Preview Screenshot Testing}}; baselines recorded by {{CI only | developer with command X}}.
  Never commit re-recorded baselines unless the task is a visual change.
- Instrumented: Gradle-managed device `{{task}}`.

## Required per feature task (Definition of Done)
1. ViewModel test: initial state, success, error, and each user action (Turbine `test {}` on `uiState`).
2. Repository test with fake data sources (Room in-memory DB or DAO fake).
3. Mapper tests for DTO->domain incl. null/unknown fields.
4. Compose UI test for primary interaction + accessibility semantics.
5. Screenshot test for each `UiState` variant.
6. `{{format}}`, `{{detekt}}`, `lint{{Variant}}`, `test{{Variant}}UnitTest` all green; no new lint-baseline entries.
7. Every EARS criterion maps to >=1 test referencing its ID.

## Naming
`fun \`given X when Y then Z\`()` {{or methodName_condition_expected}}. One behaviour per test.
