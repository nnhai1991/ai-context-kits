---
inclusion: auto
name: code-index
description: How to use the repository code index (file map, flows, contracts, dependents, impact) before designing, changing, or reviewing any code.
---
# Code index — consult before you design or change code

The repo keeps a code index at `docs/ai/code-index/`: `INDEX.md` (directories, flows, cross-cutting components, hotspots), `dirs/*.md`
(one row per file), `flows/*.md` (what each entry point reaches), `components/*.md` (promoted nodes only), `contracts.md`, `graph.json` (source of truth).

Rules:
1. Never read `graph.json` directly. Ask it: `python3 scripts/ai/query_code_index.py impact|dependents|flows|tests|contract|find|node <file>`.
2. Before writing `design.md` or touching an existing file: run `impact` on the files you will change, read the flow cards it names, then
   **read the source files it lists**. The index holds no signatures or bodies; it tells you where to look and what breaks.
3. Prefer extending a component found with `find` over creating a parallel one. Search by purpose, then by glossary term, then by symbol.
4. Nodes with `risk: high`, a card in `components/`, or a place in `hotspots.md` are review-required: smallest change, tests first, no refactors by side effect, and the design must say how the change keeps the card's invariants.
5. A contract change (endpoint, DTO field, schema, route params, event payload, flag) is stop-and-ask. List every party from `query contract <id>` in the question.
6. New dependency edges must respect `rules/allowed-edges.json`; `query violations` must not grow. Never "modernize by side effect".
7. After implementing, follow `prompts/update-code-index.md`: regenerate, rewrite the summaries of changed files, update the prose of touched
   flows and promoted cards, and make `build_code_index.py --check` pass. A changed file must not leave a stale summary.
8. The index is evidence, not truth: when a row, card or flow and the code disagree, trust the code, fix the index, and note it.
9. If `INDEX.md` is missing or `generatedAt` is older than the last 50 commits, say so and regenerate before designing.
