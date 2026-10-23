---
inclusion: always
---
# Architecture (discovered by repo scan on {{SCAN_DATE}}; confidence {{HIGH/MED/LOW}}; evidence: docs/ai/scan-report.md)

## Pattern in use
{{MVVM | MVI (Orbit/MVIKotlin/custom reducer) | Clean (ui/domain/data) | Circuit | Decompose | mixed: describe}}
Evidence: {{3–5 file paths}}

## Layers & dependency direction
`ui -> {{domain ->}} data`. Domain is {{pure Kotlin, no android.* imports | not present}}.
DTOs never cross into ui; map in `{{data/mapper}}`.

## State holder contract (house pattern first; defaults apply ONLY if the scan found none)
- House pattern: {{e.g. `@HiltViewModel class XViewModel @Inject constructor(...) : ViewModel()` exposing `val uiState: StateFlow<XUiState>`}}
- Default (Google architecture recommendations): UDF; ViewModel exposes `uiState` via
  `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), initial)`; UI sends actions via method calls (`onXxx()`);
  ViewModel holds no Context/View/Lifecycle references.
- One-off events: {{"model as state + consume callback" | Channel<Effect>.receiveAsFlow() | Orbit sideEffect}}.
- Composables never mutate ViewModel state directly; they call event lambdas. Screen-level `Route` takes the ViewModel;
  inner `Screen` takes state + lambdas only (stateless, previewable).

## DI
{{Hilt}}: modules in `{{path}}`, `@InstallIn({{SingletonComponent}})`, bindings via `@Binds` for interfaces.
Dispatchers injected via `{{@IoDispatcher}}`.

## Navigation
{{Navigation 3: NavKey per destination in `:feature:x:api`, entries registered in `{{path}}`, back stack is app state}}
{{or Navigation-Compose type-safe `@Serializable` routes}} {{or Fragment nav graphs in res/navigation}}.
Never mix navigation libraries in new code.

## Concurrency
{{Coroutines/Flow}}: `viewModelScope` in ViewModels; no `GlobalScope`; long-running/durable work -> WorkManager;
catch exceptions without swallowing `CancellationException`.
{{RxJava}}: only in legacy modules {{list}}; new code uses Flow; bridge with `asFlow()`.

## Process death & config changes
Persist user input / selection in `SavedStateHandle` keys or `rememberSaveable`; nav state {{is serializable}}.

## Persistence
{{Room as source of truth; repositories wrap DAOs}}. Schema changes need a `Migration` + migration test -> stop-and-ask.
