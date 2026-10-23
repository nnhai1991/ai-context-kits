# Android AI-Context Template Kit: Kiro Steering, Specs, Repo-Scan Prompt and Portability Guide (October 2026)

This package gives an AI coding assistant what it needs to write correct code in any Android repository. Use one canonical `docs/ai/` source and generate `.kiro/steering/*.md` (the primary target) from it, plus `AGENTS.md` (read by Android Studio Gemini, Junie, Copilot, Cursor, Windsurf, and by Claude Code via `@AGENTS.md`). Every architecture-specific value is a `{{PLACEHOLDER}}`. A repo-scan prompt fills those placeholders and flags anything it cannot prove as "UNKNOWN – ask tech lead". The structure mirrors the iOS kit: checklist → Kiro file set → portability → repo scan → evidence and failure modes → hybrid.

## TL;DR

- **What matters most:** exact versions (Kotlin, AGP, compileSdk/minSdk/targetSdk, Compose BOM, KSP vs kapt), the real architecture discovered by scanning, one golden-path exemplar slice, and the exact Gradle commands that define "done". Without these, models produce plausible but wrong Android code: deprecated or hallucinated APIs, unguarded newer API calls, made-up dependencies, broken UDF. A FSE Companion '25 study (Chen et al., MARIN) of one industrial project measured ~12.75% hallucination for third-party library APIs vs ~85% for project-specific APIs — your own code is where the model is weakest.
- **How to structure it:** small always-on core (`product.md`, `tech.md`, `structure.md`, short `architecture.md`); everything else in `fileMatch`/`auto` steering scoped by Android globs. Requirements go in Kiro specs (EARS `requirements.md` / `bugfix.md` → `design.md` → `tasks.md`), with Kiro hooks as automated gates. Keep always-on under ~200 lines total; Windsurf caps workspace rule files at 12,000 characters.
- **How to stay portable:** `docs/ai/` is canonical; `scripts/ai/generate.py` emits each tool's format; CI fails on drift. 2026 baselines to verify per repo: Kotlin 2.4.x, AGP 9.x (built-in Kotlin), KSP2 only (KSP1 removed; kapt in maintenance), Compose BOM 2026.09.00, Navigation 3 (1.2.0), targetSdk 36 (Play requires API 36 for new apps/updates from Aug 31, 2026; lower floors for Wear/Auto 35 and TV/XR 34).

## Key Findings

