# Code Index layer (shared by iOS, Android, Angular kits)

Steering tells the AI *how the repo is built*. Specs tell it *what to build*. The **code index** tells it
**where everything is, who depends on it, what breaks if you touch it, and what nobody wrote down in the code.**
It stores what is expensive to rediscover and links to what is cheap to read. It never duplicates signatures or bodies.

## Design
- **Source of truth is a flat, file-level graph** (`graph.json`): one node per source file (plus *contract* nodes for endpoints, storage,
  routes, events and flags, and *external* nodes for libraries), typed edges with evidence and confidence, generated flows, violations.
- **Every readable file is a generated view** of the graph. Hand-written prose lives only below the `<!-- generated:end -->` marker of a view
  and survives regeneration. Per-file curated fields (the one-line summary, tier, domain, owner, entry) live in `annotations.json`.
- **Groupings are facets, not a hierarchy.** Directory, layer, flow, domain, owner and (when the platform has one) module are fields on the node.
  No module definition is required: directories and entry points exist on every platform.
- **Full coverage by construction:** every non-test file has a row in exactly one directory card, a one-line summary (auto-bootstrapped,
  agent-refined), inbound dependents, flow membership and tests. `--check` enforces it.
- **Prose only where the code is silent:** invariants and gotchas on flows, directories and promoted components. Promotion (risk high,
  cross-cutting, security-tagged) is one-way.

## Files in `docs/ai/code-index/`
| File | What it holds | Who writes it |
|---|---|---|
| `graph.json` | nodes, edges, flows, violations, stats (schema: `code-index.schema.json`) | script only |
| `symbols.json` | symbol → file | script only |
| `annotations.json` | per-node summary, tier, domain, owner, entry; the script never lowers a tier | agent |
| `INDEX.md` | directories, flows, cross-cutting, contracts summary, hotspots, unreachable files, orphans + hand-written gotchas and unknowns | script + agent tail |
| `dirs/<slug>.md` | one row per file (symbol, kind, path, summary, fan-in, flows, tests, risk), uses/used-by dirs + hand-written purpose, surface, invariants | script + agent tail |
| `flows/<id>.md` | entry, key path (file at each hop), files, shared files, contracts, tests + hand-written invariants | script + agent tail |
| `components/<id>.md` | promoted nodes only: metrics, uses, used-by, flows, tests + hand-written responsibility, invariants, gotchas | script + agent tail |
| `contracts.md` | every endpoint, table/key, route, event and flag with providers and consumers | script only |
| `dependencies.md` | every external import grouped by declared package (lock file), version, allowlist status from `tech.md`, importers, flows; declared-but-unused packages | script only |
| `hotspots.md`, `violations.md` | top-20 risk; edges that break `rules/allowed-edges.json` | script only |
| `rules/allowed-edges.json` | allowed layer→layer and dir→dir dependencies | tech lead |
| `impact.md`, `PLATFORM.md`, `prompts/`, `templates/` | recipe, platform notes, agent prompts, prose skeletons | kit |

## Scripts (`scripts/ai/`)
- `build_code_index.py --platform ios|android|angular [--check]` — regenerates everything; `--check` fails on missing summaries, stale promoted nodes,
  unwritten card prose, rule violations, or a third-party import that is not on the `tech.md` allowlist (once that table is filled). Regex-based; `PLATFORM.md` names the tool that should replace each extractor.
- `query_code_index.py impact|dependents|flows|tests|contract|find|node|violations|stale` — the only way agents should consult the graph.

## Dependency model
An edge `from → to` means "if `to` changes contract or behaviour, `from` may break". Impact walks it in reverse.
Structural (`imports`, `extends`, `implements`, `injects`), behavioural (`calls`, `observes`, `navigates_to`), data
(`consumes_endpoint`, `exposes_endpoint`, `reads`, `writes`, `emits`, `defines_route`), verification (`tested_by`).
Only high/medium edges drive fan-in and risk; low-confidence symbol matches appear in impact output as *possible*.
Contract nodes make the invisible couplings (DI by name, routing by string, streams, HTTP, tables) explicit: providers and consumers meet on the node.
External nodes (`ext:`) are matched to the lock file (Podfile.lock / Package.resolved, libs.versions.toml, package.json + package-lock.json) and to the
allowlist table in `docs/ai/tech.md`, so the "never add a dependency" rule is checked, not just stated.

## Lifecycle
1. Scan ends with `prompts/build-code-index.md`: generate, fix entry points and rules, write summaries in priority order, write prose where the code is silent.
2. Tech lead reviews `INDEX.md`, the component cards and the invariants of the top flows.
3. Every spec task ends with `prompts/update-code-index.md` (hook) and `--check` (CI). Views are committed; CI fails if regeneration produces a diff.
