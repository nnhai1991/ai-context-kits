# Design — {{Feature}}

## Impact (from docs/ai/code-index — run prompts/impact-analysis.md first)
| Node | Why affected | Change type | Tests | Human review? |
|---|---|---|---|---|
| {{…}} | {{…}} | {{behaviour/contract}} | {{…}} | {{yes/no}} |
Reuse candidates: {{…}} · Contract changes (stop-and-ask): {{…}}

## Fit to existing architecture (from architecture.md, exemplars.md)
Mirrors exemplar `{{feature}}`. Module: `{{:feature:payments}}` (new screen) + `{{:core:data / :core:network / :core:database}}` additions. No new dependencies.

## Components
| Layer | Type | Notes |
|---|---|---|
| UI | `{{PaymentMethodsRoute}}` (VM, nav) -> `{{PaymentMethodsScreen}}(uiState, onSetDefault, onDeleteRequest, onDeleteConfirm, onRetry)` | stateless screen, previews per state |
| State | `{{PaymentMethodsUiState}}` sealed: `Loading`, `Content(items, isRefreshing, pendingDelete)`, `Empty`, `Error` | `pendingDelete` in `SavedStateHandle` |
| VM | `{{PaymentMethodsViewModel}}` | `uiState = repo.observe().map{…}.stateIn(WhileSubscribed(5000))` {{or Orbit container}} |
| Domain | `{{SetDefaultPaymentMethodUseCase}}`, `{{DeletePaymentMethodUseCase}}` | default-card rule (Req 3.3) lives here |
| Data | `{{PaymentMethodsRepository}}` / `{{OfflineFirstPaymentMethodsRepository}}` | Room = source of truth; refresh writes to DB |
| Network | `{{PaymentMethodsApi}}` + `{{PaymentMethodDto}}` (`@Serializable`) | from OpenAPI `{{tag}}` |
| DB | `{{PaymentMethodEntity}}`, `{{PaymentMethodDao}}` | **schema migration v{{n}}->v{{n+1}} — requires approval** |
| DI | `{{PaymentsDataModule}}` (`@Binds`) | |
| Nav | `{{PaymentMethodsKey : NavKey}}` registered in `{{AppNavigation}}` | |

## Sequence (delete)
UI -> VM.onDeleteConfirm(id) -> DeleteUseCase -> repo.delete(id): DAO soft-remove -> API DELETE -> on failure restore row + emit error.

## Error handling
`{{DomainError}}.{Network, Unauthorized, Conflict}` -> UiState message resource ids.

## Testing strategy (trace to requirements)
| Req | Test |
|---|---|
| 1.1–1.5 | VM Turbine tests with `Fake{{PaymentMethods}}Repository` |
| 2.2 | VM test: optimistic revert |
| 3.3 | Use case unit test |
| 4.1 | `SavedStateHandle` restore test |
| 4.2 | Compose UI semantics test |
| 4.3 | Screenshot tests (light/dark/fontScale 2) |

## Open questions needing tech-lead approval
- {{Soft delete vs immediate? New dependency? Permission? Schema change?}}
