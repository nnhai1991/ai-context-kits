# UPDATE CODE INDEX — run after each spec task / before opening a PR

1. Regenerate (fast, idempotent; the graph is never edited by hand):
       python3 scripts/ai/build_code_index.py --platform {{p}}
2. `python3 scripts/ai/query_code_index.py stale` → for every file you changed, rewrite its `summary` in `annotations.json`
   if the one-line meaning changed; otherwise just refresh its `sourceHash` to the current value shown in `graph.json`.
   New file → write its summary (replace the `AUTO:` line). Deleted file → remove its entry from `annotations.json` (`_orphans` lists them).
3. Prose: update the **flow card** of any flow whose invariant changed, the **component card** of any promoted node you touched, and the
   **directory card** if the directory's purpose or public surface changed. If the script promoted a node you touched (it now has a
   `components/*.md` with placeholders), write its three prose sections now.
4. Contracts: `python3 scripts/ai/query_code_index.py contract <id>` for every endpoint, table, route, event or flag you changed; report every
   party in the PR description. A contract change without every party updated is a blocking finding.
5. `python3 scripts/ai/query_code_index.py violations` → zero new violations, or an explicit justification in the PR.
   A new third-party import must first be added to the `tech.md` allowlist by the tech lead; `dependencies.md` shows it as `not on allowlist` until then.
6. `python3 scripts/ai/build_code_index.py --platform {{p}} --check` must pass. Commit `docs/ai/code-index/**` in the same PR.
   CI rule: regenerated views must be committed (no diff after a CI run), and a PR that touches a promoted node must touch its card.
