# The iOS AI-Context Template Kit: one fill-in package that lets Kiro (and every other coding agent) generate code that fits an existing iOS repo

The most reliable way to get correct AI-generated code in an existing iOS repo is to keep a small, architecture-agnostic set of context files and fill it in from the repo itself. Kiro steering describes how the repo works, Kiro specs describe what to build, and one exemplar feature shows the whole vertical slice. A repo-scan prompt generates all of this and the tech lead reviews it. Keep one canonical copy and feed AGENTS.md, CLAUDE.md, Cursor, Copilot, Windsurf and Xcode from it.

## TL;DR

- **What the AI needs:** about 58 facts in 8 groups (checklist in section 1). The ones that matter most are exact Swift/Xcode/deployment-target versions, the dominant architecture and its dependency direction, the concurrency and actor-isolation settings, one golden-path exemplar feature, the existing networking/persistence/DI entry points, and the exact build and test commands. Hallucinated or wrong-version APIs, mixed UIKit/SwiftUI idioms, main-actor bugs and invented dependencies almost always trace back to one of these being missing.
- **How to package it:** use Kiro's three foundation steering files (`product.md`, `tech.md`, `structure.md`, which are included in every interaction by default). Add six iOS files (`architecture.md`, `conventions.md`, `testing.md`, `api-contracts.md`, `exemplars.md`, `ios-api-guardrails.md`), each set to `always`, `fileMatch`, `manual` or `auto` inclusion so the context budget stays small. Feature work goes through EARS-format specs in `.kiro/specs/<feature>/`.
- **How to stay portable and get it filled:** keep the canonical text in `docs/ai/`. Generate thin per-tool adapters from it: AGENTS.md, a CLAUDE.md that imports `@AGENTS.md`, `.cursor/rules/*.mdc`, `.github/instructions/*.instructions.md` and `.devin/rules/*.md`. A CI drift check catches stale copies. Then run the REPO SCAN prompt. It inspects project files, infers the architecture with evidence, picks an exemplar, and writes "UNKNOWN – ask tech lead" items instead of guessing.

---

## Key Findings

1. **Kiro's model fits this problem well.**
   - The three foundation files are included in every interaction by default.
   - Other steering files are scoped with front matter: `always` (the default), `fileMatch` plus `fileMatchPattern` (one glob or an array), `manual` (pulled in with `#file-name` or a slash command), and `auto` (needs `name` and `description`; loads when the request matches the description).
   - Kiro reads AGENTS.md from the workspace root and subdirectories. AGENTS.md is always included and has no inclusion modes.
2. **Two Kiro gotchas matter for teams.**
   - Custom agents do **not** load steering automatically. You must add `"resources": ["file://.kiro/steering/**/*.md"]`.
   - When global steering (`~/.kiro/steering/`) and workspace steering conflict, the workspace file wins. You can push an org-wide "iOS baseline" via MDM and still let each repo override it.
3. **Specs connect functional requirements to code.**
   - A Kiro spec is `requirements.md` (user stories plus EARS criteria, `WHEN … THE SYSTEM SHALL …`), `design.md` and `tasks.md`.
   - If architecture docs already exist, use the Design-first variant.
   - Bugfix specs use `bugfix.md` with Current / Expected / Unchanged behaviour (`SHALL CONTINUE TO`).
   - Kiro can derive property-based tests from EARS requirements.
4. **AGENTS.md is the cross-tool lowest common denominator, but tools read it differently.**
   - It is plain Markdown, the nearest file wins, and it is used by tens of thousands of open-source projects.
   - OpenAI contributed it on December 9, 2025 to the Agentic AI Foundation under the Linux Foundation, alongside Anthropic and Block, with support from Google, Microsoft, AWS, Bloomberg and Cloudflare.
   - Claude Code reads CLAUDE.md and recommends a one-line `@AGENTS.md` import as the bridge.
   - Cursor combines nested AGENTS.md files with their parents.
