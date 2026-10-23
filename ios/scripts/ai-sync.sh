#!/usr/bin/env bash
# Generates per-tool AI instruction files from the canonical docs/ai/*.md.
# Usage: scripts/ai-sync.sh        -> write files
#        scripts/ai-sync.sh --check -> exit 1 if generated files are stale (for CI)
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=docs/ai
CHECK=${1:-}
TMP=$(mktemp -d)

emit() { # path content
  mkdir -p "$TMP/$(dirname "$1")"; printf '%s' "$2" > "$TMP/$1"
}
body() { cat "$SRC/$1"; }

# --- AGENTS.md: always-scoped files, link to the rest
AG="# AGENTS.md — generated from docs/ai (edit there, run scripts/ai-sync.sh)

"
for f in product.md tech.md structure.md architecture.md; do AG+="$(body $f)

"; done
AG+="See docs/ai/ for conventions, testing, api-contracts, exemplars, ios-api-guardrails.
"
emit AGENTS.md "$(printf "$AG")"
emit CLAUDE.md "@AGENTS.md
"

# --- scoped rules
gen_rule() { # file globs description
  local f=$1 globs=$2 desc=$3 base=${1%.md}
  emit ".claude/rules/$base.md" "$(printf -- "---
paths: [%s]
---
%s" "$globs" "$(body $f)")"
  emit ".cursor/rules/$base.mdc" "$(printf -- "---
description: %s
globs: [%s]
alwaysApply: false
---
%s" "$desc" "$globs" "$(body $f)")"
  emit ".github/instructions/$base.instructions.md" "$(printf -- "---
applyTo: \"%s\"
---
%s" "${globs//\"/}" "$(body $f)")"
  emit ".devin/rules/$base.md" "$(printf -- "---
trigger: glob
globs: [%s]
description: %s
---
%s" "$globs" "$desc" "$(body $f)")"
}
gen_rule conventions.md '"**/*.swift"' "Swift coding conventions"
gen_rule ios-api-guardrails.md '"**/*.swift"' "iOS API guardrails"
gen_rule testing.md '"**/*Tests/**/*.swift", "**/Tests/**/*.swift"' "Testing and quality gates"
gen_rule api-contracts.md '"**/Networking/**", "**/Data/**", "**/*DTO*.swift"' "API contracts and data mapping"
emit ".cursor/rules/exemplars.mdc" "$(printf -- "---
description: Golden-path feature & shared infra to copy for new features/tests
alwaysApply: false
---
%s" "$(body exemplars.md)")"
emit ".devin/rules/exemplars.md" "$(printf -- "---
trigger: model_decision
description: Golden-path feature & shared infra to copy for new features/tests
---
%s" "$(body exemplars.md)")"

if [[ "$CHECK" == "--check" ]]; then
  if diff -r "$TMP" . --exclude='.*' --exclude='docs' --exclude='scripts' >/dev/null 2>&1 \
     && diff -r "$TMP/.claude" .claude >/dev/null 2>&1 && diff -r "$TMP/.cursor" .cursor >/dev/null 2>&1; then
    echo "AI files up to date"; exit 0
  else echo "AI files are stale — run scripts/ai-sync.sh"; exit 1; fi
fi
cp -R "$TMP"/. .
echo "Generated AGENTS.md, CLAUDE.md, .claude/rules, .cursor/rules, .github/instructions, .devin/rules"
