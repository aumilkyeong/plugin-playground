# evals

케이스 형식은 [`plugins/friction-loop/evals/README.md`](../../friction-loop/evals/README.md)를 따른다. 기준을 바꿀 때마다 그 실패를 재현하는 케이스를 여기에 더한다.

| 케이스 | 확인하는 것 |
|---|---|
| `process-flowchart-in-doc` | 갈래와 되돌아가는 길이 있는 과정을 문서에 도식화하면, 판단 갈래가 보이는 Mermaid 흐름도에 화살표 레이블과 메시지를 말하는 제목이나 캡션이 붙는다 |
| `uncertain-hypotheses` | 상관, 가설, 확인된 사실이 섞인 아이디어를 그릴 때 상관과 가설을 확정된 인과처럼 그리지 않는다 |
| `terminal-boxes-korean` | 채팅에서 상자 도식을 부탁하면 터미널 텍스트 도식으로 그리고, 한글 폭 검사(`textwidth.py`)를 돌린다 |
| `simple-fact-no-diagram` | 문장 하나로 답할 수 있는 평소 질문에는 발동하지 않는다 |

결정적으로 볼 수 있는 것(파일, Mermaid 형식, 판단 마름모, 화살표 레이블, 검사 스크립트 실행)은 regex와 tool_used로, 나머지(되돌아가는 길, 제목의 메시지, 정직)는 llm으로 채점한다.

렌더 확인(`render.py`)과 시청자 테스트는 eval에서 보지 않는다. 브라우저가 eval 샌드박스 안에서 뜨지 않기 때문이다. 이 두 단계는 실제 세션에서 확인한다.

## 실행

플러그인 폴더에서 실행한다. 실제 모델을 부르므로 비용이 든다.

```bash
cd plugins/visualize-idea
claude plugin eval . --allow-tools Write Edit "Bash(python3 *)" --no-publish --max-cost-usd 6
```

- `--allow-tools`: 문서 케이스는 파일을 써야 하고, 터미널 케이스는 `textwidth.py`를 돌려야 한다.
- 샌드박스가 켜진 Claude Code 세션 안에서 실행하면 eval이 임시 폴더를 만들다 막힌다. 터미널에서 직접 실행하거나 샌드박스 밖에서 실행한다.
- 기본으로 플러그인 없이 돌린 결과(W/OUT)도 함께 나온다. 두 점수의 차이가 이 플러그인이 더한 몫이다. `skill-fired`와 `width-check` 채점기는 플러그인이 발동했는지 보는 표시라 점수에 넣지 않는다.
