# Code index — iOS specifics

## Generate / query
    python3 scripts/ai/build_code_index.py --platform ios --root . --out docs/ai/code-index [--check]
    python3 scripts/ai/query_code_index.py impact <File.swift> [...]

## What is an entry point here (one flow each)
Screens reached by navigation (`NavigationLink(value:)`, `.navigationDestination(for:)`, coordinator `push(`/`present(`, `StackState<Route>`),
`UIViewController` subclasses and coordinators, app/scene delegates, background tasks (`BGTaskScheduler`), widgets and app-extension entry points,
plus anything annotated `"entry": true` in `annotations.json`. Name heuristic: `Screen|Page|RootView|Coordinator|ViewController|Router|Scene|Flow`.
Plain `*View.swift` files are deliberately NOT entries (they are subviews); annotate the real screens if the repo names them `View`.

## Edge quality warning
Swift `import` is module-level, so within one target the only regex signal is symbol matching (`calls`, low confidence). Flows therefore
report `confidence: low` on iOS until a symbol tool is used. Treat `possible` rows in impact output as "open the file and check".

## Directory buckets
`dir` = the file's folder (Xcode groups or folder-synced groups). Targets / SPM packages are optional: when present, the leading path segment
(`Packages/Payments/Sources/...`) is the module and `rules/allowed-edges.json` can constrain `Features/* → Features/*`.

## Tools that replace the regex extractors (use when available; record the tool in `graph.json › extractor`)
- Symbol graph: `swift symbolgraph-extract` / `xcrun swift-symbolgraph-extract -module-name X -target …` or `indexstore-db` → real `calls`, `extends`, `implements` with high confidence; also merges a type spread across extension files into one node (`symbols`).
- Targets/packages: `xcodebuild -list -json`, `swift package describe --type json`, Tuist `tuist graph --format json`, XcodeGen `project.yml` → module facet and `imports` between targets.
- DI: swift-dependencies `@Dependency(\.key)` + `DependencyKey` conformances; Factory `@Injected`; Swinject `register/resolve` → `injects`/`implements`.
- Navigation: coordinator `push`/`present`, `NavigationStack` destinations, deep links in `Info.plist`/associated domains → `navigates_to`/`defines_route`.
- HTTP: `APIClient.get(path:)`, `URLRequest` builders, generated OpenAPI clients → `consumes_endpoint`. Storage: SwiftData `@Model`, Core Data entities, GRDB/Realm tables, `UserDefaults` keys, Keychain → `storage:`.
- Tests: `*Tests.swift`, `*UITests` → `tested_by`.

## Card extras for iOS (write them in the prose sections when relevant)
Actor isolation (`@MainActor`, `nonisolated`), Sendable requirements, availability guards (`#available`), app-extension safety (`UIApplication.shared`), background-mode behaviour, Keychain accessibility class.
