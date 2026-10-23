---
inclusion: auto
name: security
description: "Security, auth, tokens, sanitization, XSS, CSP, secrets, PII/PCI and dependency rules for Angular code"
---
# Security Rules
- Rely on Angular's built-in sanitization; `DomSanitizer.bypassSecurityTrust*` requires tech-lead approval + justification comment.
- Never bind untrusted HTML via `[innerHTML]` without sanitization; never build URLs from user input without validation.
- Tokens: {{HttpOnly cookies + CSRF via withXsrfConfiguration | in-memory only}}. Never `localStorage`/`sessionStorage` for tokens.
- Secrets: nothing secret in `environment*.ts`, `angular.json` `define`, or assets — bundles are public.
- CSP: {{policy / autoCsp}}; no inline handlers or `eval`; Trusted Types {{enabled?}}.
- PCI/PII: {{card capture only via PSP hosted fields; store token + last4 + brand + expiry}}. Never log PII.
- SSR: no request-specific data in singletons; no secrets in TransferState.
- Dependencies: none new without approval; run `{{AUDIT_CMD}}`. Accessibility is a release blocker (AXE clean, WCAG AA).