5. **Swift is a known weak spot for LLMs.**
   - Paul Hudson's "What to fix in AI-generated Swift code" catalogues deprecated APIs (`foregroundColor()` → `foregroundStyle()`, `cornerRadius()` → `clipShape(.rect(cornerRadius:))`, the 1-parameter `onChange()`), old GCD patterns and hallucinated APIs.
   - Better Stack's "AI Showdown: Which Model Can Actually Code a Swift App?" (February 2026, seven models tested) names two causes: a data gap (much production Swift is proprietary) and API drift (models emit 2022-era syntax that is now deprecated).
   - The remedy is explicit version facts plus an exemplar feature.
6. **Concurrency defaults changed recently.**
   - Swift 6.2 added default `@MainActor` isolation (SE-0466).
   - SE-0461 runs `nonisolated async` functions on the caller's actor (`nonisolated(nonsending)`); `@concurrent` is the opt-out.
   - Secondary sources report that new Xcode 26 projects enable MainActor default isolation and approachable concurrency by default, while existing projects must opt in per target.
   - The scan must read these settings, not assume them.

---

## 1. Master checklist: what an AI needs to generate correct iOS code

**P0**: without it, code usually fails to compile or violates the architecture. **P1**: it compiles but doesn't fit. **P2**: polish. The last column names the template file that holds the item.

### 1.1 Project facts

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 1 | Swift language version (`SWIFT_VERSION`, `swift-tools-version`) | P0 | Uses syntax or features the compiler rejects (typed throws, `sending`, macros), or outdated idioms | tech |
| 2 | Xcode version (local + CI) | P0 | APIs or build settings missing from the SDK | tech |
| 3 | Minimum deployment target per platform | P0 | `@Observable` (iOS 17) or `NavigationStack` (iOS 16) used below the target without `#available`, so the build breaks | tech |
| 4 | Concurrency settings: strict checking, Default Actor Isolation, Approachable Concurrency, upcoming features | P0 | Missing or redundant `@MainActor`, Sendable errors, data races | tech, architecture |
| 5 | Targets, schemes, configurations, app extensions | P0 | Files land in the wrong target; `UIApplication.shared` used in an extension | structure |
| 6 | Project generator (raw `.xcodeproj`, Tuist, XcodeGen, pure SPM) | P0 | Corrupt `pbxproj` hand-edits, or edits wiped by `tuist generate` | structure |
| 7 | Package managers (SPM, CocoaPods, Carthage) and local packages | P0 | SPM dependency added to a Pods-only target; missing `import` | tech |
| 8 | Approved third-party dependencies with versions | P0 | Invented or duplicate libraries; existing ones reinvented | tech |
| 9 | Platforms, devices, orientations | P1 | iPhone-only layouts in an iPad app | product |

### 1.2 Architecture rules

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 10 | Dominant pattern (MVVM/TCA/Clean/VIPER/MVC/RIBs/hybrid) and where each is used | P0 | Generic "MVVM + ViewModel" dropped into a TCA codebase | architecture |
| 11 | Layers and **allowed dependency direction** | P0 | Views calling `URLSession`; domain importing UIKit | architecture |
| 12 | Module boundaries, public API surface, import rules | P0 | Circular imports; `internal` symbols used across modules | architecture, structure |
| 13 | DI mechanism (init injection, Environment, swift-dependencies, Factory, Swinject, Needle) | P0 | Singletons everywhere; untestable code | architecture |
| 14 | Navigation (NavigationStack path, coordinators, routers, TCA stack navigation, UIKit nav, deep links) | P0 | Direct pushes where a coordinator or route enum is required | architecture |
| 15 | State management (`@Observable` vs `ObservableObject`, TCA, Combine) | P0 | Mixed property wrappers; duplicated state | architecture |
| 16 | Concurrency model (async/await vs Combine vs GCD; actors; `@MainActor` policy; Task cancellation) | P0 | GCD in async code; leaked unstructured `Task {}`; UI updates off the main actor | architecture |
| 17 | UI framework policy (SwiftUI-only/UIKit-only/mixed) and bridging rules | P0 | `UIColor` in SwiftUI views; SwiftUI in UIKit-only modules | architecture |
| 18 | Error model (domain error enums, typed throws, user-facing mapping) | P1 | `print(error)`; swallowed errors | conventions |
| 19 | Persistence (SwiftData/Core Data/GRDB/Realm) and migration rules | P1 | A second persistence stack; skipped migrations | architecture |

