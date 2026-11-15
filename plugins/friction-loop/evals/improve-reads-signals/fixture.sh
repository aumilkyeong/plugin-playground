#!/usr/bin/env bash
# 시스템 저장소처럼 보이는 작업 폴더와, 두 세션에서 npm test가 거듭 실패한 대화 기록을 만든다.
# 두 세션 모두 사용자가 중단한 뒤 pnpm을 쓰라고 바로잡는다. 사용자는 '마찰:'로 기록하지 않았다.
set -euo pipefail

mkdir -p .claude-plugin docs plugins
cat > .claude-plugin/marketplace.json <<'EOF'
{"name": "eval", "owner": {"name": "eval"}, "plugins": []}
EOF
cat > docs/decisions.md <<'EOF'
# 자가개선 시스템 결정 기록

## 주간 지표

| 주(시작일) | 마찰 기록 | 반복 지시 | 신호 | 반영 | 지움 | 메모 |
|---|---|---|---|---|---|---|

## 변경 기록
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
