---
inclusion: fileMatch
fileMatchPattern: ["**/*.ts", "angular.json", "nx.json", "**/project.json"]
---
# Architecture Rules (filled from scan + tech lead; UNKNOWNs in questions.md; evidence: docs/ai/scan-report.md)

## Pattern
- Primary state/data pattern: **{{STATE_PATTERN}}** (NgRx Store+Effects | NgRx SignalStore | NGXS | Akita/Elf | services+signals | RxJS BehaviorSubject services | legacy mixed). Confidence {{HIGH/MED/LOW}}.
- Facade layer: {{yes — components talk only to *Facade / *Store | no}}.
- Smart/presentational split: {{pages/ = smart; ui/ = presentational (inputs/outputs only)}}.

## Data flow (golden path)
route -> {{Page}} -> {{Facade/Store}} -> {{ApiService}} -> HttpClient -> DTO -> mapper -> model -> {{Presentational}}

## Dependency direction
- Allowed: page -> facade/store -> api -> http; ui -> models only.
- Forbidden: ui -> data-access; data-access -> pages; feature A -> feature B internals. Never change Nx tags/depConstraints without asking.

## Dependency injection
- {{inject() | constructor injection (legacy)}}. New singletons: {{@Service() (v22+) | @Injectable({ providedIn: 'root' })}}.
- Feature-scoped state: provide in the route's `providers` {{or component providers}}, not root.
- Configuration via injection tokens: {{API_BASE_URL in core/config.ts}}.

## Routing
- Standalone `Routes`; lazy `loadComponent` / `loadChildren` per feature.
- Guards/resolvers: {{functional CanActivateFn/ResolveFn | class-based (legacy)}}; `withComponentInputBinding` {{on/off}}.
- {{v22: paramsInheritanceStrategy default 'always' unless app.config overrides.}}

## Signals vs RxJS policy
- Component state: signals (`signal`, `computed`, `linkedSignal`). Async reads: {{httpResource/rxResource (v22 stable) | Observable + toSignal | store effects}}.
- Event streams with cancellation/debounce/combination: RxJS inside services; expose as signals or `async` pipe.
- No manual `.subscribe()` in components unless paired with `takeUntilDestroyed()`. Never hold the same state in a signal AND a BehaviorSubject.

## Forms
- New forms: {{Signal Forms (@angular/forms/signals) | typed Reactive Forms (NonNullableFormBuilder)}}. Never untyped `FormGroup`/`any`.
- Custom controls: {{FormValueControl (v22) | ControlValueAccessor}}.

## Errors
- Global: {{ErrorHandler path}}; HTTP: {{error interceptor path}}; user notification via {{NotificationService path}}. No duplicate toasts.

## Legacy coexistence
- {{"src/app/legacy/** is NgModule + zone + RxJS. Edit in its existing style; do not migrate unless the task says so."}}