### 1.3 Conventions

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 20 | Naming (types, files, protocols, tests, feature folders) | P1 | Inconsistent, hard-to-grep names | conventions |
| 21 | Folder layout per feature | P0 | Files dumped at the root | structure |
| 22 | SwiftLint/SwiftFormat configs and how to run them | P1 | CI lint failures; noisy diffs. Leave formatting to tools, not prose | conventions |
| 23 | Access control (`internal` default, `public` only at module API, `final`) | P1 | Everything `public`, or nothing visible across modules | conventions |
| 24 | Logging (OSLog `Logger`, privacy redaction) and analytics | P1 | `print`; PII in logs | conventions |
| 25 | Localization (String Catalogs, `String(localized:)`, SwiftGen) | P1 | Hard-coded English | conventions |
| 26 | Accessibility (labels, Dynamic Type, hit targets, UI-test identifiers) | P1 | Unlabeled buttons, fixed fonts. A documented LLM weakness | conventions |
| 27 | Design system tokens and shared components | P1 | Raw hex colors, one-off buttons | conventions, exemplars |
| 28 | Doc and comment style (DocC, `// MARK:`) | P2 | Noise | conventions |

### 1.4 Existing code context

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 29 | **Golden-path exemplar**: paths to every file of one vertical slice (view → state/VM/reducer → use case → repository → API client → DTO → mapper → tests → DI → navigation) | P0 | One concrete example beats pages of rules. Without it you get "textbook" code that doesn't match the repo | exemplars |
| 30 | Networking entry point (client, endpoint style, auth refresh, retries) | P0 | A new `URLSession` wrapper per feature | api-contracts |
| 31 | Persistence entry point | P1 | A parallel store | architecture |
| 32 | Shared infrastructure catalog (flags, analytics, images, keychain, config) | P1 | Duplicated utilities | exemplars |
| 33 | Do-not-touch zones (generated, vendored, legacy) | P0 | Destructive edits | structure |

### 1.5 Contracts

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 34 | API spec location (OpenAPI/GraphQL) and codegen tool | P0 | Hallucinated JSON keys | api-contracts |
| 35 | DTO vs domain separation and where mapping lives | P0 | DTOs leaking into views | api-contracts |
| 36 | Decoding strategy (key/date strategies, unknown enum cases) | P1 | Runtime decode failures | api-contracts |
| 37 | Environments (xcconfig base URLs per configuration) | P1 | Hard-coded production URLs | api-contracts |
| 38 | Feature-flag system and naming | P1 | Unflagged features | api-contracts |
| 39 | Error contract (HTTP → domain, retry, offline) | P1 | Generic alerts | api-contracts |

### 1.6 Quality gates

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 40 | Test framework per target: XCTest vs Swift Testing (`@Test`, `#expect`) | P0 | XCTest assertions inside Swift Testing files | testing |
| 41 | Mocking approach (protocol mocks, Mockolo/Sourcery, dependency test values) | P0 | Invented mocking libraries | testing |
| 42 | Snapshot and UI testing (swift-snapshot-testing, XCUITest identifiers) | P1 | Broken or missing snapshots | testing |
| 43 | Exact build, test and lint commands (`xcodebuild`, `swift test`, fastlane, `tuist test`) | P0 | "Done" on code that was never compiled | tech, testing |
| 44 | Coverage expectations per layer | P1 | Untested logic | testing |
| 45 | CI pipeline and required checks | P1 | PRs that fail CI | testing |
| 46 | PR checklist / Definition of Done | P1 | Missing localization, accessibility or tests | testing |

### 1.7 Security and privacy

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 47 | Secret handling (xcconfig + CI secrets; never print or commit) | P0 | Hard-coded API keys | conventions |
| 48 | Keychain wrapper for tokens and credentials | P0 | Tokens in UserDefaults | conventions |
| 49 | ATS policy | P1 | `NSAllowsArbitraryLoads` added "to make it work" | conventions |
| 50 | Info.plist permission strings policy | P1 | Missing or placeholder `NS…UsageDescription`, then App Review rejection | conventions |
| 51 | Entitlements and privacy manifest (`PrivacyInfo.xcprivacy`, required-reason APIs) | P1 | Store compliance failures | conventions |
| 52 | PII and data-classification rules | P1 | PII in analytics or logs | conventions |

