# BUILD CODE INDEX — instructions for the agent (read-only on source; writes only docs/ai/code-index/)

Goal: a code index where **every source file is mapped** (a row with a one-line meaning, inbound dependencies, flows and tests),
**contracts** (endpoints, storage, routes, events, flags) list every party, and hand-written prose exists only where the code is silent.
The index stores what is expensive to rediscover (who depends on what, what breaks, history) and links to what is cheap to read (the source).
Never copy signatures, parameter lists or outbound dependency lists into the index.

## Step 0 — Generate
    python3 scripts/ai/build_code_index.py --platform {{ios|android|angular}} --root . --out docs/ai/code-index
Read `docs/ai/code-index/PLATFORM.md` first: it says what counts as an entry point here, which platform tool should replace the regex
extractor, and the resolver order for directory buckets. Read `docs/ai/scan-report.md` and `exemplars.md` if they exist.
Open `INDEX.md` and note: stats line, unreachable files, orphan annotations, extractor confidence.

## Step 1 — Entry points and rules (fix the skeleton before writing prose)
- Every screen the user can reach, every background job and every exposed endpoint must be an entry (a flow). If one is missing, add
  `"entry": true` to its node in `annotations.json`. If a flow is bogus (a subview promoted by name), it is harmless; leave it.
- Copy `templates/../rules/allowed-edges.json` to `rules/allowed-edges.json` if absent and tighten it to the layering the scan found.
  Regenerate. Every remaining violation is either a real smell (record it in INDEX.md gotchas) or a rule that is wrong (fix the rule).
- `dependencies.md`: every third-party package must be on the `tech.md` allowlist (fill that table first; `--check` fails on `not on allowlist`).
  `Declared but never imported` are removal candidates for the tech lead; `not in lock file` rows mean the lock file was not found or the module name
  could not be mapped to a package (fix by naming the module in the allowlist row's Import column).
- Unreachable files: decide dead code vs missing entry. Record dead-code candidates under INDEX.md › Unknowns for the tech lead.

## Step 2 — Summaries (one line per file; this is the bulk of the work, do it in priority order)
For each row whose summary starts with `AUTO:` write `"summary"` in `annotations.json` (the script stores the file hash; a later file
change marks the summary stale). One line, **what it does for the app**, not what it is. Cite nothing; the row already links the file.
Priority: exemplar feature → files in the top-10 hotspots → files in ≥3 flows → entry points → the rest. Stop when the budget runs out:
`AUTO:` rows are acceptable coverage, they are just weaker. Never invent; if you cannot tell from the file, write `UNKNOWN: <what to check>`.

## Step 3 — Prose where the code is silent
- **Flow cards** (`flows/*.md`, below the marker): what the flow does for the user; invariants that span its files; history. One flow at a time,
  reading the key path files. At least one invariant per flow or the literal line `No cross-file invariant found`.
- **Directory cards** (`dirs/*.md`): Purpose (first line shows in INDEX.md), whether the boundary is enforced or by convention, public surface
  by convention, invariants, gotchas.
- **Component cards** (`components/*.md`): only for promoted nodes (risk high, cross-cutting, security). Responsibility, invariants and side
  effects, gotchas. These are the cards the tech lead reviews, so cite evidence (`path:line`) for every invariant.
- `INDEX.md` tail: repo-wide gotchas and Unknowns.

## Step 4 — Verify and hand over
    python3 scripts/ai/build_code_index.py --platform {{p}} --check
Fix what it reports (missing summaries, stale promoted nodes, placeholder prose, violations). Print a 10-line summary: files, flows,
cards written, AUTO rows left, violations, unreachable, and the top 3 unknowns for the tech lead. Do not change source.
