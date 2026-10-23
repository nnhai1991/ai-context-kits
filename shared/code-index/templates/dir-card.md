<!-- Template for the hand-written tail of dirs/<slug>.md. The generated part above the marker holds the row table (one row per file: symbol, kind, summary, fan-in, flows, tests, risk), uses/used-by directories, and metrics. Write only what the code does not say. -->

## Purpose (one paragraph; first line is shown in INDEX.md)
{{What this directory is for and what belongs here. Say whether its boundary is compiler-enforced (module/target/project) or by convention.}}

## Public surface (by convention unless enforced)
- {{Types or entry points other directories may use. Everything else is internal.}}

## Invariants & side effects
- {{Rules that hold across files here, e.g. ordering, uniqueness, threading, "never log PAN"}}

## Gotchas / history
- {{date: what happened, link to spec or bug}}
