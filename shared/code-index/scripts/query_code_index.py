#!/usr/bin/env python3
"""query_code_index.py — ask the code index questions so agents never read graph.json. Stdlib only.

  python3 scripts/ai/query_code_index.py <command> [args] [--index docs/ai/code-index] [--depth 3] [--json]

Commands:
  find <text>                 search ids, symbols and summaries
  node <path|id>              one node: summary, facets, uses, used-by, flows, tests, card
  dependents <path|id>        reverse walk to --depth (default 3); low-confidence edges shown as 'possible'
  flows <path|id>             flows the node sits in, with their key paths
  tests <path|id> [...]       union of tests covering these nodes
  contract <id>               every provider and consumer of a contract node (endpoint:, storage:, route:, event:, flag:)
  impact <path|id> [...]      the design.md › Impact table + 'Read these files' + 'Contract parties' (+ --contract for any-depth contract walk)
  violations                  rule violations
  stale                       nodes whose agent summary predates the current file
Paths may be given with or without extension; ids are paths without extension.
"""
import argparse, collections, json, os, sys

STRUCTURAL = {"imports", "extends", "implements", "injects"}
BEHAVIOURAL = {"calls", "observes", "navigates_to"}
PROVIDER = {"exposes_endpoint", "defines_route", "emits", "writes"}
CONSUMER = {"consumes_endpoint", "navigates_to", "observes", "reads"}

def load(index):
    gp = os.path.join(index, "graph.json")
    if not os.path.exists(gp): sys.exit(f"no graph at {gp}; run build_code_index.py first")
    g = json.load(open(gp))
    if g.get("version") != 2: sys.exit("graph.json is not version 2; rebuild with build_code_index.py")
    nodes = {n["id"]: n for n in g["nodes"]}
    inc, outg = collections.defaultdict(list), collections.defaultdict(list)
    for e in g["edges"]: inc[e["to"]].append(e); outg[e["from"]].append(e)
    return g, nodes, inc, outg

def resolve(nodes, ref):
    if ref in nodes: return ref
    base = ref.rsplit(".", 1)[0] if "." in os.path.basename(ref) else ref
    base = base.lstrip("./")
    if base in nodes: return base
    hits = [i for i in nodes if i.endswith("/" + base) or i == base or nodes[i].get("path") == ref]
    if len(hits) == 1: return hits[0]
    hits = [i for i in nodes if base in i or any(base == s for s in nodes[i].get("symbols", []))]
    if len(hits) == 1: return hits[0]
    sys.exit(f"cannot resolve '{ref}' ({len(hits)} candidates: {hits[:8]})")

def label(nodes, i): return nodes[i].get("path", i) if i in nodes else i
def card(nodes, i):
    n = nodes.get(i, {})
    if n.get("class") != "code": return "contracts.md"
    slug = lambda s: "".join(ch if ch.isalnum() else "_" for ch in s).replace("__", "__").strip("_")
    import re
    sl = re.sub(r"[^A-Za-z0-9]+", "__", i).strip("_")
    return f"components/{sl}.md" if n.get("tier") == "card" else f"dirs/{re.sub(r'[^A-Za-z0-9]+', '__', n['facets']['dir']).strip('_') or 'root'}.md"

def dependents(nodes, inc, start, depth, include_low=False):
    """returns {id: (depth, via_type, confidence, through)}"""
    seen = {start: (0, "", "", "")}; frontier = [start]
    for d in range(1, depth + 1):
        nxt = []
        for cur in frontier:
            for e in inc[cur]:
                if e["type"] not in STRUCTURAL | BEHAVIOURAL | {"consumes_endpoint", "reads", "observes"}: continue
                if e["confidence"] == "low" and not include_low: continue
                if e["type"] == "navigates_to" and d > 1: continue  # another flow starts there
                fr = e["from"]
                if fr in seen or nodes.get(fr, {}).get("kind") == "test": continue
                seen[fr] = (d, e["type"], e["confidence"], cur); nxt.append(fr)
        frontier = nxt
    del seen[start]
    return seen

def possible(nodes, inc, i): return sorted({e["from"] for e in inc[i] if e["confidence"] == "low" and nodes.get(e["from"], {}).get("kind") != "test"})
def tests_of(outg, ids): return sorted({e["to"] for i in ids for e in outg[i] if e["type"] == "tested_by"})
def risk_score(n): m = n.get("metrics", {}); return m.get("fanIn", 0) * (m.get("churn6m", 0) + 1) * (1 if m.get("testCount", 0) else 3)

