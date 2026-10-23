# Impact analysis recipe

Run it, do not compute it by hand:

    python3 scripts/ai/query_code_index.py impact <path-or-id> [<path-or-id> ...] [--depth 3] [--contract]

What the query does (so you can judge its output):
1. **Direct dependents** = reverse of every high/medium structural or behavioural edge into the node
   (`imports`, `extends`, `implements`, `injects`, `calls`, `observes`, `navigates_to`). Low-confidence edges are listed as *possible*.
2. **Transitive blast radius** = repeat to `--depth` (default 3). The walk stops at `navigates_to` (another flow starts there).
3. **Contract changes** (`--contract`, or when the node is a contract node: endpoint, storage, route, event, flag):
   every party on the contract at any depth, no stop condition. This is always stop-and-ask.
4. **Flows** = every flow the node sits in; **tests** = union of `tested_by` edges over everything reached, plus the full suite of any high-risk node.
5. **Risk ranking** = fanIn × (churn6m + 1) × (1 if tests else 3); top 5 shown.
6. Output = the table for `design.md › Impact` (`Node | Why affected | Change type | Tests | Needs human review?`),
   a **Read these files** list (open them; the index does not hold their contents), and a **Contract parties** list.
7. Paste the table into `design.md › Impact`; add every contract change to the spec's stop-and-ask list.
