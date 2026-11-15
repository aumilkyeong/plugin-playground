# evals

`/friction-loop:improve`가 변경을 반영할 때마다 그 마찰을 재현하는 케이스를 여기에 하나씩 더한다. 케이스가 쌓일수록 같은 마찰이 다시 생기는 것을 막아 준다.

## 케이스 형식

```
evals/<케이스 이름>/
├── prompt.md          # frontmatter(name, description, tags, max_turns, allowed_tools) + 사용자 프롬프트
└── graders/
    ├── criteria.md    # type: llm. 본문이 판정 기준
    └── <이름>.md      # type: regex | tool_used | tool_order | file_exists
```

- 케이스 이름에는 원인이 된 마찰을 짐작할 수 있는 말을 쓴다. 마찰 ID는 `docs/decisions.md`에 적는다.
- 결정적으로 확인할 수 있는 것은 `regex`, `tool_used`, `file_exists`로 채점하고, 나머지만 `llm`에 맡긴다.
- 직접 부르는 skill은 프롬프트에 `/플러그인:이름`을 그대로 쓰면 펼쳐진다.
- 다른 플러그인 케이스는 그 플러그인의 `evals/`에 둔다.

## 실행

플러그인 폴더에서 실행한다. 실제 모델을 부르므로 비용이 든다.

```bash
cd plugins/friction-loop
claude plugin eval . --max-cost-usd 2
```

새 케이스를 대화형으로 만들려면 `claude plugin eval init`, 빈 틀만 만들려면 `claude plugin eval init --bare <이름>`.

자세한 형식: https://code.claude.com/docs/en/plugin-evals
