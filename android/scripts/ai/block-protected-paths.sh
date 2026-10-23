#!/usr/bin/env bash
# Kiro PreToolUse hook: exit 2 blocks the tool call. Reads hook context JSON on stdin.
# Verify the JSON field names and tool-name matcher against your Kiro version's docs.
set -euo pipefail
input=$(cat)
path=$(printf '%s' "$input" | python3 -c 'import sys,json
d=json.load(sys.stdin); t=d.get("tool_input",d)
print(t.get("path") or t.get("file_path") or t.get("filePath") or "")' 2>/dev/null || true)
if printf '%s' "$path" | grep -Eq '(^|/)build/|/generated/|local\.properties$|\.jks$|\.keystore$|gradle/wrapper/|google-services\.json$'; then
  echo "Blocked: $path is a protected/generated file. Edit the source of truth instead." >&2
  exit 2
fi
exit 0
