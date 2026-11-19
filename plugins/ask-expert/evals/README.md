# evals

케이스 형식은 [`plugins/friction-loop/evals/README.md`](../../friction-loop/evals/README.md)를 따른다. 기준을 바꿀 때마다 그 실패를 재현하는 케이스를 여기에 더한다.

| 케이스 | 확인하는 것 |
|---|---|
| `state-location` | 상태를 어디에 둘지 묻는 보통 무게의 질문에 아키텍트에게 자문하고, 넘긴 브리프에 Claude가 떠올린 안(URL 쿼리 등)을 끼워 넣지 않으며, 권장안과 포기하는 것이 달린 번호 결정으로 돌려준다 |
| `challenge-hypothesis` | 사용자가 자기 가설을 검토해 달라고 하면 반박 모드로 부르고, 가설을 그대로 맞다고 돌려주지 않는다 |
| `proactive-bridge` | 묻지 않았어도 구현 요청에 앱-웹 계약 같은 되돌리기 어려운 결정이 있으면 먼저 자문하고, 사용자가 정하기 전까지 구현을 멈춘다 |
| `script-naming` | 몇 줄 고치면 되돌릴 수 있는 결정에는 아키텍트를 부르지 않고 권장안과 포기하는 것을 바로 답한다. skill 발동은 보지 않는다(2026-11-17 측정에서 skill 없이도 이 답이 나왔다) |
| `risk-scan-parallel` | 여러 관점에 걸친 무거운 설계(결제) 문서의 위험을 찾을 때 렌즈별로 나눠 2~3번 부르고, 심어 둔 위험 여섯 가지 가운데 다섯 이상을 필수 수정과 확인 필요로 나눠 돌려준다 |
| `fact-lookup-no-trigger` | "검토해줘"로 끝나도 사실 확인에는 발동하지 않는다 |

결정적으로 볼 수 있는 것(skill 발동, 아키텍트 호출 횟수, 브리프에 든 말)은 `tool_used`로, 답의 모양과 내용은 `llm`으로 채점한다. `llm` 채점은 마지막 응답만 본다. 그래서 브리프의 중립성은 `tool_used`의 `input_match`로 Agent 입력을 직접 검사한다.

`brief-no-seed`는 사용자가 후보를 말하지 않은 질문에서 브리프에 URL 쿼리 같은 안이 들어 있으면 실패한다. Claude가 자기 안을 심어 아키텍트를 앵커링했다는 신호다. 다른 말로 같은 안을 심으면 놓친다.

## 실행

플러그인 폴더에서 실행한다. 실제 모델을 부르므로 비용이 든다. 아키텍트는 Opus에 effort `xhigh`로 돌아서 호출 한 번이 무겁다. 처음에는 케이스 하나씩 돌려 비용을 확인한다.

```bash
cd plugins/ask-expert
claude plugin eval . --scaffold --case state-location --runs 1 --no-publish --max-cost-usd 5
claude plugin eval . --scaffold --allow-tools Write Edit --no-publish --max-cost-usd 40   # 전체
```

- `--scaffold`: 케이스마다 `fixture.sh`로 작은 예제 저장소나 설계 문서를 만든다.
- `--allow-tools Write Edit`: `proactive-bridge`는 Claude가 구현을 시작할 수 있어야 멈추는지 볼 수 있다.
- 기본으로 플러그인 없이 돌린 결과도 함께 나온다. `skill-fired`와 `arm: with-only` 채점기는 플러그인이 발동했는지 보는 표시라 점수에 넣지 않는다.
- 샌드박스가 켜진 Claude Code 세션 안에서 실행하면 eval이 임시 폴더를 만들다 막힌다. 터미널에서 직접 실행한다.

## 다음 실험

architect 하나에 렌즈를 싣는 지금 구성(A)과, 정체성별 agent 셋이 각자 답하고 메인 Claude가 종합하는 구성(B)을 같은 케이스로 비교한다. B는 비교용 브랜치에만 만든다. 케이스마다 미리 적어 둔 꼭 짚어야 할 점을 몇 개 짚었는지, 권장안이 하나인지, 포기하는 것을 밝혔는지, 시간과 비용을 본다. B가 꼭 짚을 점을 A보다 꾸준히 더 짚으면 그때 나눈다. 나눈다면 기준 대조가 가장 많은 사용자 경험·신뢰성(성능, 접근성, 보안)부터 떼어 낸다.
