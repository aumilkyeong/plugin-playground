#!/usr/bin/env bash
# 포크 직후처럼 결정 기록(docs/decisions.md)이 없는 시스템 저장소와, 두 세션에서 npm test가 거듭 실패한 대화 기록을 만든다.
# 두 세션 모두 사용자가 중단한 뒤 pnpm을 쓰라고 바로잡는다. 묶을 거리가 있어야 검토가 제안 표에서 멈추고, 기록 단계로 넘어가지 않는다.
set -euo pipefail

mkdir -p .claude-plugin plugins
cat > .claude-plugin/marketplace.json <<'EOF'
{"name": "eval", "owner": {"name": "eval"}, "plugins": []}
EOF

ts=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
dir="$HOME/.claude/projects/-work-demo"
mkdir -p "$dir"
for s in s1 s2; do
  case $s in
    s1) fix="이 저장소는 pnpm만 써. pnpm test로 돌려" ;;
    s2) fix="pnpm 쓰라고 했잖아. npm 말고 pnpm test" ;;
  esac
  meta="\"sessionId\":\"eval-$s\",\"cwd\":\"/work/demo\",\"timestamp\":\"$ts\",\"isSidechain\":false"
  cat > "$dir/eval-$s.jsonl" <<EOF
{"type":"user",$meta,"promptSource":"typed","message":{"role":"user","content":"테스트 돌려줘"}}
{"type":"assistant",$meta,"message":{"role":"assistant","content":[{"type":"tool_use","id":"$s-t1","name":"Bash","input":{"command":"npm test"}}]}}
{"type":"user",$meta,"message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"$s-t1","is_error":true,"content":"Exit code 1\nnpm error Missing script: \"test\""}]}}
{"type":"assistant",$meta,"message":{"role":"assistant","content":[{"type":"tool_use","id":"$s-t2","name":"Bash","input":{"command":"npm run test"}}]}}
{"type":"user",$meta,"message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"$s-t2","is_error":true,"content":"Exit code 1\nnpm error Missing script: \"test\""}]}}
{"type":"assistant",$meta,"message":{"role":"assistant","content":[{"type":"tool_use","id":"$s-t3","name":"Bash","input":{"command":"npm install"}}]}}
{"type":"user",$meta,"message":{"role":"user","content":[{"type":"text","text":"[Request interrupted by user]"}]}}
{"type":"user",$meta,"promptSource":"typed","message":{"role":"user","content":"$fix"}}
EOF
done