### 1.8 Process

| # | Item | Pri | Why / what goes wrong without it | File |
|---|---|---|---|---|
| 53 | How functional requirements map to specs (one spec per feature, naming) | P0 | Monolithic, unreviewable specs | product |
| 54 | EARS writing rules and acceptance-criteria format | P0 | Untestable "should work well" criteria | requirements template |
| 55 | Task granularity (each task leaves the app compiling; tests in the same task) | P0 | Big-bang changes that don't build | tasks template |
| 56 | Which architecture docs/ADRs are authoritative | P1 | Agent follows a stale doc | architecture |
| 57 | Stop-and-ask rules (new dependency, schema change, permission, project restructure) | P0 | Silent risky changes | product |
| 58 | Branch, commit and PR conventions | P2 | Messy history | conventions |

---

## 2. The Kiro template file set

All files below are shipped in this kit under `docs/ai/` (canonical) and `.kiro/steering/` (with Kiro front matter). Spec templates are in `.kiro/specs/_template/`.

### 2.1 Package layout

```text
repo-root/
├── AGENTS.md                 # generated thin index (cross-tool)
├── CLAUDE.md                 # "@AGENTS.md" + Claude-only notes
├── docs/ai/                  # CANONICAL source of truth (no tool front matter)
│   ├── product.md  tech.md  structure.md  architecture.md
│   ├── conventions.md  testing.md  api-contracts.md  exemplars.md
│   ├── ios-api-guardrails.md  repo-scan-prompt.md  scan-report.md
│   └── ai-files.yaml         # canonical file → scope mapping
├── .kiro/steering/           # generated: docs/ai + Kiro front matter
├── .kiro/specs/<feature>/{requirements,design,tasks}.md
├── .kiro/hooks/*.json
├── .claude/rules/*.md        # generated (paths:)
├── .cursor/rules/*.mdc       # generated (description/globs/alwaysApply)
├── .github/instructions/*.instructions.md   # generated (applyTo)
├── .devin/rules/*.md         # generated (Windsurf trigger:)
└── scripts/ai-sync.sh        # generator + --check for CI
```

### 2.2 Inclusion-mode plan

| Steering file | Kiro inclusion | Rationale |
|---|---|---|
| `product.md`, `tech.md`, `structure.md` | `always` | Foundation files. Small, and needed every time |
| `architecture.md` | `always` | Prevents most structural mistakes. Keep it under about 120 lines |
| `conventions.md`, `ios-api-guardrails.md` | `fileMatch` `**/*.swift` | Only needed when touching Swift |
| `testing.md` | `fileMatch` on test paths | Loads when tests are written |
| `api-contracts.md` | `fileMatch` on networking/data paths | Data-layer work |
| `exemplars.md` | `auto` (or `manual`) | Pulled in for "build a feature" requests; reference it with `#exemplars` in spec sessions |
| `repo-scan.md` | `manual` | Runbook, invoked with `/repo-scan` |

Use `fileMatchPattern`, the key in the official docs. Some community posts show `fileMatch:`, which is not the documented key.

### 2.3 EARS patterns for `requirements.md`

- Ubiquitous: `THE … SHALL`
- Event-driven: `WHEN …`
- State-driven: `WHILE …`
- Unwanted behaviour: `IF … THEN …`
- Optional feature: `WHERE …`

Each criterion states one testable behaviour and gets an ID that tests reference.

For bugs, use Kiro's Bugfix spec with three sections: Current (`WHEN … THEN the app …`), Expected (`… SHALL …`), Unchanged (`… SHALL CONTINUE TO …`) — the regression guard.

### 2.4 Optional Kiro hooks

Useful iOS hooks: lint/format on save; a localization-check prompt when `Localizable.xcstrings` changes; a "steering may be stale" reminder when `Package.resolved`, `project.pbxproj` or CI config changes.

Caveats: file triggers fire only on changes the agent makes; agent-prompt hooks consume credits; the schema differs across versions (CLI V3 uses standalone versioned JSON, the older IDE used `*.kiro.hook`). Generate the first hook with "Ask Kiro to create a hook" and copy whatever schema it emits.

