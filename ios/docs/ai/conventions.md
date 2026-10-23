# Coding Conventions
- Lint/format enforced by `{{.swiftlint.yml}}` / `{{.swiftformat}}` — run them; don't restate them.
- Naming: {{`XRepository` + `DefaultXRepository`}}; file = primary type; one primary type per file.
- Access: `internal` default; `public` only for module API; classes `final` by default.
- Errors: {{`enum XError: Error`}} mapped to {{ErrorBanner/AlertState}}; no `try!`/force-unwrap outside tests.
- Logging: `Logger(subsystem: "{{com.company.app}}", category: "{{Feature}}")`; user data `privacy: .private`; no `print`.
- Strings: {{Localizable.xcstrings via String(localized:)}}; no hard-coded user-facing text.
- Design system: `{{DesignSystem}}` tokens and components only.
- Accessibility: label every control; support Dynamic Type; `accessibilityIdentifier` = "{{feature.element}}".
## Security & privacy
- No secrets in source ({{Config.xcconfig}} + CI secrets); never print tokens.
- Tokens/credentials only in `{{KeychainStore}}`. No new ATS exceptions.
- Permissions/entitlements: ask first; usage strings come from {{product/legal}}. Required-reason API → update PrivacyInfo.xcprivacy.
