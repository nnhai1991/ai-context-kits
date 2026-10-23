---
id: conventions
scope: glob
globs: ["**/*.kt", "**/*.kts", "**/res/values*/strings.xml"]
description: "Kotlin, Compose and Views coding conventions"
---
# Kotlin & Android conventions

## Naming
| Kind | Pattern | Example |
|---|---|---|
| Screen composable | `{{Feature}}Screen` (stateless) + `{{Feature}}Route` (holds VM) | `PaymentMethodsScreen` |
| ViewModel | `{{Feature}}ViewModel` | |
| UI state | `{{Feature}}UiState` ({{sealed interface | data class}}) | |
| Use case | `{{Verb}}{{Noun}}UseCase` with `operator fun invoke` | `DeletePaymentMethodUseCase` |
| Repository | `{{Noun}}Repository` (interface) / `{{Default|Offline}}{{Noun}}Repository` (impl) | |
| DTO / Entity / Domain | `{{Noun}}Dto` / `{{Noun}}Entity` / `{{Noun}}` | |
| Test fake | `Fake{{Noun}}Repository` in `{{:core:testing}}` | |

## Style
- Formatter: {{ktlint via Spotless | ktfmt}}; config: `.editorconfig`, `{{config/detekt/detekt.yml}}`. Run `{{format cmd}}` before finishing.
- Visibility: `internal` by default inside feature modules; `public` only for module API. {{explicitApi() enabled in :core:*}}.
- No `!!` in production code; no `lateinit` in ViewModels.
- Errors: {{`Result<T>` | sealed `DomainResult`}}; map exceptions at repository boundary; never catch `CancellationException` silently.
- Logging: `{{Timber}}` only; never log tokens, PAN, email, or other PII.

## Compose UI
- Use `{{DesignSystem}}` components from `{{:core:designsystem}}` before Material3 primitives; colors/typography via `{{AppTheme}}` tokens, never raw `Color(0x...)`/`sp` literals.
- Strings: `stringResource(R.string.…)`; no hard-coded user-visible text; plurals via `pluralStringResource`.
- Accessibility: every non-decorative `Icon`/`Image` gets `contentDescription` (decorative = `null`); clickable rows use
  `Modifier.semantics(mergeDescendants = true)` or `toggleable/selectable` roles; min touch target 48.dp.
- Collect flows with `collectAsStateWithLifecycle()`.
- Each screen has `@Preview`s {{light/dark, fontScale 1.5}} using a `PreviewParameterProvider` for states.
- `modifier` is the first optional parameter and is applied to the root.

## Views (legacy/mixed)
- ViewBinding {{not DataBinding}}; Fragments collect with `viewLifecycleOwner.repeatOnLifecycle(STARTED)`.
- Compose inside Views via `ComposeView` with `ViewCompositionStrategy.{{DisposeOnViewTreeLifecycleDestroyed}}`.