def cmd_find(g, nodes, inc, outg, a):
    q = a.args[0].lower(); rows = []
    for i, n in nodes.items():
        if q in i.lower() or q in n.get("summary", "").lower() or any(q in s.lower() for s in n.get("symbols", [])): rows.append(n)
    out("| Node | Kind | Summary | Card |\n|---|---|---|---|\n" + "".join(f"| `{i['id']}` | {i['kind']} | {i.get('summary','')} | {card(nodes, i['id'])} |\n" for i in rows[:40]), rows, a)

def cmd_node(g, nodes, inc, outg, a):
    i = resolve(nodes, a.args[0]); n = nodes[i]; m = n.get("metrics", {})
    uses = sorted({e["to"] for e in outg[i] if e["confidence"] != "low" and not e["to"].startswith("ext:") and e["type"] != "tested_by"})
    used = sorted({e["from"] for e in inc[i] if e["confidence"] != "low" and e["type"] != "tested_by"})
    txt = [f"# {i}", f"- path: {n.get('path','')} · kind: {n['kind']} · layer: {n.get('facets',{}).get('layer','')} · dir: {n.get('facets',{}).get('dir','')} · tier: {n.get('tier')} · risk: {n.get('risk')}{' · STALE' if n.get('stale') else ''}",
           f"- summary: {n.get('summary','')}", f"- metrics: fan-in {m.get('fanIn',0)}, churn6m {m.get('churn6m',0)}, tests {m.get('testCount',0)}, flows {m.get('flowCount',0)}",
           f"- card: {card(nodes, i)}", "- uses: " + (", ".join(uses) or "—"), "- used by: " + (", ".join(used) or "—"),
           "- possible (low-confidence): " + (", ".join(possible(nodes, inc, i)) or "—"),
           "- flows: " + (", ".join(n.get("facets", {}).get("flows", [])) or "—"), "- tests: " + (", ".join(label(nodes, t) for t in tests_of(outg, [i])) or "— none")]
    out("\n".join(txt), {"node": n, "uses": uses, "usedBy": used}, a)

def cmd_dependents(g, nodes, inc, outg, a):
    i = resolve(nodes, a.args[0]); deps = dependents(nodes, inc, i, a.depth)
    rows = sorted(deps.items(), key=lambda kv: (kv[1][0], kv[0]))
    txt = f"Dependents of `{i}` to depth {a.depth} ({len(rows)}):\n| Node | Depth | Via | Confidence | Through |\n|---|---|---|---|---|\n" + \
          "".join(f"| `{k}` | {v[0]} | {v[1]} | {v[2]} | `{v[3]}` |\n" for k, v in rows)
    pos = possible(nodes, inc, i)
    if pos: txt += "\nPossible (low-confidence symbol match, verify by reading): " + ", ".join(f"`{p}`" for p in pos)
    out(txt, {"dependents": {k: {"depth": v[0], "via": v[1], "confidence": v[2], "through": v[3]} for k, v in rows}, "possible": pos}, a)

def cmd_flows(g, nodes, inc, outg, a):
    i = resolve(nodes, a.args[0]); fls = [f for f in g["flows"] if i in f["files"] or i in f.get("contracts", []) or f["entry"] == i]
    txt = f"Flows through `{i}` ({len(fls)}):\n" + "".join(f"- **{f['id']}** (entry `{label(nodes, f['entry'])}`, {len(f['files'])} files, {len(f['tests'])} tests): " + " → ".join(label(nodes, x) for x in f["keyPath"]) + f"\n  card: flows/{f['id']}.md\n" for f in fls)
    out(txt, fls, a)

def cmd_tests(g, nodes, inc, outg, a):
    ids = [resolve(nodes, x) for x in a.args]; ts = tests_of(outg, ids)
    out("Tests covering " + ", ".join(ids) + ":\n" + ("\n".join(f"- {label(nodes, t)}" for t in ts) or "- none found"), ts, a)

def cmd_contract(g, nodes, inc, outg, a):
    cid = a.args[0]
    if cid not in nodes: sys.exit(f"unknown contract {cid}; contracts look like endpoint:GET /v1/x, storage:x, route:x, event:x, flag:x")
    prov = sorted({e["from"] for e in inc[cid] if e["type"] in PROVIDER}); cons = sorted({e["from"] for e in inc[cid] if e["type"] in CONSUMER})
    out(f"Contract `{cid}` — providers: {', '.join(prov) or '—'}; consumers: {', '.join(cons) or '—'}\nA change here affects every party listed; this is stop-and-ask.", {"providers": prov, "consumers": cons}, a)

