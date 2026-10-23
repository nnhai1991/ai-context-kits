---
inclusion: always
---
# Product Context

## What this application is
{{ONE_PARAGRAPH_PRODUCT_DESCRIPTION}}

## Users & key journeys
| Persona | Top journeys | Critical constraints |
|---|---|---|
| {{PERSONA_1}} | {{JOURNEYS}} | {{e.g. WCAG AA, mobile-first, slow networks}} |

## Business rules the code must never violate
- {{RULE_1 e.g. "Card data (PAN/CVV) never touches our code; only PSP-hosted fields."}}

## Domain glossary (use these names in code)
| Term | Meaning | Code name |
|---|---|---|
| {{TERM}} | {{MEANING}} | {{PaymentMethod}} |

## Where requirements live
- Functional requirements: {{PATH_OR_TOOL}} · Architecture docs / ADRs: {{docs/adr/}} (authoritative; flag conflicts with code)
- One Kiro spec per {{feature|epic}} at `.kiro/specs/{{kebab-name}}/`; Design-First when an architecture doc exists.

## Agent operating rules
- STOP and ask before: new/upgraded dependency; editing generated code; changing Nx tags/depConstraints; public API change of shared libs;
  security-sensitive code (auth, sanitization bypass, tokens); ambiguous requirement; anything marked UNKNOWN.
- Never "modernize" code you weren't asked to touch. Never guess versions, endpoints, or names — ask.
- Reuse existing services/components before creating parallel ones.
