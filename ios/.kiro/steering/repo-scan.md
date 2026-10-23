---
inclusion: manual
---
# REPO SCAN — fill the iOS AI-context templates from this repository
Fill docs/ai/{product,tech,structure,architecture,conventions,testing,api-contracts,exemplars,ios-api-guardrails}.md.
RULES: Read-only — modify no source, project files or dependencies. Every value cites evidence (path:line or command
output). Missing/conflicting evidence → `UNKNOWN – ask tech lead: <precise question>`. Never guess. Never print secret values.

## Step 0 — Inventory
- `git ls-files | wc -l`; tree to depth 3 (exclude Pods, .build, DerivedData, Carthage).
- Hot files: `git log --since=6.months --name-only --pretty=format: | sort | uniq -c | sort -rn | head -50`.
- Locate: *.xcworkspace, *.xcodeproj, Package.swift (all), Package.resolved, Podfile(.lock), Cartfile(.resolved),
  Project.swift/Tuist/, project.yml, Gemfile, fastlane/Fastfile, .swiftlint.yml, .swiftformat, .xcode-version,
  *.xcconfig, Info.plist, *.entitlements, PrivacyInfo.xcprivacy, *.xcstrings, .github/workflows/*, bitrise.yml,
  ci_scripts/ (Xcode Cloud), .circleci/, .gitlab-ci.yml, Dangerfile, openapi*.{yaml,json}, *.graphql,
  existing AGENTS.md/CLAUDE.md/.cursor/.kiro, docs/adr.

## Step 1 — Toolchain → tech.md
- `xcodebuild -list -json`; `xcodebuild -showBuildSettings -scheme <main> -json` (fallback: grep pbxproj/xcconfig) for
  SWIFT_VERSION, *_DEPLOYMENT_TARGET, SWIFT_STRICT_CONCURRENCY, SWIFT_DEFAULT_ACTOR_ISOLATION,
  SWIFT_APPROACHABLE_CONCURRENCY, SWIFT_UPCOMING_FEATURE_*, OTHER_SWIFT_FLAGS, TARGETED_DEVICE_FAMILY.
- Package.swift: tools version, platforms, targets, swiftSettings (.defaultIsolation, .enableUpcomingFeature,
  .swiftLanguageMode), dependencies. Xcode version from .xcode-version / CI runner / DEVELOPER_DIR.
- Dependency table from Package.resolved / Podfile.lock / Cartfile.resolved.
- Build/test/lint commands: copy what CI and Fastfile lanes actually run.

## Step 2 — Structure → structure.md
- Targets (app, extensions, frameworks, tests) and dependencies; generator (Tuist/XcodeGen; .xcodeproj git-ignored?;
  PBXFileSystemSynchronizedRootGroup present?).
- Module graph: per module `grep -rh "^import " | sort | uniq -c`.
- Generated/vendored paths (SwiftGen, Sourcery, OpenAPI output, R.swift, Vendor/).

## Step 3 — Entry point & UI framework
- `@main struct …: App` vs `@main`/`@UIApplicationMain` AppDelegate; SceneDelegate; UIApplicationSceneManifest;
  storyboards/xibs; UIMainStoryboardFile.
- Counts: `import SwiftUI` vs `import UIKit`; `: View {` vs `UIViewController` subclasses; `UIHostingController`,
  `UIViewRepresentable`. Classify SwiftUI-only (>90%), UIKit-only, or Mixed — and from the last 6 months of history,
  which kind of screen is being added now.

## Step 4 — Architecture detection (score each; report evidence counts)
| Pattern | Signals |
|---|---|
| TCA | `import ComposableArchitecture`, `@Reducer`, `Reduce {`, `StoreOf<`, `@ObservableState`, `@Dependency` |
| MVVM | `*ViewModel.swift`; `@Observable`/`ObservableObject`+`@Published` classes owned by views |
| Clean | `*UseCase*`, `*Repository` protocols, Domain/Data/Presentation folders, DTO→Entity mappers |
| VIPER | per-module `*Interactor`+`*Presenter`+`*Router`/`*Wireframe`+`*Entity`, `*Builder`/`*Module` |
| RIBs | `*Buildable`, `*Interactor`, `*Router`, RIBs dependency |
| MVC | logic-heavy view controllers, no VM/Presenter types |
| Custom Redux | custom `Store`, `Action` enums, `reduce(` |
| Modular SPM | many local library products; Features/*, Core/*; Interface/Implementation split |
Report dominant + secondary/legacy patterns with paths; confidence high (≥70% of feature folders), medium (40–70%),
low; and conflicts with ADRs/docs.

## Step 5 — Cross-cutting mechanisms
- DI: Swinject (`Container()`, `.register`), Factory (`@Injected`, `Container.shared`), Needle (`Component<`),
  swift-dependencies (`@Dependency`, `DependencyKey`), custom `EnvironmentKey`s, Assembly/Composition Root,
  singletons (`static let shared`).
- Navigation: `NavigationStack(path:`, `navigationDestination`, `NavigationView`, `*Coordinator`, `*Router`, Route enums,
  TCA `StackState`/`@Presents`, `UINavigationController`, deep links (`onOpenURL`, `openURLContexts`).
- Concurrency counts: `async func`, `actor `, `@MainActor`, `Task {`, `Task.detached`, `@concurrent`, `nonisolated`,
  `Sendable`, `AnyPublisher`/`.sink(`, `DispatchQueue`, `completion:`, `withCheckedContinuation` → classify per module.
- Networking client, endpoint style, auth refresh, decoder config, error type. Persistence (SwiftData `@Model`, Core Data
  `.xcdatamodeld`, GRDB, Realm, Keychain/UserDefaults wrappers). Logging, analytics, flags, l10n, design system.
- Security: paths (not values) of likely secrets (`apiKey`, `secret`, `.p8`, GoogleService-Info.plist); ATS keys;
  usage descriptions; entitlements; privacy manifest.

## Step 6 — Testing → testing.md
- `import XCTest` vs `import Testing` counts per target; snapshot/UI test targets; Mock*/Fake*/Stub* style and generator
  configs; *.xctestplan; coverage settings; CI required checks; PR template.

