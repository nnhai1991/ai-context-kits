# IMPACT ANALYSIS — run before writing design.md

1. Resolve the change to files: the files you expect to modify, plus any contract (`endpoint:`, `storage:`, `route:`, `event:`, `flag:`) you expect to change.
2. Run:
       python3 scripts/ai/query_code_index.py impact <file> [<file> ...] [--depth 3] [--contract]
   Use `--contract` when a DTO field, schema, route param or event payload will change.
3. Read, in this order: the flow cards listed for the files (`flows <file>`), the cards listed under **Cards to read**, and every file under
   **Read these files**. The index does not hold signatures; the source does.
4. Paste the generated table into `design.md › Impact`. Add every line under **Contract parties** to the spec's stop-and-ask list.
5. If the table lists a `possible` row, open that file and either confirm it (keep the row, note the evidence) or drop it.
6. If a node you will touch has risk high or a card, the design must say how the change keeps that card's invariants.
