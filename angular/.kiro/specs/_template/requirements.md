# Requirements: {{Feature}} (example: Saved Payment Methods)
Source FR: {{FR-PAY-012}} · Architecture: {{docs/adr/…}} · Owner: {{name}}

## Introduction
Signed-in customers can view, add, set default, and remove saved cards at `/account/payment-methods`. Card capture uses {{PSP}} hosted fields; we store only the PSP token.

## Requirement 1 — List saved methods
**User story:** As a signed-in customer, I want to see my saved cards so that I can manage them.
1. WHEN the user navigates to `/account/payment-methods` THE SYSTEM SHALL request `GET {{API}}/payment-methods` and display brand, last 4, expiry (MM/YY) and default badge.
2. WHILE the request is in flight THE SYSTEM SHALL show a loading indicator announced to assistive technology (`role="status"`).
3. WHEN the response contains zero methods THE SYSTEM SHALL show an empty state with an "Add card" action.
4. IF the request fails THEN THE SYSTEM SHALL show an inline error with "Retry" and SHALL NOT show a global toast (interceptor policy {{X}}).
5. IF the user is not authenticated THEN THE SYSTEM SHALL redirect to `{{LOGIN_ROUTE}}` via the existing auth guard.

## Requirement 2 — Add a card
1. WHEN the user selects "Add card" THE SYSTEM SHALL display a form with cardholder name and the {{PSP}} hosted card fields.
2. WHEN the cardholder name is empty or longer than 100 characters THE SYSTEM SHALL show a field-level validation message and disable submit.
3. WHEN the user submits a valid form THE SYSTEM SHALL tokenize via {{PSP}} and send `POST {{API}}/payment-methods` with `{ token, holderName, makeDefault }`.
4. WHILE submission is pending THE SYSTEM SHALL disable submit and prevent duplicate submissions.
5. WHEN creation succeeds THE SYSTEM SHALL add the method to the list without reload and move focus to the new item.
6. IF tokenization or creation fails THEN THE SYSTEM SHALL keep the entered name, show the error, and not create a partial record.

## Requirement 3 — Set default
1. WHEN the user selects "Make default" on a non-default method THE SYSTEM SHALL call `PUT {{API}}/payment-methods/{id}/default` and update badges optimistically.
2. IF the call fails THEN THE SYSTEM SHALL revert the badge and show an inline error.

## Requirement 4 — Remove
1. WHEN the user selects "Remove" THE SYSTEM SHALL open an accessible confirmation dialog with focus trapped.
2. WHEN the user confirms THE SYSTEM SHALL call `DELETE {{API}}/payment-methods/{id}` and remove the item on success.
3. IF the method is the default and other methods exist THEN THE SYSTEM SHALL require choosing a new default first.
4. WHERE the feature flag `payments_delete_enabled` is off THE SYSTEM SHALL hide the Remove action.

## Non-functional
- NFR-1: PAN/CVV never pass through application code, logs, or state.
- NFR-2: WCAG 2.2 AA; AXE clean.  - NFR-3: SSR-safe {{if SSR}}.  - NFR-4: Feature lazy-loaded; initial chunk budget unchanged.

<!-- EARS: Ubiquitous THE SYSTEM SHALL · Event WHEN · State WHILE · Unwanted IF…THEN · Optional WHERE. One testable behaviour per criterion. -->
