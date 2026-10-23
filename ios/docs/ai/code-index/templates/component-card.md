<!-- Template for the hand-written tail of components/<id>.md. Only promoted (tier: card) nodes get this file. The generated header holds kind, layer, path, metrics, uses, used-by, flows, tests and the stale flag. Do not copy signatures or dependency lists here: read the source. -->

## Responsibility (what it does, one paragraph)
{{…}}

## Invariants & side effects (what the code does not say)
- {{writes table X; must not be called off the main actor; idempotent; cached 5 min}}

## Gotchas / history
- {{2026-07: optimistic rollback bug — see BUG-123}}