---

## 3. Tool-portability mapping

| Tool | Location(s) | Format / scoping | Limits & quirks |
|---|---|---|---|
| **Kiro** | `.kiro/steering/*.md`; global `~/.kiro/steering/`; `AGENTS.md` (root and subdirectories); specs `.kiro/specs/`; hooks `.kiro/hooks/` | YAML `inclusion: always/fileMatch/manual/auto`; `fileMatchPattern` (string or array); `auto` needs `name` + `description` | Workspace beats global. Custom agents need `resources`. AGENTS.md is always included. CLI V1/V2 support inclusion modes only partially (V3 fully). Web can't read `~/.kiro` |
| **Claude Code** | `CLAUDE.md` / `.claude/CLAUDE.md`, `CLAUDE.local.md`, `~/.claude/CLAUDE.md`, `.claude/rules/**/*.md` | Markdown; `@path` imports; rules use `paths:` (the only field read) and load on demand | Under 200 lines is a soft target; very long files get partially ignored. Imports organise but don't save context. Doesn't read AGENTS.md natively, so use `@AGENTS.md` |
| **Cursor** | `.cursor/rules/**/*.mdc`; `AGENTS.md` (root and subdirectories); legacy `.cursorrules`; User/Team rules | `.mdc` with `description`, `globs`, `alwaysApply`. Modes: Always / Apply Intelligently / Specific Files / Manual (`@rule`) | Keep rules under 500 lines. Plain `.md` in the rules dir is ignored. `alwaysApply: true` ignores globs. Nested AGENTS.md combines with parents |
| **GitHub Copilot** | `.github/copilot-instructions.md`; `.github/instructions/**/*.instructions.md`; `AGENTS.md`; also `CLAUDE.md`/`GEMINI.md` | Markdown; `applyTo:` glob; optional `excludeAgent` | Code review's former 4,000-character cap on instruction files was removed on GitHub in June 2026; Azure Repos review preview still documents it. Review reads base-branch instructions. `@file` expands only in the root-style files |
| **AGENTS.md** | Root plus nested per package | Plain Markdown, no required fields; nearest file wins; chat prompt overrides | How nested files combine varies by tool, so test it |
| **Windsurf** (Cognition/Devin) | `.devin/rules/*.md` (preferred), `.windsurf/rules/*.md`, legacy `.windsurfrules`, `global_rules.md`, `AGENTS.md` | `trigger: always_on/model_decision/glob/manual`, `globs`, `description`. Nested AGENTS.md acts as a glob rule | Official docs give per-file limits only: workspace rules 12,000 characters per file, `global_rules.md` 6,000; no combined cap listed |
| **Xcode 26.3+** (Claude Agent, Codex; Gemini/ACP reported from 26.6) | Apple: AGENTS.md/CLAUDE.md, skills and MCP config go in `~/Library/Developer/Xcode/CodingAssistant/codex` and `…/ClaudeAgentConfig`. Community reports a project-root CLAUDE.md is also detected | Same as Codex / Claude Code | Agents get build, test, preview and Apple-docs tools via MCP. External CLIs connect with `xcrun mcpbridge`. The per-user directories sit outside the repo, so add a sync step. Pre-26.3 "ChatGPT in Xcode" chat has no repo instruction file: attach `docs/ai/*` manually |

### 3.1 Single-source-of-truth strategy

1. **Canonical text lives in `docs/ai/*.md`** with no tool front matter. `ai-files.yaml` declares each file's scope.
2. **`scripts/ai-sync.sh` generates the adapters.** Each scope maps to one native field per tool:

   | Scope | Kiro | Claude | Cursor | Copilot | Windsurf |
   |---|---|---|---|---|---|
   | always | `inclusion: always` | content in AGENTS.md | `alwaysApply: true` | content in AGENTS.md | `always_on` |
   | glob | `fileMatch` + `fileMatchPattern` | `paths:` | `globs` | `applyTo` | `glob` |
   | auto | `auto` + `name` + `description` | `description` → rule | `description` | — | `model_decision` |
   | manual | `manual` | — | `@rule` | — | `manual` |

   Also generate a root `AGENTS.md` (always-files only, under about 150 lines, linking to `docs/ai/`) and a `CLAUDE.md` containing `@AGENTS.md`.