## Step 7 — Pick the golden-path exemplar → exemplars.md
Score the top 3 candidates. Choose the feature that (a) follows the dominant pattern; (b) is a full vertical slice
(UI, state, use case, repository, network call, mapper, DI registration, navigation entry); (c) has unit (ideally
snapshot) tests; (d) changed in the last 6 months but is not the highest-churn area; (e) has ~5–15 files; (f) has few
lint suppressions/TODOs. List every file with its role, plus 1–3 anti-exemplars with reasons.

## Step 8 — Output
1. Filled docs/ai/*.md (keep {{…}} only where UNKNOWN); always-loaded files ≤ ~120 lines.
2. docs/ai/scan-report.md: evidence table (fact, value, source, confidence), architecture and exemplar scoring tables,
   detected conflicts.
3. ## UNKNOWN – ask tech lead — checklist of precise questions (why it matters, what was found), always including:
   direction for new UI if mixed; whether legacy patterns may be extended; DoD/coverage targets; who approves
   permissions/entitlements; which architecture docs are authoritative.

# STEP — Build the code index (after the scan, before any feature work)
Follow `docs/ai/code-index/prompts/build-code-index.md` and `docs/ai/code-index/PLATFORM.md`. Generate with
`python3 scripts/ai/build_code_index.py --platform ios --root . --out docs/ai/code-index` (every file gets a row, flows from each entry point,
contracts with all parties; on iOS prefer the symbol-graph tool named in PLATFORM.md, regex edges are low confidence). Then: fix entry points and
`rules/allowed-edges.json`, write one-line summaries in `annotations.json` (exemplar → hotspots → shared files → the rest), write invariants on flow,
directory and promoted component cards, and make `build_code_index.py --check` pass. Design work must run `prompts/impact-analysis.md` first.