1. **Kiro's model fits well, but its rules are strict.** Inclusion modes: `always` (default), `fileMatch` + `fileMatchPattern` (string or array), `manual` (`#name` / slash command), `auto` (needs `name` + `description`). Front matter must be the very first content in the file. Kiro also reads `AGENTS.md` (root + subdirs, always included) and supports live refs `#[[file:gradle/libs.versions.toml]]`. Custom agents do not load steering automatically — add `"resources": ["file://.kiro/steering/**/*.md"]`.
2. **Specs map onto "functional requirements + architecture docs".** Requirements-First or Design-First (use Design-First when architecture docs exist). Bugfix specs use `bugfix.md` with Current / Expected / Unchanged (`SHALL CONTINUE TO`). "Run all tasks" builds a dependency graph and runs independent tasks in parallel, so task granularity and stated dependencies matter.
3. **Hooks can enforce, not just suggest.** `.kiro/hooks/*.json` (`"version": "v1"`); triggers include `PreToolUse`, `PreTaskExec`, `PostTaskExec`, `PostFileSave`, `Stop`. A command action exiting with code 2 blocks `PreToolUse`. Use it to block edits to generated sources, `local.properties`, keystores. File triggers fire only for agent-made changes.
4. **Android Studio's agent is a first-class AGENTS.md consumer.** It scans the current and all parent directories and prepends the content; supports `@./file.md` imports; `GEMINI.md` in the same dir wins over `AGENTS.md`. IDE "Rules" live in `.idea/project.prompts.xml`; skills in `.agents/skills` or `.android-studio/skills`; `.aiexclude` keeps files out of context. Google's Now in Android ships a 58-line `AGENTS.md` with flavors, exact Gradle commands, test libs and CI rules — the best public reference for tone and density. (Note: NiA's AGENTS.md still says Navigation 2 while the code moved to Navigation 3 — a live example of why the scan must check code, not docs.)
5. **Google's architecture guidance gives defaults; the scan decides.** UDF is "strongly recommended": ViewModel exposes `uiState` via `stateIn(WhileSubscribed(5000))`, receives actions via method calls, is lifecycle-agnostic; ViewModel-originated events should become UI state updates. The template states these as defaults that apply only when the scan finds no established house pattern (MVI/Orbit, Circuit, Decompose, RxJava).
6. **The 2026 toolchain changed in ways earlier-trained models get wrong.** AGP 9 enables built-in Kotlin by default, so `org.jetbrains.kotlin.android` is incompatible with the new DSL (opt-out `android.builtInKotlin=false` goes away in AGP 10). KMP modules must use `com.android.kotlin.multiplatform.library`. KSP1 is removed; Room 3 is KSP-only; Compose 1.12 needs compileSdk 37 and AGP 9. Each needs an explicit line in `tech.md` / `android-api-guardrails.md`.

---

## 1. The Information Checklist (P0 / P1 / P2)

P0: code won't compile, won't fit, or is unsafe without it — fill before any spec runs. P1: compiles but fails review — fill in week one. P2: polish.

### 1a. Project facts

| ID | P | Item | Why / what goes wrong without it |
|---|---|---|---|
| PF-01 | P0 | Kotlin version + K2, language/API level | Syntax that won't compile or misses newer idioms |
| PF-02 | P0 | AGP + Gradle versions; built-in Kotlin on/off (`android.builtInKotlin`, `android.newDsl`) | Pre-AGP-9 models add `kotlin("android")` and old variant APIs, breaking the build |
| PF-03 | P0 | JDK toolchain (`jvmToolchain`, `JavaVersion`) | jvmTarget mismatch errors |
| PF-04 | P0 | compileSdk / minSdk / targetSdk (per module) | Unguarded newer API calls → `NoSuchMethodError`; targetSdk 36 behaviour changes (edge-to-edge, predictive back) |
| PF-05 | P0 | UI toolkit (Compose/Views/mixed); Compose BOM; compiler plugin | Hallucinated or removed Compose/Material3 APIs; missing interop rules |
| PF-06 | P0 | `libs.versions.toml` aliases + "catalog only" rule | Raw coordinates, invented versions, duplicate libs |
| PF-07 | P0 | KSP vs kapt per processor | Build failures (KSP1 removed, Room 3 KSP-only) or slow builds |
| PF-08 | P0 | Modules (`settings.gradle.kts`), types, convention plugins | Files in wrong module; raw plugins instead of conventions; circular deps |
| PF-09 | P0 | Build types × flavors; default local variant | Non-existent Gradle tasks; code in wrong source set |
| PF-10 | P1 | Third-party SDK inventory + new-deps policy | Second HTTP client; analytics SDK that breaks Play data-safety |
| PF-11 | P1 | Java/Kotlin interop; "no new Java" rule | Needless ports; missing `@JvmStatic`/nullability |
| PF-12 | P2 | Build perf flags (config cache, build cache, non-transitive R) | Changes that break the configuration cache |

### 1b. Architecture rules

| ID | P | Item | Why / failure |
|---|---|---|---|
| AR-01 | P0 | Pattern actually used: MVVM / MVI (Orbit, MVIKotlin, custom) / Clean / Circuit / Decompose / MVP legacy | Model defaults to "MVVM + Hilt + Retrofit" and generates foreign code |
| AR-02 | P0 | Layers and dependency direction; domain pure Kotlin? | DTOs in composables; Android imports in domain |
| AR-03 | P0 | Module boundaries (`feature:*` → `core:*` only; api/impl split) | Feature-to-feature imports erode modularization |
| AR-04 | P0 | DI framework + scoping (Hilt/Koin/Dagger/Anvil/Metro/manual) | `@HiltViewModel` in a Koin app; singletons holding Activity context |
| AR-05 | P0 | Navigation (Nav3 / Nav2 type-safe / Fragment graphs / Decompose / Voyager / Circuit) | The most hallucination-prone area; Nav2 string routes, Nav2 `@Serializable` and Nav3 `NavKey` are mutually incompatible |
| AR-06 | P0 | State holder contract (`ViewModel` + `StateFlow<UiState>`, MVI container, Circuit Presenter) | State mutated from composables; lost one-off events on rotation |
| AR-07 | P0 | Async model: coroutines/Flow vs RxJava + bridge rules | Leaks and double subscriptions |
| AR-08 | P1 | Dispatcher injection | Hard-coded `Dispatchers.IO`, untestable |
| AR-09 | P1 | One-off events policy (state vs `Channel`/`SharedFlow`) | House rule not followed |
| AR-10 | P1 | Lifecycle-aware collection (`collectAsStateWithLifecycle`, `repeatOnLifecycle`) | Background collection |
| AR-11 | P1 | Process death: `SavedStateHandle`, `rememberSaveable`, serializable nav state | Lost forms/selections |
| AR-12 | P2 | Offline-first / sync (Room source of truth, WorkManager) | Network called from ViewModel |

### 1c. Conventions

| ID | P | Item | Why / failure |
|---|---|---|---|
| CV-01 | P0 | Naming (`XxxScreen`/`XxxRoute`/`XxxViewModel`/`XxxUiState`/`XxxUseCase`/`XxxRepository(Impl)`/`XxxDto`/`XxxEntity`) | Fragmented code |
| CV-02 | P0 | Package layout per module (by feature vs by layer) | Arbitrary packages |
| CV-03 | P0 | Formatter/linter configs + exact fix command (ktlint/Spotless/detekt) | CI style failures, fix loops |
| CV-04 | P1 | Visibility (`internal` default; explicit API mode?) | Public bloat |
| CV-05 | P1 | Error model (`Result<T>`, sealed errors, boundary exceptions) | `runCatching` swallowing `CancellationException` |
| CV-06 | P1 | Logging (Timber; PII rules) | `Log.d` in release; PII leaks |
| CV-07 | P1 | Strings in `strings.xml`; plurals | Breaks localization and lint |
| CV-08 | P1 | Accessibility (`contentDescription`, semantics, 48dp) | Fails a11y audits and semantics-based tests |
| CV-09 | P1 | Theming (Material3/design system tokens; no raw `Color(0xFF…)`) | Off-brand, duplicated components |
| CV-10 | P2 | `@Preview` conventions | Blocks screenshot testing |
| CV-11 | P2 | KDoc/comment policy | Noise |

### 1d. Existing code context

| ID | P | Item | Why / failure |
|---|---|---|---|
| EX-01 | P0 | **Golden-path exemplar slice** (Screen → ViewModel → UseCase → Repository → API → DTO → mapper → Room → DI → nav → tests) | Single best lever; project-specific APIs are where hallucination concentrates |
| EX-02 | P0 | Shared infra entry points (HTTP client, Room DB, DataStore, Coil/Glide, WorkManager factory, analytics, flags) | Second `OkHttpClient`/`RoomDatabase`; direct SDK calls |
| EX-03 | P1 | Design-system component catalog | Rebuilt buttons/cards |
| EX-04 | P1 | Test fakes location (`core:testing`), dispatcher rule | Mocks everything |
| EX-05 | P2 | "Do not copy" legacy areas | Learns from old MVP/AsyncTask code |

### 1e. Contracts

| ID | P | Item | Why / failure |
|---|---|---|---|
| CT-01 | P0 | API contract source (OpenAPI/GraphQL/proto) + codegen location | Invented endpoints; hand-written models that codegen produces |
| CT-02 | P0 | Serialization lib + naming strategy + unknown-key policy | Runtime crashes; R8-stripped adapters |
| CT-03 | P0 | DTO vs domain separation + mapper location | DTOs in UI |
| CT-04 | P1 | Environments (`BuildConfig`, flavors, base URLs) | Hard-coded URLs/secrets |
| CT-05 | P1 | Feature flags (provider, naming, defaults, cleanup) | Ungated features |
| CT-06 | P2 | Pagination/caching/retry conventions | Inconsistent networking |

### 1f. Quality gates

| ID | P | Item | Why / failure |
|---|---|---|---|
| QG-01 | P0 | Exact commands (format, lint, detekt, unit per variant, single test, screenshot verify/record, instrumented) | Model can't self-verify; "finishes" with a red build |
| QG-02 | P0 | Test stack (JUnit4/5, coroutines-test, Turbine, MockK/Mockito, Truth/AssertK, Robolectric) | Tests won't compile |
| QG-03 | P0 | Definition of Done per task | Missing DI bindings / nav registration |
| QG-04 | P1 | UI testing (Compose rule, Espresso, test tags policy) | Fragile text matchers |
| QG-05 | P1 | Screenshot tool + record/verify ownership | Wrong goldens committed |
| QG-06 | P1 | Lint config/baseline + "no new baseline entries" | Suppression instead of fixes |
| QG-07 | P2 | Baseline profiles / macrobenchmark | Startup regressions |
| QG-08 | P1 | CI pipeline on PR | Mismatch local vs CI |

### 1g. Security and privacy

| ID | P | Item | Why / failure |
|---|---|---|---|
| SP-01 | P0 | Secrets via `local.properties`/Gradle props/CI → `BuildConfig`; never committed | Hard-coded keys |
| SP-02 | P0 | R8/ProGuard rules; keep rules for reflection/serialization | Release-only crashes |
| SP-03 | P0 | Runtime permission flow (Activity Result API, rationale) | Missing or deprecated handling |
| SP-04 | P1 | Secure storage (Keystore; replacement for deprecated `EncryptedSharedPreferences`) | Insecure/deprecated storage |
| SP-05 | P1 | `network_security_config.xml`, cleartext, pinning | Cleartext traffic |
| SP-06 | P1 | Play policies (target API, data safety, FGS types, exact alarms) | Unpublishable update |
| SP-07 | P2 | `.aiexclude` / `.kiroignore` | Keystores in AI context |

### 1h. Process

| ID | P | Item | Why / failure |
|---|---|---|---|
| PR-01 | P0 | Spec mapping; Requirements-First vs Design-First | Agent ignores or re-invents design |
| PR-02 | P0 | EARS conventions + requirement IDs traced to tasks/tests | Missing edge cases |
| PR-03 | P0 | Stop-and-ask rules (dependency, module, migration, public API, permission, UNKNOWN) | Silent drift |
| PR-04 | P1 | Task granularity (one layer-slice, ends green, dependencies stated) | Parallel waves collide |
| PR-05 | P1 | Branch/commit conventions | Messy history |
| PR-06 | P2 | Steering maintenance cadence | Stale rules contradict code |

---

## 2. Kiro File Set

All files are shipped in this kit under `docs/ai/` (canonical, tool-neutral front matter) and `.kiro/steering/` (Kiro front matter). Spec templates are in `.kiro/specs/_template/`; hooks in `.kiro/hooks/android-gates.json` + `scripts/ai/block-protected-paths.sh`.

### 2.1 Layout

```text
.kiro/steering/
  product.md tech.md structure.md architecture.md   # always
  conventions.md            # fileMatch **/*.kt, **/*.kts, strings.xml
  testing.md                # fileMatch test source sets
  api-contracts.md          # fileMatch data/network/remote/api, schemas
  android-api-guardrails.md # fileMatch *.kt, manifests, build.gradle.kts, res/xml
  security.md               # fileMatch manifests, proguard, network config, data
  exemplars.md              # auto
  repo-scan.md              # manual (#repo-scan)
.kiro/specs/<feature>/{requirements|bugfix}.md design.md tasks.md
.kiro/hooks/android-gates.json
```

Front-matter rule: `---` must be on line 1 of each file, no blank line or BOM before it, or Kiro ignores the inclusion mode. In Kiro you may replace exemplar paths with live refs `#[[file:path]]`; `tech.md` can embed `#[[file:gradle/libs.versions.toml]]`.

### 2.2 EARS patterns for `requirements.md`

Ubiquitous `THE SYSTEM SHALL`; Event `WHEN …`; State `WHILE …`; Unwanted `IF … THEN …`; Optional `WHERE …`. One testable behaviour per criterion; IDs referenced by tasks and tests. The shipped example is a Saved Payment Methods screen (list/refresh/offline, set default with optimistic revert, delete with default-card rule and flag gate, plus platform-quality criteria for process death, TalkBack and edge-to-edge). Bugfix spec: Current / Expected / Unchanged (`SHALL CONTINUE TO`).

### 2.3 Hooks

`android-gates.json`: `block-protected-files` (PreToolUse → script exits 2 on `build/`, `/generated/`, `local.properties`, `*.jks`, `*.keystore`, `gradle/wrapper/`, `google-services.json`), `format-kotlin-on-save` (PostFileSave), `verify-after-spec-task` (PostTaskExec agent prompt runs detekt/lint/unit tests and checks DI + nav registration), `steering-drift-reminder` (Stop). The `write|edit` matcher and stdin JSON field names are placeholders — confirm against your Kiro version's built-in tool reference.

---

## 3. Tool-Portability Mapping

| Tool | Location | Format / scoping | Limits & quirks (2026) |
|---|---|---|---|
| **Kiro** | `.kiro/steering/*.md`; `~/.kiro/steering/`; `AGENTS.md` (root + subdirs); `.kiro/specs/`; `.kiro/hooks/*.json` | `inclusion: always|fileMatch|manual|auto`; `fileMatchPattern`; `auto` needs `name`+`description`; `#[[file:…]]` | Front matter line 1. Workspace wins over global. Custom agents need `resources`. CLI V1/V2 partial inclusion support (V3 full). AGENTS.md always included |
| **Claude Code** | `CLAUDE.md` / `.claude/CLAUDE.md`; `.claude/rules/**/*.md`; `CLAUDE.local.md` | Rules read only `paths:` (globs, brace expansion); no `paths` = always | <200 lines target; `@path` imports up to 4 hops; reads AGENTS.md only if no CLAUDE.md (v2.1.277+) → put `@AGENTS.md` in CLAUDE.md; invalid YAML → rule loads everywhere |
| **Cursor** | `.cursor/rules/*.mdc`; `AGENTS.md` (root + subdirs) | `description`, `globs`, `alwaysApply` | Plain `.md` in rules dir ignored; `alwaysApply: true` overrides globs; rules don't apply to Tab/inline edit |
| **GitHub Copilot** | `.github/copilot-instructions.md`; `.github/instructions/*.instructions.md`; `AGENTS.md` | `applyTo: "glob,glob"`; `excludeAgent` | Path-specific files apply only to cloud agent and code review on GitHub.com; CLI also reads CLAUDE.md/GEMINI.md |
| **AGENTS.md** | Root + any subdir | Plain Markdown; nearest wins | No glob scoping → use as always-on core; per-module AGENTS.md for module rules |
| **Windsurf / Devin** | `.devin/rules/*.md` (preferred), `.windsurf/rules/*.md`; `~/.codeium/windsurf/memories/global_rules.md`; AGENTS.md | `trigger: always_on|model_decision|glob|manual` | 12,000 chars per workspace rule file; 6,000 global; subdirectory AGENTS.md = auto-glob |
| **Android Studio Gemini / Agent Mode** | `AGENTS.md` (current + parent dirs); `GEMINI.md` (wins in same dir); Rules in `.idea/project.prompts.xml`; skills `.agents/skills` or `.android-studio/skills`; `.aiexclude` | Markdown preamble; `@./file.md` imports | Needs Narwhal 4 Feature Drop Canary 4+ (older: `AGENT.md`); Rules shared only if `.idea` in VCS; Rules + AGENTS.md combined |
| **JetBrains Junie** | `.junie/AGENTS.md` → root `AGENTS.md` + `.junie/playbook.md` + `.junie/rules/*.md` → legacy `.junie/guidelines.md`; `~/.junie/AGENTS.md` | Plain Markdown | If a higher-priority file exists, legacy `guidelines.md` is not read |

### 3.1 Single-source-of-truth strategy

- `docs/ai/*.md` canonical, with tool-neutral front matter (`id`, `scope: always|glob|auto|manual`, `globs`, `description`).
- `scripts/ai/generate.py` emits: `AGENTS.md` (always-files + index of scoped rules), `CLAUDE.md` (`@AGENTS.md`), `.kiro/steering/`, `.claude/rules/` (`paths:`), `.cursor/rules/*.mdc`, `.github/instructions/*.instructions.md` (`applyTo`), `.devin/rules/` (`trigger`), `.junie/rules/`.
- `.github/workflows/ai-context.yml` regenerates and fails on `git diff`, plus checks `tech.md` still names the AGP version in the catalog.
- Always-on content lives in AGENTS.md once; Claude imports it rather than duplicating into `.claude/rules`. Add per-module AGENTS.md only for module-specific rules (Android Studio walks parent dirs). Keep `.idea/project.prompts.xml` Rules minimal so they don't contradict AGENTS.md. Commit generated files — Copilot cloud agent and Kiro Web read only what is in the repo.
- Alternatives if you'd rather not maintain the script: `rulesync`, `ruler`, `onerule` (none target Android Studio `.aiexclude`/Rules).

---

## 4. The REPO SCAN prompt

Shipped as `docs/ai/repo-scan-prompt.md` and `.kiro/steering/repo-scan.md` (`inclusion: manual`, invoke with `#repo-scan`). Read-only; every value cites `path:line` or command output; `UNKNOWN – ask tech lead` instead of guesses; never prints secrets. Steps: 0 inventory + hybrid detection; 1 project facts (incl. built-in Kotlin, KSP/kapt, convention plugins, variants); 2 UI toolkit classification; 3 architecture scoring (MVVM/MVI/Clean/Circuit/Decompose/Voyager/MVP/modular) with CURRENT vs LEGACY; 4 DI; 5 navigation; 6 async/state/lifecycle; 7 data & infra; 8 quality gates; 9 security & release; 10 exemplar selection; 11 output (`scan-report.md`, filled templates, `questions.md`, then STOP).

---

## 5. Failure modes → template defenses

| Failure mode | Root cause | Defense |
|---|---|---|
| Hallucinated Compose APIs / wrong BOM | Training-data version mix | `tech.md` pins BOM; guardrail "only APIs in BOM X; search sources or ask"; DoD requires compiling build + screenshot tests |
| Deprecated APIs (`AsyncTask`, `startActivityForResult`, `onBackPressed`, `LiveData` in new code, synthetics, `EncryptedSharedPreferences`) | Older training data | Forbidden → replacement table scoped to `**/*.kt`; detekt/lint in PostTaskExec hook |
| Unguarded newer APIs vs minSdk | minSdk ignored | minSdk in always-on `tech.md`; guard/`@RequiresApi` rule; `lint` NewApi in DoD |
| Mixing Views and Compose idioms | Toolkit unknown | Scan classifies COMPOSE/VIEWS/MIXED; separate Views section + interop rules |
| Breaking UDF / mutating state from composables | Tutorial code | State-holder contract; `Route`/`Screen` split; VM Turbine tests required |
| Context/View leaks in ViewModel | Convenience | Forbidden row + architecture rule |
| Wrong scope/dispatcher (`GlobalScope`, hard-coded IO, swallowed `CancellationException`, `collectAsState`) | Unclear house rules | Concurrency section, injected dispatcher, lifecycle collection, error rule |
| Ignoring config changes / process death | Not in requirements | Platform-quality EARS requirement; `SavedStateHandle` test; bugfix example |
| Invented dependencies / raw coordinates | Package hallucination (USENIX Sec '25: ~19.7% of recommended packages hallucinated in Python/JS) | `libs.*` only; stop-and-ask; dependencyGuard/catalog check |
| Wrong plugin wiring under AGP 9 | Pre-2026 data | Built-in Kotlin flag + rule; official `agp-9-upgrade` skill for migrations |
| kapt for KSP-capable processor | Old tutorials | Processor table + forbidden row |
| Hand-editing generated files | Agent "fixes" at wrong place | Protected list + PreToolUse blocking hook + `.aiexclude` |
| Missing R8 keep rules → release-only crash | Debug-only verification | R8 rules in api-contracts/security; release build for data-model changes |
| Missing runtime permissions / Play policy | Requirements silent | Permission rule; stop-and-ask on new permissions; data-safety inventory |
| Inaccessible UI | Not prompted | a11y rules, EARS a11y criteria, semantics tests |
| Steering contradicts code | Docs rot | Scan cites evidence; CI drift + version check; Stop hook |

**Community rule sets — borrow, don't adopt wholesale.** Google's official `android/skills` (AGP 9 upgrade, Navigation 3 setup, edge-to-edge, R8, XML→Compose; `android skills add --all`) are good companions for migration tasks. `new-silvermoon/awesome-android-agent-skills` and `krutikJain/android-agent-skills` confirm the single-source + generator pattern but encode generic MVVM/Hilt defaults that may contradict your repo.

---

## 6. Hybrid stacks

**Stays the same:** four-tier structure (always-on core, glob rules, auto exemplars, manual scan); EARS/bugfix specs; stop-and-ask; generator + drift CI; evidence-or-UNKNOWN discipline; golden-path exemplar.

| Stack | Add to `tech.md` | Scan signals | Globs | Guardrails |
|---|---|---|---|---|
| **KMP / Compose Multiplatform** | Kotlin/KMP version, targets, source-set hierarchy, CMP version, shared vs platform UI, Nav3 multiplatform | `kotlin { }` multiplatform, `commonMain/androidMain/iosMain`, `expect/actual`, `com.android.kotlin.multiplatform.library` | `**/commonMain/**`, `**/androidMain/**`, `**/iosMain/**` | No `android.*`/`java.*` in `commonMain`; AGP 9 KMP plugin replaces `com.android.library` in shared modules |
| **Flutter** | Flutter/Dart SDK, state mgmt, go_router, freezed/json_serializable, Pigeon | `pubspec.yaml`, `lib/`, `android/app/build.gradle(.kts)`, `MethodChannel` | `**/*.dart`, `android/**` | Never edit `*.g.dart`/`*.freezed.dart`; host app keeps targetSdk/permissions/R8; `flutter analyze/test`, goldens |
| **React Native** | RN version, New Architecture flag, Expo vs bare, navigation, state, TS strictness | `package.json`, `app.config.*`, `android/`, `newArchEnabled` | `**/*.{ts,tsx}`, `android/**` | Native modules follow native steering; don't edit autolinking/codegen output; Jest/RTL + Detox/Maestro |
| **Capacitor** | Capacitor version, web framework, plugins | `capacitor.config.*`, `android/app/src/main/assets/public` | `src/**`, `android/**` | Never edit copied web assets; `npx cap sync android` after web build |

Rule: keep native Android steering unchanged but scoped (`fileMatchPattern: ["android/**"]`) and add a sibling set for the cross-platform layer. The scan's Step 0 hybrid detection runs before Android heuristics.

---

## Recommendations

1. **Week 0 (½ day):** copy `docs/ai/`, `scripts/ai/`, and the CI workflow into the repo. Run `#repo-scan`. Answer `questions.md` in a 30-minute session. Regenerate.
2. **Gate P0 before the first spec.** Every P0 row must be a proven value, and the exemplar files must exist and be green.
3. **Design-First specs when an architecture doc exists**, Requirements-First otherwise. One layer-slice per task with explicit dependencies.
4. **Enforce, don't just ask:** install the PreToolUse protected-path hook and the PostTaskExec verification hook on day one; add detekt `ForbiddenImport` rules for the forbidden-API table.
5. **Pin the 2026 baseline but verify per repo:** Kotlin 2.4.x, AGP 9.x built-in Kotlin, KSP2 only, Compose BOM 2026.09.00 (Compose 1.12 needs compileSdk 37), Navigation 3 only if the scan shows it or the tech lead approves, targetSdk 36.
6. **Re-scan after every major upgrade** and review steering diffs like code.

## Caveats

- Tool behaviour changes fast (Kiro CLI inclusion support, Claude Code AGENTS.md reading, Android Studio skill dirs, Copilot path-specific scope). Re-check the portability table quarterly.
- Some quirks are community-documented (Cursor ignoring plain `.md`, Junie shadowing `guidelines.md`); test in your setup.
- Kiro hook tool-name matchers and stdin JSON fields in the sample are placeholders.
- Research figures come from general (Python/Java) code studies, not Android-specific benchmarks.
- Room 3.0 maturity not confirmed; keep Room 2.x guidance unless the scan shows `androidx.room3`.

## Sources

- https://kiro.dev/docs/steering/
- https://kiro.dev/docs/specs/
- https://kiro.dev/docs/specs/feature-specs/
- https://kiro.dev/docs/specs/bugfix-specs/
- https://kiro.dev/docs/specs/quick-spec/
- https://kiro.dev/docs/hooks/types/
- https://kiro.dev/docs/cli/v3/hooks/
- https://developer.android.com/studio/gemini/agent-files
- https://developer.android.com/studio/gemini/skills
- https://developer.android.com/studio/gemini/best-practices
- https://developer.android.com/studio/gemini/aiexclude
- https://developer.android.com/studio/releases/past-releases/as-narwhal-feature-drop-release-notes
- https://github.com/android/nowinandroid/blob/main/AGENTS.md
- https://github.com/android/skills
- https://android-developers.googleblog.com/2026/04/build-android-apps-3x-faster-using-any-agent.html
- https://developer.android.com/topic/architecture/views/recommendations-views
- https://developer.android.com/topic/architecture/ui-layer/events
- https://developer.android.com/build/releases/agp-9-0-0-release-notes
- https://developer.android.com/build/releases/gradle-plugin-roadmap
- https://blog.jetbrains.com/kotlin/2026/01/update-your-projects-for-agp9/
- https://developer.android.com/build/migrate-to-ksp
- https://github.com/google/ksp
- https://developer.android.com/jetpack/androidx/releases/room3
- https://developer.android.com/jetpack/androidx/releases/navigation3
- https://developer.android.com/blog/posts/whats-new-in-the-jetpack-compose-april-26-release
- https://support.google.com/googleplay/android-developer/answer/11926878
- https://kotlinlang.org/docs/releases.html
- https://code.claude.com/docs/en/memory
- https://docs.github.com/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
- https://docs.windsurf.com/windsurf/cascade/memories
- https://docs.devin.ai/cli/extensibility/rules
- https://thepromptshelf.dev/blog/jetbrains-junie-guidelines-md-agents-md-migration-2026/
- https://github.com/new-silvermoon/awesome-android-agent-skills
- https://github.com/krutikJain/android-agent-skills
- https://arxiv.org/pdf/2505.05057 (MARIN, API hallucination)
- https://github.com/dyoshikawa/rulesync/issues/3529
