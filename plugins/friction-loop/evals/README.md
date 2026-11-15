# evals

`/friction-loop:improve`가 변경을 반영할 때마다 그 마찰을 재현하는 케이스를 여기에 하나씩 더한다. 케이스가 쌓일수록 같은 마찰이 다시 생기는 것을 막아 준다.

## 케이스 형식

```
evals/<케이스 이름>/
├── prompt.md          # frontmatter(name, description, tags, max_turns, allowed_tools) + 사용자 프롬프트
├── case.yaml          # (선택) context.scaffold_script처럼 prompt.md에 쓸 수 없는 설정
├── fixture.sh         # (선택) scaffold_script. 빈 작업 폴더에서 시작해 필요한 파일을 만든다
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
claude plugin eval . --scaffold --allow-tools "Bash(python3 *)" --max-cost-usd 2
```

- `--scaffold`: `case.yaml`의 `scaffold_script`를 실행해 작업 폴더를 준비한다. `improve-reads-signals`는 이 단계에서 시스템 저장소 모양의 폴더와 가짜 대화 기록을 만든다. 가짜 기록은 실행마다 새로 만드는 임시 홈 아래에만 생긴다.
- `--allow-tools "Bash(python3 *)"`: 검토 skill이 수집 스크립트를 돌릴 수 있게 한다. 이 권한이 없으면 Bash가 세션에서 빠져서 수집 단계를 확인할 수 없다.

새 케이스를 대화형으로 만들려면 `claude plugin eval init`, 빈 틀만 만들려면 `claude plugin eval init --bare <이름>`.

자세한 형식: https://code.claude.com/docs/en/plugin-evals
