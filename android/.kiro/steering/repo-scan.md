---
inclusion: manual
---
# REPO SCAN — fill the Android AI-context templates from this repository

# ROLE
You are an Android codebase analyst. Your job is to DISCOVER facts, not to suggest improvements.
Do not modify any source file. Only write to docs/ai/ (and .kiro/steering/ if docs/ai does not exist).
Every fact you record MUST cite evidence as `path:line` or a command output. If you cannot prove a fact, write
`UNKNOWN – ask tech lead` and add it to the questions list. Never fill a placeholder with a "typical" value. Never print secret values.

# STEP 0 — Inventory (read-only)
List: root files; `settings.gradle(.kts)`; every `build.gradle(.kts)`; `gradle/libs.versions.toml`; `gradle.properties`;
`gradle/wrapper/gradle-wrapper.properties`; `build-logic/` or `buildSrc/`; `local.properties.example`/`secrets.defaults.properties`;
every `AndroidManifest.xml`; `proguard-rules.pro`, `consumer-rules.pro`; `lint.xml`, `lint-baseline.xml`; `detekt.yml`/`config/detekt/*`;
`.editorconfig`; ktlint/Spotless config; `res/xml/network_security_config.xml`; CI (`.github/workflows/*`, `bitrise.yml`, `.gitlab-ci.yml`,
`Jenkinsfile`, `.circleci/`); `fastlane/`; existing AI files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/`, `.github/copilot-instructions.md`,
`.junie/`, `.kiro/`, `.aiexclude`); `docs/`, ADRs, OpenAPI/GraphQL schemas.
Hybrid detection first: `pubspec.yaml` (Flutter), `package.json` + `android/` (React Native), `capacitor.config.*`, KMP `kotlin { }` blocks.
If allowed to run commands: `./gradlew -q projects`; `./gradlew -q :app:dependencies --configuration {{variant}}RuntimeClasspath | head -300`;
`./gradlew tasks --all | grep -Ei "test|lint|detekt|spotless|ktlint|roborazzi|paparazzi|screenshot|baselineprofile"`.
Hot files: `git log --since=6.months --name-only --pretty=format: | sort | uniq -c | sort -rn | head -50`.

# STEP 1 — Project facts -> tech.md
Kotlin version; AGP version; Gradle version; `android.builtInKotlin` / `android.newDsl` / `kotlin.android` plugin usage; JDK toolchain &
jvmTarget; compileSdk/minSdk/targetSdk per module (follow convention plugins!); Compose enabled? Compose BOM; Compose compiler plugin;
KSP vs kapt per processor; build types, flavor dimensions, flavors; modules and type (application/library/feature/test/benchmark/KMP);
convention plugin IDs and what each configures; Java vs Kotlin file counts (`find . -name "*.java" -not -path "*/build/*" | wc -l`).
Exact build/test/lint commands: copy what CI actually runs.

# STEP 2 — UI toolkit
Count: `@Composable` functions; `res/layout*/*.xml`; `Fragment` subclasses; `ComposeView`/`AndroidView` usages; ViewBinding/DataBinding flags.
Classify: COMPOSE_ONLY | VIEWS_ONLY | MIXED (report ratio and which modules are which). Material2 vs Material3 imports; design-system module.
From the last 6 months of history, which kind of screen is being added now.

# STEP 3 — Architecture pattern (score each; report top match + confidence)
| Pattern | Signals |
|---|---|
| MVVM | `*ViewModel : ViewModel` exposing `StateFlow`/`LiveData`; `*UiState` classes |
| MVI | sealed `*Intent|*Action|*Event`, `*Effect|*SideEffect`, `*Reducer`, `reduce(`; `org.orbitmvi.orbit`, `com.arkivanov.mvikotlin`, `ContainerHost` |
| Clean | `domain` module/package, `*UseCase`/`*Interactor` with `invoke`, repo interfaces in domain, impls in data |
| Circuit | `com.slack.circuit`, `Presenter<`, `Ui<`, `CircuitUiState`, `@CircuitInject` |
| Decompose | `com.arkivanov.decompose`, `ComponentContext`, `*Component`, `childStack` |
| Voyager | `cafe.adriel.voyager`, `Screen`, `ScreenModel` |
| MVP legacy | `*Presenter` + `*View` interfaces, `attachView` |
| Modular | `:feature:*`, `:core:*`, `api`/`impl` split; check feature->feature deps |
Give counts and 3 example paths each. If multiple, state which is CURRENT (newest files by git log) vs LEGACY.
Confidence: high (>=70% of feature modules), medium (40–70%), low. Report conflicts with ADRs/docs/existing AGENTS.md.

# STEP 4 — DI
Hilt (`@HiltAndroidApp`, `@AndroidEntryPoint`, `@HiltViewModel`, `@InstallIn`); plain Dagger (`@Component`, `DaggerAppComponent`);
Anvil (`@ContributesTo`, `@ContributesBinding`, `@MergeComponent`); Metro (`dev.zacsweers.metro`, `@DependencyGraph`);
Koin (`startKoin`, `module {`, `viewModelOf`, `koinViewModel()`); manual (`AppContainer`/`ServiceLocator`).
Record module locations, scopes, how dispatchers are provided (qualifiers?).

# STEP 5 — Navigation
Navigation 3 (`androidx.navigation3`, `NavDisplay`, `NavKey`, `entryProvider`, `rememberNavBackStack`); Navigation-Compose
(`NavHost`, `composable<Route>` type-safe vs `composable("route/{arg}")` string); Fragment nav (`res/navigation/*.xml`, `findNavController`,
Safe Args); Decompose/Voyager/Circuit navigators; custom Router. Record how a new destination is declared and registered (paths),
deep links, single- vs multi-activity (count `<activity` in manifests).

# STEP 6 — Async, state, lifecycle
Count imports `kotlinx.coroutines.flow` vs `io.reactivex`; `LiveData`; `collectAsStateWithLifecycle` vs `collectAsState`; `repeatOnLifecycle`;
`SavedStateHandle`; `rememberSaveable`; `GlobalScope`; hard-coded `Dispatchers.IO` vs injected; one-off events mechanism (`Channel`, `SharedFlow`, state flags).

# STEP 7 — Data & infra
Network: Retrofit/OkHttp vs Ktor; interceptors; auth. Serialization: kotlinx.serialization / Moshi (codegen or reflect) / Gson.
Contracts: OpenAPI/GraphQL (Apollo `apollo {}`)/proto, codegen output dirs. Persistence: Room (version, schema export dir, migrations),
SQLDelight, DataStore, SharedPreferences. Images: Coil/Glide. Background: WorkManager (custom `WorkerFactory`?). Analytics/crash/flags/
remote-config SDKs and wrappers. Secrets plugin and BuildConfig fields.

# STEP 8 — Quality gates -> testing.md
Test source sets per module; JUnit4 vs JUnit5; MockK/Mockito; Turbine; Truth/AssertK; Robolectric; Compose UI test; Espresso;
screenshot tool (Roborazzi/Paparazzi/`com.android.compose.screenshot`) and record/verify tasks; Gradle-managed devices;
baseline profile/macrobenchmark modules; lint/detekt/ktlint/Spotless tasks; what CI runs on PRs (exact commands). Derive local commands for the default variant.

# STEP 9 — Security & release
Manifest permissions (and runtime-request code paths); `exported` flags; network security config & cleartext; R8 `isMinifyEnabled`/`isShrinkResources`;
keep rules for serialization/reflection; signing config source; keystore files in repo (flag!); `.aiexclude`. Report PATHS of likely secrets, never values.

# STEP 10 — Pick the golden-path exemplar -> exemplars.md
Candidates = feature modules/packages containing ALL of: screen + state holder + (use case) + repository + remote + local + DI + navigation + >=1 unit test (+ UI/screenshot test).
Score: completeness (0–5) + recency (git log) + test coverage + follows the CURRENT pattern (not legacy) + small size (<~1,500 LOC).
Pick the top 1 (and a Views-based one if MIXED). List every file path per layer. List 1–3 anti-exemplars with reasons.

# STEP 11 — Output (write these files)
1. `docs/ai/scan-report.md`: tables for Steps 1–10 with evidence; pattern confidence; contradictions found (e.g. AGENTS.md says Nav2 but code uses Nav3).
2. Filled templates in `docs/ai/`: product, tech, structure, architecture, conventions, testing, api-contracts, exemplars,
   android-api-guardrails, security — replace each {{PLACEHOLDER}} with a proven value or `UNKNOWN – ask tech lead`. Always-loaded files <= ~120 lines.
3. `docs/ai/questions.md`: "UNKNOWN – ask tech lead" list, each with: question, why it matters (checklist ID), what you found, proposed default.
   Always include unless documented: new-dependency policy; JUnit4 vs 5 for NEW modules; one-off event pattern; whether LiveData/RxJava may
   appear in new code; screenshot baseline ownership; Room migration approval; feature-flag naming; data-safety inventory owner;
   target architecture for NEW code if legacy and current coexist.
4. Then STOP and print a summary. Do not start feature work.

# STEP — Build the code index (after the scan, before any feature work)
Follow `docs/ai/code-index/prompts/build-code-index.md` and `docs/ai/code-index/PLATFORM.md`. Generate with
`python3 scripts/ai/build_code_index.py --platform android --root . --out docs/ai/code-index` (every file gets a row, flows from each entry point,
contracts with all parties). Then: fix entry points and `rules/allowed-edges.json`, write one-line summaries in `annotations.json` (exemplar → hotspots →
shared files → the rest), write invariants on flow, directory and promoted component cards, and make `build_code_index.py --check` pass.
Design work must run `prompts/impact-analysis.md` (`query_code_index.py impact`) first.
