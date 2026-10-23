---
inclusion: always
---
# Technology Stack
## Toolchain (authoritative)
- Xcode {{26.x}} (CI {{26.x}}) · Swift language mode {{5|6}} · swift-tools-version {{6.x}}
- Minimum deployment: iOS {{17.0}} {{, macOS …}} — newer APIs MUST use `if #available(iOS NN, *)` with a fallback.

## Concurrency build settings (read from project — never assume)
- Strict concurrency: {{minimal|targeted|complete}} · Default Actor Isolation: {{MainActor|nonisolated}} (per target: {{…}})
- Approachable Concurrency: {{YES|NO}} · Upcoming features: {{NonisolatedNonsendingByDefault, InferIsolatedConformances, …}}
- SPM swiftSettings: {{.defaultIsolation(MainActor.self), .enableUpcomingFeature(...)}}

## UI
- Policy: {{SwiftUI-only | UIKit-only | Mixed: new screens SwiftUI via UIHostingController}} · Observation: {{@Observable|ObservableObject|TCA}}

## Dependencies — the ONLY allowed third-party libraries
| Library | Version | Purpose | Import |
|---|---|---|---|
| {{swift-composable-architecture}} | {{1.x}} | {{state}} | `import ComposableArchitecture` |
- Managers: {{SPM|CocoaPods}}; local packages in `{{Packages/}}`. Propose new deps in design.md "Open questions" — never add them.

## Commands (run these to verify work)
- Schemes: `xcodebuild -list -workspace {{App.xcworkspace}}`
- Build: `xcodebuild build -workspace {{…}} -scheme {{App}} -destination 'platform=iOS Simulator,name={{iPhone 17}}' -quiet`
- Tests: `xcodebuild test -workspace {{…}} -scheme {{App}} -destination '{{…}}' -only-testing:{{Target/Suite}}`
- Packages: `swift test --package-path {{Packages/Feature}}`
- Lint: `{{swiftlint lint --strict}}` · Format: `{{swiftformat --lint .}}`
- Project generation: `{{tuist generate | xcodegen generate}}` — never hand-edit generated project files.
- Fastlane: `{{bundle exec fastlane test}}`
