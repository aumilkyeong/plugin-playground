# evals

케이스 형식은 [`plugins/friction-loop/evals/README.md`](../../friction-loop/evals/README.md)를 따른다. 기준을 바꿀 때마다 그 실패를 재현하는 케이스를 여기에 더한다.

| 케이스 | 확인하는 것 |
|---|---|
| `readme-for-newcomer` | README를 새로 쓰면 skill이 발동하고 cold-reader로 시험한다. 채점은 기준마다 따로 한다: 요점과 실행 명령이 첫 소제목 앞에 있다, 없는 기능을 지어내지 않는다, 지어낸 실행 결과는 예시라고 밝힌다, 독자를 정하지 않았으니 초보자가 모를 JSON과 pytest를 풀이한다, 글에 대한 글과 번역투가 없다. 긴 글은 LLM 판정이 흔들리므로 용어 풀이는 regex로 본다 |
| `commit-message-korean` | diff를 주고 커밋 메시지를 부탁하면 skill이 발동하고, 무엇을 고쳤는지 드러나는 한국어 제목 줄을 쓴다 |
| `chat-answer-no-trigger` | 평소 채팅 질문에는 발동하지 않는다 |

## 실행

플러그인 폴더에서 실행한다. 실제 모델을 부르므로 비용이 든다.

```bash
cd plugins/writing-for-human
claude plugin eval . --scaffold --allow-tools Write Edit --no-publish --max-cost-usd 5
```

- `--scaffold`: README 케이스의 `fixture.sh`로 README가 없는 작은 저장소를 만든다.
- `--allow-tools`: README 케이스는 파일을 써야 한다.
- 커밋 케이스는 git을 실행하지 않고 diff를 프롬프트로 준다. eval 샌드박스가 macOS 임시 폴더 쓰기를 막아 Xcode의 git이 실행되지 않기 때문이다.
- Claude Code 세션 안에서 실행하면 eval이 `/tmp`에 임시 폴더를 만들다 샌드박스에 막힌다. 터미널에서 직접 실행하거나 샌드박스 밖에서 실행한다.
- 기본으로 플러그인 없이 돌린 결과(W/OUT)도 함께 나온다. 두 점수의 차이가 이 플러그인이 더한 몫이다. `skill-fired`, `cold-reader` 채점기는 플러그인이 발동했는지 보는 표시라 점수에 넣지 않는다.
