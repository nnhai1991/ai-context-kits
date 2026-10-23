---
id: tech
scope: always
---
# Tech stack (source of truth: gradle/libs.versions.toml)

## Toolchain (verify against files; do NOT assume newer/older)
| Item | Value |
|---|---|
| Kotlin | {{KOTLIN_VERSION}} (K2) |
| AGP | {{AGP_VERSION}} — built-in Kotlin: {{ON/OFF}} (`android.builtInKotlin`); new DSL: {{ON/OFF}} |
| Gradle wrapper | {{GRADLE_VERSION}} |
| JDK toolchain | {{JDK}}; jvmTarget {{JVM_TARGET}} |
| compileSdk / minSdk / targetSdk | {{COMPILE}} / {{MIN}} / {{TARGET}} |
| UI | {{COMPOSE_ONLY / VIEWS_ONLY / MIXED}}; Compose BOM {{BOM}}; Material3 {{VER}} |
| Annotation processing | {{KSP2 / kapt / both}} — processors: {{room:ksp, hilt:ksp, moshi:ksp, ...}} |
| Async | {{Coroutines+Flow / RxJava3 / both (bridge: kotlinx-coroutines-rx3)}} |
| DI | {{Hilt / Koin / Dagger / Anvil / Metro / manual}} |
| Navigation | {{Navigation3 / Navigation-Compose type-safe / Fragment nav XML / Decompose / Voyager / Circuit}} |
| Network | {{Retrofit+OkHttp / Ktor}}; serialization {{kotlinx.serialization / Moshi / Gson}} |
| Persistence | {{Room x.y / SQLDelight}}; {{DataStore Preferences/Proto}} |
| Images | {{Coil 3 / Glide}} |
| Background | {{WorkManager}} |
| Analytics / crash | {{Firebase / Sentry / internal}} via `{{AnalyticsWrapperPath}}` |

## Dependency rules
- Add or reference dependencies ONLY through `libs.*` catalog aliases. Never write raw coordinates or versions in module build files.
- Do NOT add a new library, plugin or version bump without asking (stop-and-ask).
- Apply convention plugins (`{{alias(libs.plugins.myapp.android.feature)}}`) instead of raw AGP/Kotlin plugins in feature modules.
- {{IF AGP>=9 && builtInKotlin}}: never apply `org.jetbrains.kotlin.android`; Kotlin is built into AGP.
- {{IF KMP}}: Android target in shared modules uses `com.android.kotlin.multiplatform.library`.

## Commands (run from repo root; default variant {{VARIANT}})
| Purpose | Command |
|---|---|
| Format (auto-fix) | `{{./gradlew spotlessApply | ./gradlew ktlintFormat}}` |
| Static analysis | `{{./gradlew detekt}}`; `./gradlew lint{{Variant}}` |
| Unit tests (all) | `./gradlew test{{Variant}}UnitTest` |
| Single test | `./gradlew :{{module}}:test{{Variant}}UnitTest --tests "{{fqcn}}"` |
| Screenshot verify | `{{./gradlew verifyRoborazzi{{Variant}} | verifyPaparazzi{{Variant}} | validate{{Variant}}ScreenshotTest}}` |
| Instrumented | `{{./gradlew pixel6api{{N}}{{Variant}}AndroidTest}}` (Gradle-managed device) |
| Build | `./gradlew assemble{{Variant}}` |
| Dependency guard / API check | `{{./gradlew dependencyGuard | apiCheck}}` |

## Environments
- Flavors: {{FLAVOR_DIMENSIONS_AND_VALUES}}; build types: {{debug, release, benchmark}}
- Config fields via `buildConfigField` in `{{path}}`; secrets come from `{{local.properties / gradle.properties / CI env}}` — never committed.
