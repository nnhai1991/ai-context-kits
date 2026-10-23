---
id: security
scope: glob
globs: ["**/AndroidManifest.xml", "**/proguard-rules.pro", "**/consumer-rules.pro", "**/network_security_config.xml", "**/data/**", "**/*Crypto*.kt"]
description: "Security and privacy rules"
---
# Security & privacy
- Secrets: read from `{{local.properties/CI}}` into `BuildConfig` via `{{secrets-gradle-plugin | custom}}`; never commit; never log.
- Network: `android:usesCleartextTraffic="false"`; config at `{{app/src/main/res/xml/network_security_config.xml}}`; pinning {{yes/no}}.
- Storage of tokens: {{Keystore-backed}}; no PII in plain SharedPreferences/DataStore.
- `android:exported` explicit on every component; PendingIntent uses `FLAG_IMMUTABLE` unless mutability required.
- R8 enabled for release (`isMinifyEnabled = true`); add keep rules for reflection/serialization; verify with `./gradlew assemble{{Release}}` + smoke test.
- Any new data collection must be added to the Play Data safety inventory at `{{path}}` -> stop-and-ask.
- Keep `.aiexclude` / `.kiroignore` covering keystores, `local.properties`, customer data fixtures.
