# friction-loop: 자가개선 루프

쓰면 쓸수록 개인 확장 시스템이 나아지게 하는 최소 루프다. 사용자가 할 일은 두 가지뿐이다.

1. **기록 한 줄**: 불편한 순간에 `마찰: <무엇이 불편했나>`를 입력한다. hook이 기록하고 Claude에게는 보내지 않으므로 토큰이 들지 않는다. `friction:`도 된다.
2. **승인 한 번**: 일주일에 한 번 이 저장소에서 `/friction-loop:improve`를 실행하고, 제안 표에서 반영할 번호를 고른다.

```
마찰 기록 ──┐
            ├─▶ /friction-loop:improve ─▶ 제안 표 ─▶ 승인 ─▶ plugins/ 변경 + eval ─▶ docs/decisions.md
대화 기록 ──┘     (묶기·형태 선택)                                         (처리한 마찰 ID, 주간 지표)
```

## 구성

| 파일 | 역할 |
|---|---|
| `hooks/hooks.json` | `UserPromptSubmit` hook. `마찰:` 프롬프트를 기록하고 막는다 |
| `scripts/friction.py` | 기록(`hook`, `add`)과 조회(`list`, `stats`) |
| `scripts/recent_prompts.py` | 최근 N일 직접 입력한 프롬프트를 대화 기록에서 뽑는다 (읽기 전용) |
| `skills/improve/SKILL.md` | 주간 검토. 직접 불렀을 때만 돈다 |
| `evals/` | 변경마다 재현 케이스가 하나씩 쌓인다 |

마찰 기록은 `${CLAUDE_PLUGIN_DATA}/friction.jsonl`에 쌓여 플러그인을 업데이트해도 남는다. 처리 여부는 저장소의 `docs/decisions.md`에 적힌 마찰 ID로 판단하므로, 무엇을 왜 고쳤는지가 코드 변경과 같은 곳에 남는다.

## 설치

```bash
claude plugin marketplace add aumilkyeong/plugin-playground
claude plugin install friction-loop@aumilkyeong
```

세션에서 `마찰: 테스트`를 입력하면 `마찰 F-001 기록` 메시지가 보여야 한다. 주간 검토(`/friction-loop:improve`)까지 쓰는 방법은 [저장소 README의 빠른 시작](../../README.md#빠른-시작)에 있다.

## 개발

설치하지 않고 이 세션에만 불러온다. 저장소 루트에서 실행한다.

```bash
claude --plugin-dir ./plugins/friction-loop
```

`--plugin-dir`로 띄운 개발본과 설치본은 플러그인 ID가 달라 데이터 폴더도 다를 수 있다. 실제 기록은 설치본으로 쌓는다.

## 설계 메모

- **포착을 skill이 아니라 hook으로 둔 이유**: hook은 샌드박스 밖에서 돌아 플러그인 데이터 폴더에 쓸 수 있고, 모델을 거치지 않아 즉시 끝난다. skill이 Bash로 기록하면 샌드박스가 켜진 환경에서 `~/.claude/plugins/data` 쓰기가 막힌다.
- **hook은 모든 프롬프트에 불린다**(`/loop`, 백그라운드 agent 보고 포함). 접두어가 없으면 아무것도 출력하지 않는다. 출력이 생기면 Claude의 컨텍스트에 들어가기 때문이다.
- **자기 수정은 제안까지만 자동**이다. hook은 사용자 권한으로 샌드박스 밖에서 돌기 때문에, 반영은 항상 승인을 거친다.
