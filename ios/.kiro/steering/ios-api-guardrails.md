---
inclusion: fileMatch
fileMatchPattern: ["**/*.swift"]
---
# iOS API Guardrails (deployment target iOS {{17.0}})
- If unsure an API exists, search Apple docs (Xcode MCP documentation search if available). Never invent API.
- SwiftUI: `foregroundStyle()` not `foregroundColor()`; `clipShape(.rect(cornerRadius:))` not `cornerRadius()`;
  zero- or two-parameter `onChange`; `NavigationStack` not `NavigationView`{{; `Tab` API if iOS 18+}}.
- Observation: {{`@Observable` + `@State`; `@Bindable` for bindings}}; no `ObservableObject` in new code {{except module X}}.
- Concurrency: no `DispatchQueue.main.async`/semaphores in new code; prefer async APIs over completion handlers.
- No UIKit types (`UIColor`, `UIScreen.main`) inside SwiftUI views except via `{{DesignSystem}}` bridges.
- Use `URL.documentsDirectory` and `FormatStyle` (`.formatted()`) instead of `String(format:)` for user-facing numbers.
