# Requirements: {{Feature}}
Source: {{JIRA-123}} · Architecture ref: {{ADR-007}} · Owner: {{name}}
## Introduction
{{User problem, scope, out of scope}}
## Requirement 1 — {{Show saved payment methods}}
**User story:** As a {{signed-in shopper}}, I want {{to see my saved cards}}, so that {{I can pay faster}}.
### Acceptance criteria (EARS)
1. WHEN the user opens the Payment screen THE app SHALL display saved cards sorted by last-used date descending.
2. WHILE the saved-cards request is in flight THE app SHALL show a loading placeholder and disable "Pay".
3. IF the request fails with a network error THEN THE app SHALL show the shared ErrorBanner with a Retry action.
4. WHERE the `payments_saved_cards` flag is disabled THE app SHALL hide the saved-cards section.
5. THE app SHALL expose each card row to VoiceOver as "{{brand}} ending in {{last4}}".
6. WHEN the user has no saved cards THE app SHALL show the empty state with an "Add card" action.
## Non-functional
- THE app SHALL support Dynamic Type up to {{AX5}} without truncating card numbers.

<!-- EARS patterns: Ubiquitous THE…SHALL · Event WHEN… · State WHILE… · Unwanted IF…THEN… · Optional WHERE…
     One testable behaviour per criterion. -->
