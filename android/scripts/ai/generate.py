#!/usr/bin/env python3
"""Generate tool-specific AI context files from docs/ai (canonical). Stdlib only."""
import json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "docs" / "ai"
HEADER = "<!-- GENERATED from docs/ai by scripts/ai/generate.py — do not edit -->\n"
SKIP = {"scan-report.md", "questions.md"}

def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta, body = {}, text
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); v = v.strip()
                meta[k.strip()] = json.loads(v) if v.startswith("[") else v.strip('"')
    meta.setdefault("scope", "always"); meta.setdefault("id", path.stem)
    return meta, body.strip() + "\n"

def write(rel, content):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")

docs = [parse(p) for p in sorted(SRC.glob("*.md")) if p.name not in SKIP]
for d in [".claude/rules", ".cursor/rules", ".github/instructions", ".devin/rules", ".junie/rules"]:
    shutil.rmtree(ROOT / d, ignore_errors=True)

always = [b for m, b in docs if m["scope"] == "always"]
index = "\n".join(f"- `{m['id']}` ({m['scope']}{': ' + ','.join(m.get('globs', [])) if m.get('globs') else ''}) — docs/ai/{m['id']}.md"
                  for m, _ in docs if m["scope"] != "always")
write("AGENTS.md", HEADER + "\n".join(always) + "\n## Scoped rules (read when relevant)\n" + index + "\n")
write("CLAUDE.md", HEADER + "@AGENTS.md\n")

for m, body in docs:
    i, g, s = m["id"], m.get("globs", []), m["scope"]
    desc = m.get("description", "")
    kiro_name = "repo-scan" if i == "repo-scan" else i
    kiro = {"always": "inclusion: always", "manual": "inclusion: manual",
            "glob": f"inclusion: fileMatch\nfileMatchPattern: {json.dumps(g)}",
            "auto": f"inclusion: auto\nname: {i}\ndescription: \"{desc}\""}[s]
    write(f".kiro/steering/{kiro_name}.md", f"---\n{kiro}\n---\n{body}")
    if s == "always":
        continue  # already in AGENTS.md for the other tools
    paths = "paths:\n" + "".join(f'  - "{x}"\n' for x in g) if g else ""
    write(f".claude/rules/{i}.md", (f"---\n{paths}---\n" if paths else "") + HEADER + body)
    cur = f'description: "{desc}"\n' + (f"globs: {','.join(g)}\n" if g else "") + "alwaysApply: false\n"
    write(f".cursor/rules/{i}.mdc", f"---\n{cur}---\n{HEADER}{body}")
    if g:
        write(f".github/instructions/{i}.instructions.md", f'---\napplyTo: "{",".join(g)}"\n---\n{HEADER}{body}')
    trig = {"glob": f"trigger: glob\nglobs: {','.join(g)}", "auto": f"trigger: model_decision\ndescription: {desc}",
            "manual": "trigger: manual"}[s]
    write(f".devin/rules/{i}.md", f"---\n{trig}\n---\n{HEADER}{body}")
    write(f".junie/rules/{i}.md", HEADER + body)
print("generated", len(docs), "docs")
