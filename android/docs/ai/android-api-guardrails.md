---
id: android-api-guardrails
scope: glob
globs: ["**/*.kt", "**/AndroidManifest.xml", "**/build.gradle.kts", "**/res/xml/*.xml"]
description: "Android API version safety and forbidden/deprecated API table"
---
# Android API guardrails (minSdk {{MIN}}, targetSdk {{TARGET}}, compileSdk {{COMPILE}}, Compose BOM {{BOM}})

## Version safety
- Any API above minSdk {{MIN}} must be guarded with `if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.X)` or use the AndroidX
  compat equivalent (`ContextCompat`, `NotificationManagerCompat`, `WindowCompat`…). Annotate helpers with `@RequiresApi`.
- Use only Compose/Material3 APIs that exist in BOM {{BOM}}. If unsure an API exists, search the dependency sources in the repo
  or ask — never invent signatures. Experimental APIs require `@OptIn` and {{are allowed / forbidden}}.

## Forbidden -> use instead
| Do not use | Use |
|---|---|
| `AsyncTask`, `Handler().postDelayed` for work, `Thread {}` | coroutines in proper scope / WorkManager |
| `startActivityForResult` / `onActivityResult` / `requestPermissions`+`onRequestPermissionsResult` | Activity Result API (`registerForActivityResult`, `rememberLauncherForActivityResult`) |
| `LiveData` in new code {{unless house pattern}} | `StateFlow` + `collectAsStateWithLifecycle` |
| `collectAsState()` for VM state on Android | `collectAsStateWithLifecycle()` |
| `GlobalScope`, `runBlocking` in app code | `viewModelScope` / injected `CoroutineScope` |
| Hard-coded `Dispatchers.IO` in classes | injected dispatcher |
| `Context`/`Activity`/`View` held in ViewModel | pass via use case / `@ApplicationContext` in data layer |
| `onBackPressed()` override | `OnBackPressedDispatcher` / `BackHandler` (predictive back) |
| `EncryptedSharedPreferences` (deprecated) | {{house choice: Tink-encrypted DataStore / Keystore}} |
| `kotlin-android-extensions` synthetics, `findViewById` in new code | ViewBinding / Compose |
| raw dependency coordinates | `libs.*` aliases |
| `kapt` for processors with KSP support | `ksp` |

## targetSdk {{36}} behaviours to respect
- Edge-to-edge is enforced: handle `WindowInsets` (`Modifier.safeDrawingPadding()` / `Scaffold` insets).
- Predictive back: no blocking `onBackPressed`.
- Foreground services must declare a `foregroundServiceType`; exact alarms need permission justification.
- {{add house-specific behaviour changes}}

## Permissions
Declare in manifest + request at runtime with rationale UI; handle "denied" and "don't ask again"; never request at app start without user intent.

## Generated / protected files — never edit by hand
`build/**`, `**/generated/**`, `{{schemas/**}}`, `gradle/wrapper/**`, `local.properties`, `*.jks`, `*.keystore`, `google-services.json` {{list}}.
