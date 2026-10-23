# Requirements Document — {{Feature}} (example: Saved Payment Methods, Compose)
Source FR: {{FR-PAY-012}} · Architecture: {{docs/adr/0007-payments.md}} · Owner: {{name}}

## Introduction
{{Signed-in users can view, set default, and delete saved payment cards from Settings -> Payment methods. Out of scope: adding cards.}}

## Requirement 1 — List saved methods
**User Story:** As a signed-in user, I want to see my saved cards, so that I can manage how I pay.
### Acceptance Criteria (EARS)
1. WHEN the Payment methods screen is opened THE SYSTEM SHALL display cached methods from the local database within 300 ms and then refresh from `GET /v1/payment-methods`.
2. WHILE the refresh is in progress THE SYSTEM SHALL show a non-blocking progress indicator and keep cached items interactive.
3. IF the refresh fails AND cached data exists THEN THE SYSTEM SHALL keep showing cached data and display a retry snackbar.
4. IF the refresh fails AND no cached data exists THEN THE SYSTEM SHALL show the full-screen error state with a Retry action.
5. WHEN the list is empty THE SYSTEM SHALL show the empty state with an "Add card" call to action.
6. THE SYSTEM SHALL display each card as brand icon, "•••• last4", expiry MM/YY, and a "Default" badge — never the full PAN.

## Requirement 2 — Set default
1. WHEN the user selects "Set as default" on a non-default card THE SYSTEM SHALL optimistically mark it default and call `POST /v1/payment-methods/{id}/default`.
2. IF that call fails THEN THE SYSTEM SHALL revert the optimistic change and show an error snackbar.

## Requirement 3 — Delete
1. WHEN the user taps Delete THE SYSTEM SHALL show a confirmation dialog naming the card (brand + last4).
2. WHEN deletion is confirmed THE SYSTEM SHALL remove the card from the list and call `DELETE /v1/payment-methods/{id}`.
3. IF the card is the default AND other cards exist THEN THE SYSTEM SHALL require the user to choose a new default before deletion.
4. WHERE the feature flag `payments_delete_enabled` is off THE SYSTEM SHALL hide the Delete action.

## Requirement 4 — Platform quality
1. THE SYSTEM SHALL preserve the open confirmation dialog and pending selection across configuration change and process death.
2. THE SYSTEM SHALL expose content descriptions such as "Visa ending 4242, expires 08/28, default" for TalkBack and 48dp minimum touch targets.
3. THE SYSTEM SHALL render correctly edge-to-edge at targetSdk {{36}}, in dark theme and at font scale 2.0.

<!-- EARS patterns: Ubiquitous THE…SHALL · Event WHEN… · State WHILE… · Unwanted IF…THEN… · Optional WHERE…
     One testable behaviour per criterion; IDs (1.1, 1.2 …) are referenced by tasks and tests. -->
