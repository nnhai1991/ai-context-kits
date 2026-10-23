# Android AI-Context Template Kit

A fill-in package that lets Kiro (and Claude Code, Cursor, Copilot, Windsurf, Android Studio Gemini/Agent mode,
JetBrains Junie) generate code that fits an existing Android repo. Mirrors the iOS kit.

## Contents
- `REPORT.md` — full research report: prioritized checklist, tool-portability table, failure modes, hybrid guidance.
- `docs/ai/` — CANONICAL template files (tool-neutral front matter). Edit these only.
- `docs/ai/repo-scan-prompt.md` — the REPO SCAN prompt: give it to the agent to auto-fill the templates.
- `.kiro/steering/` — Kiro versions of the templates with inclusion front matter.
- `.kiro/specs/_template/` — requirements.md (EARS), design.md, tasks.md, bugfix.md templates (saved-payment-methods example).
- `.kiro/hooks/android-gates.json` + `scripts/ai/block-protected-paths.sh` — protected-path block, format-on-save, verify-after-task.
- `scripts/ai/generate.py` — generates AGENTS.md, CLAUDE.md, .claude/rules, .cursor/rules, .github/instructions, .devin/rules, .junie/rules from docs/ai.
- `.github/workflows/ai-context.yml` — CI drift check.

## Quick start
1. Copy this folder's contents into your repo root.
2. In Kiro run `#repo-scan` (or paste `docs/ai/repo-scan-prompt.md` into any agent).
3. Review `docs/ai/scan-report.md` and answer every item in `docs/ai/questions.md`.
4. Approve the golden-path exemplar in `docs/ai/exemplars.md`.
5. Run `python3 scripts/ai/generate.py`; keep the CI drift workflow.

Placeholders are marked `{{...}}`. Kiro front matter must be on line 1 of each steering file.

## Code index layer (shared with the other kits; see `docs/ai/code-index/README.md`)
- `docs/ai/code-index/` — generated views of a flat file-level graph: `INDEX.md`, `dirs/*.md` (one row per file), `flows/*.md` (what each entry point
  reaches), `components/*.md` (promoted hotspots only), `contracts.md` (endpoints, storage, routes, events, flags with every party), `hotspots.md`,
  `violations.md`; hand-written prose survives regeneration below each view's marker; one-line summaries live in `annotations.json`.
- `scripts/ai/build_code_index.py --platform android` regenerates everything (`--check` for CI); `scripts/ai/query_code_index.py impact|dependents|flows|contract|find`
  is how agents consult the graph. No module definition is needed: directories and entry points are the facets.
- `.kiro/steering/code-index.md` (auto) — teaches the agent to run impact before design, read the source files it lists, and refresh the index after changes.
- The repo-scan prompt ends with a "Build the code index" step; `design.md` has an Impact section that the query fills.
