---
id: structure
scope: always
---
# Repository structure

- Project source of truth: `settings.gradle.kts` + `gradle/libs.versions.toml` + convention plugins in `{{build-logic/ | buildSrc/}}`

## Modules (from settings.gradle.kts)
| Module | Type | May depend on | Purpose |
|---|---|---|---|
| `:app` | application | all `:feature:*`, `:core:*` | wiring, nav host, Application |
| `:feature:{{name}}` | {{android-library / feature convention}} | `:core:*` only | {{...}} |
| `:core:{{name}}` | {{...}} | `:core:{{lower}}` | {{...}} |

Rule: a `:feature:*` module MUST NOT depend on another `:feature:*` module {{or: only on its `:api`}}.

## Package layout inside a feature module (copy exactly)

    {{com.company.app}}.feature.{{name}}/
      ui/          {{Screen.kt, Route.kt, ViewModel.kt, UiState.kt, components/}}
      navigation/  {{FeatureNavigation.kt}}
      di/          {{FeatureModule.kt}}
      domain/      {{only if feature-local use cases}}

{{OR describe by-layer layout if that is what the scan found}}

## Source sets
- Unit tests: `src/test/`; instrumented: `src/androidTest/`; screenshot: `{{src/screenshotTest/ | src/test/ (Roborazzi/Paparazzi)}}`
- Flavor-specific code: `src/{{flavor}}/`
- Generated code (NEVER edit by hand): `build/generated/**`, `{{apollo/openapi output dir}}`, `{{schemas/ (Room exported schemas)}}`

## Key entry points
- Application: `{{path/MyApplication.kt}}`
- Main activity / nav host: `{{path}}`
- Navigation graph / keys: `{{path}}`
- DI root: `{{path}}`

## Do-not-touch
`build/**`, `**/generated/**`, `{{schemas/**}}`, `gradle/wrapper/**`, `local.properties`, `*.jks`, `*.keystore`, `google-services.json` {{list}}
