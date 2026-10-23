# Architecture Rules
Pattern: {{MVVM | TCA | Clean+MVVM | VIPER | MVC | Hybrid}} (confidence {{high/med/low}}; evidence: docs/ai/scan-report.md)

## Dependency direction
{{Presentation → Domain ← Data}} — Views never call networking/persistence; Domain imports no UIKit/SwiftUI.

## Per-layer recipe
| Concern | Use | Never |
|---|---|---|
| Screen state | {{@Observable @MainActor final class XViewModel / @Reducer struct XFeature}} | {{ObservableObject in new code}} |
| Business logic | {{XUseCase protocol + DefaultXUseCase}} | {{logic in views}} |
| Data access | {{XRepository protocol (Domain) + impl (Data)}} | {{URLSession in features}} |
| DI | {{init injection composed in XAssembly / @Dependency(\.xClient)}} | {{new singletons}} |
| Navigation | {{NavigationStack(path:) + Route enum in AppRouter / Coordinator}} | {{cross-feature NavigationLink}} |

## Concurrency
- Model: {{async/await everywhere; Combine only in legacy modules X, Y}}
- UI types are {{@MainActor (implicit via default isolation | explicit)}}; background work via {{@concurrent / actor XStore}}.
- No `DispatchQueue.main.async` in new code. Start work in `.task {}` or keep and cancel the Task.
- Domain models are Sendable value types.

## UI bridging
- {{New screens SwiftUI, hosted by UIHostingController in Coordinators; UIViewRepresentable only in DesignSystem/Bridges}}

## Persistence
- {{SwiftData container in App; repositories wrap ModelContext}}. Schema changes need a migration plan in design.md.
