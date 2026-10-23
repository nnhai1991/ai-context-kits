# Angular AI-Context Template Kit

A fill-in package that lets Kiro (and Claude Code, Cursor, Copilot, Windsurf/Devin, Junie) generate code that fits an
existing Angular repo. Mirrors the iOS and Android kits.

## Contents
- `REPORT.md` — research report: prioritized checklist, version-gate table, tool portability, failure modes, branch-out.
- `docs/ai/` — CANONICAL templates (tool-neutral front matter). Edit these only.
- `docs/ai/repo-scan-prompt.md` — the REPO SCAN prompt (read-only, evidence-cited, UNKNOWN list).
- `.kiro/steering/` — Kiro versions with inclusion front matter. `.kiro/specs/_template/` — EARS requirements, design, tasks, bugfix.
- `.kiro/hooks/*.kiro.hook` — lint-on-edit, spec-sync, verify-after-task.
- `.kiro/settings/mcp.json` — Angular CLI MCP server (`ng mcp`) so the agent can verify APIs against docs.
- `scripts/ai/generate.py` — emits AGENTS.md, CLAUDE.md, .claude/rules, .cursor/rules, .github/instructions, .devin/rules, .junie/rules.
- `.github/workflows/ai-context.yml` — CI drift check.

## Quick start
1. Copy into repo root. 2. Run `#repo-scan` in Kiro (Angular MCP enabled, `--read-only`). 3. Answer `docs/ai/questions.md`.
4. Approve the exemplar. 5. `python3 scripts/ai/generate.py`; keep the CI check.
Precedence rule the kit encodes: task/spec > repo steering + exemplars > angular.dev / MCP best practices > model memory.

## Code index layer (shared with the other kits; see `docs/ai/code-index/README.md`)
- `docs/ai/code-index/` — generated views of a flat file-level graph: `INDEX.md`, `dirs/*.md` (one row per file), `flows/*.md` (what each entry point
  reaches), `components/*.md` (promoted hotspots only), `contracts.md` (endpoints, storage, routes, events, flags with every party), `hotspots.md`,
  `violations.md`; hand-written prose survives regeneration below each view's marker; one-line summaries live in `annotations.json`.
- `scripts/ai/build_code_index.py --platform angular` regenerates everything (`--check` for CI); `scripts/ai/query_code_index.py impact|dependents|flows|contract|find`
  is how agents consult the graph. No module definition is needed: directories and entry points are the facets.
- `.kiro/steering/code-index.md` (auto) — teaches the agent to run impact before design, read the source files it lists, and refresh the index after changes.
- The repo-scan prompt ends with a "Build the code index" step; `design.md` has an Impact section that the query fills.