3. **Prefer imports and generated copies over symlinks.** Symlinks break on Windows checkouts, and Kiro and Cursor need front matter the canonical files lack. Symlinking `CLAUDE.md → AGENTS.md` is an acceptable shortcut.
4. **CI drift check.** `ai-sync.sh --check` fails the build when generated files differ. Re-run the REPO SCAN in diff mode whenever `Package.resolved`, `project.pbxproj` or CI config changes.
5. **Org baseline.** Ship guardrails and security rules as global/team steering in `~/.kiro/steering/` via MDM (Kiro's documented pattern). Repos override them because workspace wins.

**Off-the-shelf generators** if you'd rather not maintain a script: `rulesync` (dyoshikawa; `.rulesync/` source, `--check` for CI, 20+ tools), `ruler` (`.ruler/` plus `ruler.toml`), `onerule` (AGENTS.md as source, CLAUDE.md as `@AGENTS.md` import, fails CI on drift). Check Kiro `inclusion`/`auto` support before adopting any of them.

---

## 4. The REPO SCAN prompt

Shipped as `docs/ai/repo-scan-prompt.md` (and `.kiro/steering/repo-scan.md` with `inclusion: manual`, invoked with `/repo-scan`). It:

- Is read-only, cites evidence (path:line or command output) for every value, and writes `UNKNOWN – ask tech lead: <question>` instead of guessing. Never prints secret values.
- Step 0 inventories the repo (project files, package manifests, lint configs, CI configs, plists, entitlements, OpenAPI specs, existing AI instruction files, ADRs) and git hot-spots.
- Step 1 reads toolchain facts via `xcodebuild -showBuildSettings` (fallback: grep pbxproj/xcconfig) including concurrency settings, plus Package.swift and lockfiles.
- Step 2 maps targets, project generator, module import graph, generated/vendored paths.
- Step 3 detects entry point and classifies SwiftUI-only / UIKit-only / Mixed, and which kind of screen is being added recently.
- Step 4 scores architecture patterns (TCA, MVVM, Clean, VIPER, RIBs, MVC, custom Redux, modular SPM) by signal counts with confidence levels and conflicts vs ADRs.
- Step 5 detects DI, navigation, concurrency style, networking, persistence, logging, analytics, flags, l10n, design system, and security-relevant paths.
- Step 6 detects test frameworks, mocking style, snapshot/UI tests, coverage and CI checks.
- Step 7 scores and picks the golden-path exemplar (dominant pattern, full vertical slice, tested, recently touched but not highest-churn, 5–15 files, few suppressions) plus anti-exemplars.
- Step 8 outputs the filled `docs/ai/*.md`, a `scan-report.md` with evidence tables, and the UNKNOWN checklist.

---

## 5. Failure modes of AI-generated iOS code and how the template prevents them

| Failure mode | Symptom | Template control |
|---|---|---|
| Hallucinated APIs | Plausible modifiers or initializers that don't exist | Guardrail "verify via Apple docs" (Xcode 26.3 agents can search Apple documentation); build command in `tech.md` so the agent compiles before claiming done |
| Wrong deployment-target APIs | `@Observable`, `Tab`, newer modifiers used below their OS version | Exact target plus the `#available` rule in `tech.md` |
| Deprecated or legacy idioms | `foregroundColor`, `NavigationView`, `ObservableObject`, `DispatchQueue.main.async` | `ios-api-guardrails.md` (from Hudson's catalogue and SwiftAgents rules) |
| Mixed UIKit/SwiftUI idioms | `UIColor` in SwiftUI; view controllers in SwiftUI-only modules | UI policy and bridging rules in `architecture.md` |
| Ignoring main-actor isolation | Off-main UI mutation, redundant `@MainActor`, Sendable errors | Scanned concurrency settings plus the concurrency section; optional skills (twostraws "Swift Concurrency Pro", AvdLee Swift-Concurrency-Agent-Skill) |
| Broken module boundaries | Feature imports another feature; Domain imports UIKit | Import rules in `structure.md`, dependency direction in `architecture.md`, build verification |
| Bypassed networking layer | New `URLSession` calls per feature | `api-contracts.md` entry point; exemplar data layer |
| Invented dependencies | `import Alamofire` in a repo without it | Dependency allow-list plus the stop-and-ask rule |
| Hand-edited generated projects | Broken `project.pbxproj`; lost Tuist changes | Project-generation rule and do-not-touch list |
| Secret and privacy slips | Keys in code; tokens in UserDefaults; missing usage strings | Security section; scan flags secret-bearing paths |
| "Done" without verification | Code never compiled | Final verify task; DoD; optional lint/build hook |
| Accessibility gaps | Unlabeled icon buttons, fixed fonts | Accessibility rules plus EARS accessibility criteria |

**Community rule sets: borrow, don't adopt wholesale.**
- **twostraws/SwiftAgents** targets iOS 26 / Swift 6.2, forbids new third-party frameworks without asking, and avoids UIKit unless requested. Adjust it for older targets and UIKit repos.
- **twostraws/SwiftUI-Agent-Skill** ("swiftui-pro") and **AvdLee's SwiftUI and Swift Concurrency skills** are useful optional add-ons.
- **awesome-cursorrules "SwiftUI Guidelines"** is dated (2024) and hard-codes a folder layout. Your scan-derived `structure.md` should override it.

Layer all of these as `manual`/`auto` skills on top of repo-specific facts, never in place of them.

---

## 6. Branching out to hybrid stacks

**What stays the same:** the checklist groups; the Kiro file set and inclusion strategy; EARS specs and the exemplar concept; the single-source generator and the stop-and-ask rules; the scan output format (filled templates plus the UNKNOWN list).

**What changes:**

| Area | React Native / Expo | Flutter | KMP | Capacitor |
|---|---|---|---|---|
| Version facts | RN, New Architecture, Expo SDK, Hermes, Node/pnpm | Flutter channel/version, Dart SDK, FVM | Kotlin/K2, Gradle/AGP, iOS framework export (XCFramework/SPM/Pods) | Capacitor major, web framework |
| Files to scan | `package.json`, lockfile, `app.config.ts`, `ios/Podfile`, `metro.config.js`, `tsconfig.json` | `pubspec.yaml/.lock`, `analysis_options.yaml`, `ios/Podfile`, `lib/` | `settings.gradle.kts`, `build.gradle.kts`, `shared/src/{commonMain,iosMain}`, `iosApp/` | `capacitor.config.ts`, `ios/App/` |
| Architecture signals | Redux Toolkit/Zustand/React Query; React Navigation vs Expo Router | Riverpod/Bloc/Provider; go_router; freezed | expect/actual, shared ViewModels, SKIE, Koin | Web architecture plus plugins |
| Native-boundary rules | Native modules only via a wrapper dir; native changes need a new dev build; OTA can't ship native code | Plugins with native code need a full rebuild; platform channels in one place | Swift-facing API shape (suspend → async via SKIE); what stays in Swift | Native edits only in `ios/App` |
| Commands | `npx expo run:ios`, `npx expo install`, jest/detox | `flutter analyze` (clean), `flutter test`, `flutter build ipa` | `./gradlew :shared:allTests` + `xcodebuild` | `npx cap sync ios` |
| Official agent assets | `create-expo-app` writes an AGENTS.md pointing to version-matched docs | docs.flutter.dev/ai rules plus the `flutter/agent-plugins` marketplace | Community only | Community only |

Pattern: a root AGENTS.md (or Kiro `always` files) holds cross-cutting facts, and nested AGENTS.md or `fileMatch` steering lives per platform folder (`ios/`, `android/`, `shared/`). Every tool here resolves "nearest file wins" or glob scoping, so the native-iOS files from this kit apply unchanged inside `ios/` and `iosApp/`.

---

## Recommendations

1. **Pilot one repo in week 1.** Commit the templates and the scan prompt. Run the scan in Kiro (`/repo-scan`) and separately in Claude Code or Cursor, then diff the outputs — disagreement flags ambiguous code. Resolve every UNKNOWN in a 30-minute review.
2. **Lock the exemplar.** A senior engineer should approve, or deliberately clean up, the golden-path feature. It is the highest-leverage artifact in the kit.
3. **Keep always-on context small.** Four always-files of under about 120 lines each; everything else goes to `fileMatch`/`auto`/`manual`.
4. **Enforce spec discipline.** Design-first specs when an architecture doc exists; EARS criteria with IDs mapped to tests; Bugfix specs with `SHALL CONTINUE TO` for regressions.
5. **Automate drift control.** Run `ai-sync.sh --check` in CI, and flag changes to `Package.resolved`, `project.pbxproj` or CI config as "steering may be stale".
6. **Scale out.** Publish guardrails and security rules org-wide as global/team steering. New repos then only run the scan.
7. **Measure.** Track first-pass build success, lint violations and review-comment categories on AI PRs. Turn each recurring failure into a one-line guardrail.

## Caveats

- **Tool behaviour moves fast.** Kiro's hook schema differs between IDE and CLI V3, and V1/V2 support inclusion modes only partially. Windsurf now prefers `.devin/rules/`. Copilot's 4,000-character review cap was removed on GitHub but is still documented for Azure Repos. Re-verify against current docs when you adopt the kit.
- **The Xcode 26 concurrency template defaults (MainActor isolation, Approachable Concurrency on) come mostly from secondary sources, and an early beta behaved differently.** The setting key `SWIFT_DEFAULT_ACTOR_ISOLATION` also comes only from community reports. That is why the scan reads settings rather than assuming them.
- **Every vendor treats instructions as best-effort.** The real enforcement is compile, test and lint gates plus human review of architecture-touching changes. Version numbers and simulator names in the examples (such as `iPhone 17`) are placeholders the scan must replace.

## Sources

- https://kiro.dev/docs/steering/
- https://kiro.dev/docs/specs/feature-specs/
- https://kiro.dev/blog/specs-bugfix-and-design-first/
- https://kiro.dev/docs/specs/bugfix-specs/
- https://kiro.dev/docs/specs/correctness/
- https://kiro.dev/docs/specs/best-practices/
- https://kiro.dev/docs/hooks/
- https://kiro.dev/docs/hooks/types/
- https://kiro.dev/docs/cli/v3/hooks/
- https://kirotutorial.com/concepts/steering/
- https://www.memorylake.ai/en/blogs/split-kiro-steering-for-ide-and-cli
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/best-practices
- https://www.alexdunlop.com/writing/claude-md-best-practices
- https://cursor.com/docs/rules
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- https://docs.github.com/en/copilot/tutorials/customize-code-review
- https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/
- https://github.blog/changelog/2026-06-12-copilot-code-review-new-configurations-and-controls/
- https://devblogs.microsoft.com/devops/copilot-code-reviews-for-azure-repos-public-preview/
- https://aaif.io/blog/writing-an-effective-agents-md
- https://aq.dev/glossary/agents-md/
- https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/
- https://markdific.com/guides/windsurf-rules/
- https://terminalskills.io/skills/windsurf-rules
- https://www.hackingwithswift.com/articles/281/what-to-fix-in-ai-generated-swift-code
- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-control-default-actor-isolation.md
- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md
- https://www.massicotte.org/concurrency-glossary/
- https://github.com/twostraws/SwiftAgents/blob/main/AGENTS.md
- https://github.com/twostraws/swiftui-agent-skill
- https://github.com/twostraws/Swift-Concurrency-Agent-Skill
- https://www.avanderlee.com/ai-development/agent-skills-replacing-agents-md-with-reusable-ai-knowledge/
- https://developer.apple.com/forums/thread/815576
- https://developer.apple.com/videos/play/tech-talks/111428
- https://anthropic.com/news/apple-xcode-claude-agent-sdk
- https://dev.to/arshtechpro/xcode-263-use-ai-agents-from-cursor-claude-code-beyond-4dmi
- https://docs.flutter.dev/ai/get-started
- https://github.com/evanca/flutter-ai-rules
- https://expo.dev/articles/choosing-a-mobile-stack/which-mobile-stack-for-ai-coding-agents
- https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax
