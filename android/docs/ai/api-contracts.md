---
id: api-contracts
scope: glob
globs: ["**/data/**", "**/network/**", "**/remote/**", "**/api/**", "**/*.graphql", "**/openapi*.{yaml,yml,json}"]
description: "API, serialization, persistence and data-mapping contracts"
---
# API & data contracts

- Contract source of truth: `{{api/openapi.yaml | app/src/main/graphql/schema.graphqls}}`
- Codegen: {{OpenAPI generator / Apollo Kotlin}} outputs to `{{path}}` — regenerate with `{{./gradlew :core:network:generate...}}`; never hand-edit.
- HTTP client: single `{{OkHttpClient}}` provided in `{{path}}`; add interceptors there only. Auth: `{{AuthInterceptor/Authenticator}}` — do not reimplement.
- Serialization: {{kotlinx.serialization `Json { ignoreUnknownKeys = true; explicitNulls = false }`}} | {{Moshi codegen `@JsonClass(generateAdapter = true)`}}. Do not introduce a second serializer.
- DTOs: `@Serializable data class XDto` in `{{data/remote/model}}`; all fields nullable or defaulted unless contract guarantees presence.
- Mapping: `fun XDto.toDomain(): X` in `{{data/mapper}}`; domain models have no serialization annotations.
- Persistence: Room entities in `{{core:database}}`; schema export ON; every schema change requires a `Migration` + migration test -> stop-and-ask.
- Base URLs per flavor via `BuildConfig.{{API_BASE_URL}}`.
- R8: reflection-based or serialization models outside codegen need keep rules in `{{module}}/proguard-rules.pro` or `consumer-rules.pro`.
- Errors: map HTTP/IO errors to `{{DomainError}}` in repository; UI never sees `HttpException`.
- Feature flags: `{{FeatureFlags.isEnabled(Flag.X)}}`; new user-visible features ship behind `{{feature_snake_case}}`.
