---
inclusion: always
---
# Product: {{APP_NAME}}

## Purpose
{{ONE_PARAGRAPH_WHAT_THE_APP_DOES_AND_FOR_WHOM}}

## Users & platforms
- Primary users: {{USER_SEGMENTS}}
- Form factors: {{PHONE | TABLET/FOLDABLE (adaptive) | WEAR | TV | AUTO}}
- Markets / locales: {{LOCALES}} (RTL required: {{YES/NO}})

## Core domains (ubiquitous language)
| Term | Meaning | Code name |
|---|---|---|
| {{TERM}} | {{MEANING}} | `{{KotlinType}}` |

## Non-functional requirements
- Accessibility target: {{WCAG 2.2 AA / internal standard}}
- Offline behaviour: {{OFFLINE_FIRST / ONLINE_ONLY / PARTIAL}}
- Performance budgets: cold start <= {{MS}} ms; jank <= {{%}}
- Privacy: data categories collected {{LIST}} (must match Play Data safety form)

## Where requirements & architecture docs live
- Functional requirements: {{PATH_OR_URL}}
- Architecture docs / ADRs: {{PATH_OR_URL}} (authoritative; flag conflicts with code)
- Design (Figma): {{URL}} — MCP available: {{YES/NO}}
- One Kiro spec per {{feature|epic}} at `.kiro/specs/{{kebab-name}}/`; Design-First when an architecture doc exists.

## Agent operating rules
- STOP and ask before: new dependency or version bump; new module; Room schema migration; changing public API of `:core:*`;
  new permission; new navigation library; touching {{billing, auth token refresh, crypto}}; anything marked UNKNOWN.
- If a needed fact is not in steering or code, ask — never guess versions, endpoints, or names.
- Reuse/extend existing types before creating parallel ones.
