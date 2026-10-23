# API Contracts & Data Mapping
- Spec: `{{openapi/api.yaml}}`; codegen: {{swift-openapi-generator | none}} — never hand-write generated types.
- Client: `{{APIClient}}` in `{{Packages/Networking}}`; endpoints as {{`Endpoint<Response>` | generated operations}}.
- Auth: {{bearer token from KeychainStore; AuthInterceptor refreshes}} — do not reimplement.
- DTOs stay in Data; `{{XMapper}}` maps to domain; views never see DTOs.
- Decoding: {{convertFromSnakeCase; ISO8601}}; unknown enum cases → {{.unknown}}.
- Errors: transport → `{{NetworkError}}` → domain error in repository.
- Environments: {{Debug→staging, Release→prod}} via `{{API_BASE_URL}}` xcconfig key.
- Flags: `{{FeatureFlags.isEnabled(.x)}}`; new user-visible features ship behind `{{feature_snake_case}}`.
