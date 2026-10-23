# Bugfix — {{Title}} (example: crash when deleting the last saved card after rotation)
Source: {{Crashlytics issue id / JIRA}}

## Current Behavior (Defect)
- WHEN the user rotates the device while the delete confirmation dialog is open and then confirms THEN the system crashes with `{{IllegalStateException: pendingDelete is null}}`.

## Expected Behavior (Correct)
- WHEN the user confirms deletion after a configuration change or process death THE SYSTEM SHALL delete the card named in the dialog and show the empty state if none remain.

## Unchanged Behavior (Regression Prevention)
- WHEN no configuration change occurs THE SYSTEM SHALL CONTINUE TO delete the selected card and update the list.
- WHEN the deleted card was default and others exist THE SYSTEM SHALL CONTINUE TO require choosing a new default first.

## Constraints
- Fix in ViewModel/state restoration only; no UI redesign; no new dependencies.

## Tasks
- [ ] 1. Failing test reproducing Current behaviour (SavedStateHandle restore)
- [ ] 2. Fix; test passes; Unchanged tests still pass
- [ ] 3. Verify via tech.md commands
