# iOS AI-Context Template Kit

A fill-in package that lets Kiro (and Claude Code, Cursor, Copilot, Windsurf, Xcode agents)
generate code that fits an existing iOS repo.

## Contents
- `REPORT.md` — full research report: 58-item checklist, tool-portability table, failure modes, hybrid guidance.
- `docs/ai/` — CANONICAL template files (no tool front matter). Edit these only.
- `docs/ai/repo-scan-prompt.md` — the REPO SCAN prompt: give it to the agent to auto-fill the templates.
- `docs/ai/ai-files.yaml` — scope mapping used by the generator.
- `.kiro/steering/` — Kiro versions of the templates with inclusion front matter.
- `.kiro/specs/_template/` — requirements.md (EARS), design.md, tasks.md, bugfix.md templates.
- `.kiro/hooks/swiftlint-on-save.json` — optional hook (verify schema with your Kiro version).
- `scripts/ai-sync.sh` — generates AGENTS.md, CLAUDE.md, .cursor/rules, .github/instructions, .devin/rules from docs/ai.

## Quick start
1. Copy this folder's contents into your repo root.
2. In Kiro run `/repo-scan` (or paste `docs/ai/repo-scan-prompt.md` into any agent).
3. Review `docs/ai/scan-report.md` and resolve every `UNKNOWN – ask tech lead` item.
4. Approve the golden-path exemplar in `docs/ai/exemplars.md`.
5. Run `scripts/ai-sync.sh` to generate per-tool files; add `scripts/ai-sync.sh --check` and
   `python3 scripts/ai/build_code_index.py --platform ios --check && git diff --exit-code -- docs/ai/code-index` to CI.

Placeholders are marked `{{...}}`.

## Code index layer (shared with the other kits; see `docs/ai/code-index/README.md`)
- `docs/ai/code-index/` — generated views of a flat file-level graph: `INDEX.md`, `dirs/*.md` (one row per file), `flows/*.md` (what each entry point
  reaches), `components/*.md` (promoted hotspots only), `contracts.md` (endpoints, storage, routes, events, flags with every party), `hotspots.md`,
  `violations.md`; hand-written prose survives regeneration below each view's marker; one-line summaries live in `annotations.json`.
- `scripts/ai/build_code_index.py --platform ios` regenerates everything (`--check` for CI); `scripts/ai/query_code_index.py impact|dependents|flows|contract|find`
  is how agents consult the graph. No module definition is needed: directories and entry points are the facets.
- `.kiro/steering/code-index.md` (auto) — teaches the agent to run impact before design, read the source files it lists, and refresh the index after changes.
- The repo-scan prompt ends with a "Build the code index" step; `design.md` has an Impact section that the query fills.
