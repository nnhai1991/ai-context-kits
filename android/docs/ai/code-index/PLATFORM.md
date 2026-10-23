# Code index — Android specifics

## Generate / query
    python3 scripts/ai/build_code_index.py --platform android --root . --out docs/ai/code-index [--check]
    python3 scripts/ai/query_code_index.py impact <file.kt> [...]

## What is an entry point here (one flow each)
Composable screens reached by navigation (`composable<Route>`, `entry<Key>`, `composable("route")`, `dialog<…>`), `Activity`/`Fragment` classes,
`Worker` classes, and anything annotated `"entry": true` in `annotations.json` (e.g. a `BroadcastReceiver`, a deep-link handler, an exported `ContentProvider`).
Name heuristic: files matching `Screen|Activity|Fragment|Route`. Review the Flows table once: demote nothing (bogus flows are harmless), add what is missing.

## Directory buckets
`dir` = the file's package directory; directories with fewer than `--min-rows` (3) files in their subtree collapse into the parent. Gradle modules
are NOT required: when the repo is modularized, the module name is simply the leading path segment (`feature/cards/...`) and layering rules in
`rules/allowed-edges.json` can use it (`"dirs": [{"from": "feature/*", "to": "feature/*", "allow": false}]`). Monoliths get the same treatment by package.

## Tools that replace the regex extractors (use when available; record the tool in `graph.json › extractor`)
- Module graph: `./gradlew -q projects`, `./gradlew :app:dependencies --configuration {{variant}}RuntimeClasspath`, `com.jraska.module.graph.assertion` → authoritative `imports` between modules.
- DI edges: Hilt aggregated components in `build/generated/hilt`; Koin `module { }` / `get()`; Metro `@DependencyGraph` → `injects`/`implements`.
- Navigation: Nav3 `entry<Key>`/`NavKey`, Nav2 `composable<Route>`/`navigate(`, Fragment `res/navigation/*.xml` (`<action app:destination>`), manifest deep links → `defines_route`/`navigates_to`.
- HTTP: Retrofit `@GET/@POST(...)`, Ktor `client.get("…")`, Apollo operations → `consumes_endpoint` (client apps never *expose*; a KMP server module would).
- Storage: `@Entity(tableName)`, `@Dao` + `@Query("… FROM table")`, DataStore keys, SharedPreferences names, KeyStore → `storage:<table|key|store>`.
- Symbols/complexity: `detekt --report xml`, Kotlin `-Xdump-declarations-to`, or `kotlinx-ast` → better `symbols`, `calls` with medium confidence.
- Tests: `src/test`, `src/androidTest`, screenshot dirs → `tested_by`.

## Card extras for Android (write them in the prose sections when relevant)
Dispatcher usage, lifecycle/process-death handling (`SavedStateHandle`), permissions touched, R8 keep-rule needs, minSdk guards, feature-flag gates, Play data-safety categories.
