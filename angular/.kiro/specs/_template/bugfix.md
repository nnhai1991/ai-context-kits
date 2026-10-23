# Bugfix: {{Title}} (example: removed card reappears after navigating back)

## Current behavior
WHEN the user removes a saved card and navigates away and back to `/account/payment-methods` THE SYSTEM displays the removed card again until a hard refresh.

## Expected behavior
WHEN the user removes a saved card THE SYSTEM SHALL not display it on any subsequent visit in the same session.

## Unchanged behavior (regression guard)
- Listing, adding, and default-setting SHALL CONTINUE TO behave as in REQ-1..3. Interceptor/auth behaviour unchanged; no new global toasts.

## Root-cause hypothesis
{{root-provided store caches stale items; remove() updates a local copy; httpResource cache not reloaded}}

## Reproduction
1. {{STEPS}} — Evidence: {{logs/screenshots/test name}}

## Fix constraints
- Smallest change in `{{FILE}}`; write a failing test first referencing BUG-{{ID}}; no new dependencies.
