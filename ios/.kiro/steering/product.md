---
inclusion: always
---
# Product Overview
- App: {{APP_NAME}} — {{ONE_SENTENCE_PURPOSE}}
- Users: {{USER_SEGMENTS}} · Platforms: {{iPhone | iPad | Mac Catalyst | visionOS}} · Orientations: {{…}}
- Business-critical flows (never regress): {{login, checkout, …}}

## Domain glossary (use these exact terms in code)
| Term | Meaning | Code type |
|---|---|---|
| {{Booking}} | {{…}} | `{{Booking}}` |

## How requirements reach the agent
- Functional requirements: {{Jira/Confluence/docs/requirements}} · Architecture docs/ADRs: {{docs/adr}} (authoritative; flag conflicts)
- One Kiro spec per {{feature|epic}} at `.kiro/specs/{{kebab-name}}/`; use Design-first when an architecture doc exists.

## Agent operating rules
- STOP and ask before: adding a dependency; changing project/target structure; adding entitlements or Info.plist
  permissions; changing persistence schemas; touching {{DO_NOT_TOUCH_PATHS}}.
- If a needed fact is not in steering or code, ask — never guess versions, endpoints, or names.
- Reuse/extend existing types before creating parallel ones.
