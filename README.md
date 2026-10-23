# AI-Context Kits (iOS · Android · Angular) + shared Code Index layer

One bundle, three platform kits with identical shape, plus a shared code-index layer.

```
ai-context-kits/
  shared/code-index/        # schema, templates, prompts, steering, rules, build + query scripts, hook (source of truth for the layer)
  ios/                      # Swift/SwiftUI/UIKit kit  (REPORT.md, docs/ai, .kiro, scripts/ai-sync.sh + ai-files.yaml, scripts/ai/*.py)
  android/                  # Kotlin/Compose kit       (REPORT.md, docs/ai, .kiro, scripts/ai/generate.py)
  angular/                  # Angular 22 kit           (REPORT.md, docs/ai, .kiro, scripts/ai/generate.py, MCP config)
```

## What every kit contains
| Layer | Purpose | Files |
|---|---|---|
| **Steering** (how the repo is built) | versions, architecture, conventions, testing, contracts, exemplars, guardrails, security | `docs/ai/*.md` → `.kiro/steering/*.md` (+ generated AGENTS.md / CLAUDE.md / Cursor / Copilot / Windsurf / Junie) |
| **Specs** (what to build) | EARS requirements, design (with Impact section), tasks, bugfix | `.kiro/specs/_template/` |
| **Code index** (what exists, who depends on it, what breaks) | flat file graph + contract nodes; generated views: INDEX, directory cards (every file has a row), flow cards (per entry point), promoted component cards, contracts, dependencies (lock file × tech.md allowlist), hotspots, violations | `docs/ai/code-index/`, `scripts/ai/build_code_index.py`, `scripts/ai/query_code_index.py`, `.kiro/steering/code-index.md` |
| **Scan** (fill everything from the repo) | read-only, evidence-cited, UNKNOWN list; ends with building the code index | `docs/ai/repo-scan-prompt.md` (`#repo-scan` / `/repo-scan`) |
| **Gates** | hooks (format, verify after task, protected paths, refresh index), CI drift check | `.kiro/hooks/`, `.github/workflows/` |

## Rollout (per repo, ~half a day)
1. Copy the platform kit's contents into the repo root.
2. Run the scan prompt in Kiro. It fills steering, picks the exemplar, then builds the code index.
3. Tech lead answers `questions.md`, approves the exemplar, reviews INDEX.md + top-10 hotspot cards.
4. Generate per-tool files; enable the CI drift check and the "PR touching src must touch code-index" rule.
5. First feature: spec → impact analysis → design → tasks; measure first-pass build/lint success and iterate steering.

## Workflow the kits enforce
`requirements.md (EARS)` → `query_code_index.py impact` → `design.md` (pastes the impact table, lists contract parties) → `tasks.md` (one slice per task, tests in-task)
→ hooks verify → `update-code-index` (regenerate + summaries + prose, `--check`) → PR.

## Keeping the shared layer in sync
`shared/code-index/` is the source; each platform's `docs/ai/code-index/` (README, schema, impact recipe, prompts, templates, rules) and `scripts/ai/*.py`
are copies, plus a platform-specific `PLATFORM.md` (entry points, bucket rules, tools that replace the regex extractors). When you improve a prompt or a
script, copy it into the three kits (or symlink in your own monorepo of kits).

See each kit's `README.md` and `REPORT.md` for platform details and the research behind them.