def cmd_impact(g, nodes, inc, outg, a):
    targets = [resolve(nodes, x) for x in a.args]
    rows, read_files, parties = {}, set(), {}
    for t in targets:
        n = nodes[t]
        rows[t] = ("target", 0, "the change itself", "behaviour", n)
        for k, (d, via, conf, thr) in dependents(nodes, inc, t, a.depth).items():
            why = f"{via} `{label(nodes, t) if d == 1 else label(nodes, thr)}` ({conf})"
            if k not in rows or rows[k][1] > d: rows[k] = ("dependent", d, why, "behaviour", nodes[k])
        for p in possible(nodes, inc, t):
            if p not in rows: rows[p] = ("possible", 9, f"symbol match on `{label(nodes, t)}` (low confidence, verify)", "none", nodes[p])
        # contracts this node provides or consumes
        for e in outg[t]:
            c = e["to"]
            if c in nodes and nodes[c]["class"] == "contract":
                if e["type"] in PROVIDER or a.contract:
                    others = sorted({x["from"] for x in inc[c] if x["from"] != t})
                    if others: parties[c] = others
                    for o in others:
                        if o not in rows: rows[o] = ("contract-party", 1, f"shares `{c}` with `{label(nodes, t)}`", "contract", nodes[o])
        if n["class"] == "contract":
            others = sorted({x["from"] for x in inc[t]}); parties[t] = others
            for o in others: rows[o] = ("contract-party", 1, f"party on `{t}`", "contract", nodes[o])
    tests = tests_of(outg, [k for k in rows if nodes.get(k, {}).get("class") == "code"])
    high_risk = [k for k, r in rows.items() if r[4].get("risk") == "high"]
    ranked = sorted((k for k in rows if rows[k][0] != "target"), key=lambda k: -risk_score(rows[k][4]))[:5]
    txt = ["## Impact (generated by query_code_index.py; paste into design.md › Impact)", "",
           "| Node | Why affected | Change type | Tests | Needs human review? |", "|---|---|---|---|---|"]
    for k, (cls, d, why, ct, n) in sorted(rows.items(), key=lambda kv: (kv[1][1], kv[0])):
        ts = tests_of(outg, [k]) if n.get("class") == "code" else []
        review = "yes" if n.get("risk") == "high" or ct == "contract" or n.get("tier") == "card" else "no"
        txt.append(f"| `{label(nodes, k)}` | {why} | {ct} | {', '.join(label(nodes, x) for x in ts) or '— none'} | {review} |")
        if n.get("class") == "code" and cls != "possible": read_files.add(n.get("path", k))
    txt += ["", f"**Tests to run:** {', '.join(label(nodes, t) for t in tests) or 'none found'}" + ("; plus the full suite of: " + ", ".join(f"`{label(nodes, h)}`" for h in high_risk) if high_risk else ""),
            f"**Top risk in radius:** " + (", ".join(f"`{label(nodes, k)}` ({risk_score(rows[k][4])})" for k in ranked) or "—"), "",
            "**Read these files** (the index holds no signatures; open them):"] + [f"- {p}" for p in sorted(read_files)]
    txt += ["", "**Contract parties** (stop-and-ask if the contract changes):"] + ([f"- `{c}`: " + ", ".join(label(nodes, o) for o in os_) for c, os_ in parties.items()] or ["- none"])
    txt += ["", "**Cards to read:** " + ", ".join(sorted({card(nodes, k) for k in rows if nodes.get(k, {}).get('class') == 'code'}))]
    out("\n".join(txt), {"rows": {k: {"class": v[0], "depth": v[1], "why": v[2], "changeType": v[3]} for k, v in rows.items()}, "tests": tests, "readFiles": sorted(read_files), "contractParties": parties}, a)

def cmd_violations(g, nodes, inc, outg, a):
    v = g.get("violations", [])
    out(f"{len(v)} violations\n" + "".join(f"- `{x['from']}` -> `{x['to']}` ({x['type']}): {x['rule']} [{x['evidence']}]\n" for x in v), v, a)

def cmd_stale(g, nodes, inc, outg, a):
    s = [n for n in nodes.values() if n.get("stale")]
    out(f"{len(s)} stale summaries\n" + "".join(f"- {n['path']} (tier {n.get('tier')})\n" for n in s), [n["id"] for n in s], a)

def out(text, data, a): print(json.dumps(data, indent=1, default=str) if a.json else text)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["find", "node", "dependents", "flows", "tests", "contract", "impact", "violations", "stale"])
    ap.add_argument("args", nargs="*"); ap.add_argument("--index", default="docs/ai/code-index"); ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--contract", action="store_true", help="impact: walk every contract the target consumes, not only the ones it provides")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.command not in ("violations", "stale") and not a.args: sys.exit("missing argument")
    g, nodes, inc, outg = load(a.index)
    globals()["cmd_" + a.command](g, nodes, inc, outg, a)

if __name__ == "__main__": main()
