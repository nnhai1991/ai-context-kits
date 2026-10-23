---
inclusion: fileMatch
fileMatchPattern: ["**/data-access/**", "**/api/**", "**/*.api.ts", "**/openapi/**", "**/generated/**"]
---
# API Contracts
- Source of truth: `{{OPENAPI_PATH | GRAPHQL_SCHEMA_PATH}}`; generator `{{TOOL}}`; regenerate with `{{API_REGEN_CMD}}`.
- Generated code at `{{GENERATED_PATH}}` is READ-ONLY. If a contract is missing, STOP and ask (do not hand-write DTOs).
- DTO -> domain mapping in `{{MAPPER_LOCATION}}`; components never see DTOs.
- Base URL from `{{API_BASE_URL_TOKEN}}`; never hard-code hosts or read `environment` directly in services {{if token pattern}}.
- Auth attached by `{{AUTH_INTERCEPTOR_PATH}}`. Never set Authorization headers manually; never use `fetch()`/axios directly.
- Errors: backend envelope `{{ERROR_SHAPE}}`; mapped by `{{ERROR_INTERCEPTOR_PATH}}`.
- Feature flags: `{{FLAG_SERVICE}}`; names `{{CONVENTION}}`.
- Money: {{minor units integer + currency}}; dates: {{ISO-8601 -> Date in mapper}}.
