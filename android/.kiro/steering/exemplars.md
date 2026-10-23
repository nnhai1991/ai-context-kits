---
inclusion: auto
name: exemplars
description: "Golden-path reference files for implementing a new screen, ViewModel, use case, repository, API call, Room DAO, DI module, navigation route or tests in this Android repo"
---
# Golden-path exemplar: `{{feature name}}` (copy its shape, not its business logic)

| Layer | File |
|---|---|
| Route + Screen composable | `{{feature/x/src/main/.../XRoute.kt}}` |
| UiState | `{{.../XUiState.kt}}` |
| ViewModel | `{{.../XViewModel.kt}}` |
| Use case | `{{.../GetXUseCase.kt}}` |
| Repository interface + impl | `{{.../XRepository.kt}}`, `{{.../DefaultXRepository.kt}}` |
| API service | `{{.../XApi.kt}}` |
| DTO + mapper | `{{.../XDto.kt}}`, `{{.../XMapper.kt}}` |
| Room entity + DAO | `{{.../XEntity.kt}}`, `{{.../XDao.kt}}` |
| DI module | `{{.../XModule.kt}}` |
| Navigation registration | `{{.../XNavigation.kt}}` |
| ViewModel test | `{{.../XViewModelTest.kt}}` |
| UI / screenshot test | `{{.../XScreenTest.kt}}` |

Read these before writing a new feature; mirror structure, naming and test style.
(In Kiro you may replace paths with live refs: `#[[file:path]]`.)

## Shared infrastructure (reuse)
| Need | Use |
|---|---|
| HTTP / Database / DataStore | `{{path}}` / `{{path}}` / `{{path}}` |
| Image loader / WorkManager factory | `{{path}}` / `{{path}}` |
| Analytics / Feature flags | `{{path}}` / `{{path}}` |
| Loading & error UI | `{{LoadingContent / ErrorSnackbarHost}}` |

## Do-not-copy areas (legacy)
- `{{paths}}` — {{why}}
