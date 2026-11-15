# evals

`/friction-loop:improve`가 변경을 반영할 때마다 그 마찰을 재현하는 케이스를 여기에 하나씩 더한다. 케이스가 쌓이면, 나중에 확장을 고치다 같은 마찰이 되살아날 때 eval(실제 모델에 같은 상황을 시켜 보고 채점하는 시험)이 잡아낸다.

| 케이스 | 확인하는 것 |
|---|---|
| `improve-outside-repo` | 시스템 저장소가 아닌 폴더에서 `/friction-loop:improve`를 부르면 아무것도 수집하거나 바꾸지 않고, 저장소로 옮기라고 안내한다 |
| `improve-first-run` | 결정 기록(`docs/decisions.md`)이 아직 없는 포크 직후 저장소에서도 멈추지 않고 수집과 제안을 마치며, 승인 전에는 결정 기록을 만들지 않는다 |
| `improve-reads-signals` | `마찰:`로 기록하지 않은 마찰(반복 실패, 중단, 그 뒤의 바로잡는 말)도 대화 기록에서 찾아 제안 표에 넣고, 파일을 바꾸지 않은 채 승인을 기다린다 |

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

frontmatter는 파일 맨 위 `---` 두 줄 사이에 적는 설정이다. `graders/`의 파일 하나가 채점 기준 하나다.

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

- `--scaffold`: `case.yaml`의 `scaffold_script`를 실행해 작업 폴더를 준비한다. `improve-reads-signals`는 이 단계에서 시스템 저장소 모양의 폴더와 가짜 대화 기록을 만든다. 가짜 기록은 실행마다 새로 만드는 임시 홈 폴더 아래에만 생긴다.
- `--allow-tools "Bash(python3 *)"`: 검토 skill이 수집 스크립트를 돌릴 수 있게 한다. 이 권한이 없으면 Bash가 세션에서 빠져서 수집 단계를 확인할 수 없다.
- 샌드박스가 켜진 Claude Code 세션 안에서 실행하면 eval이 임시 폴더를 만들지 못해 멈춘다. 터미널에서 직접 실행한다.

새 케이스를 대화형으로 만들려면 `claude plugin eval init`, 빈 틀만 만들려면 `claude plugin eval init --bare <이름>`을 실행한다.

자세한 형식: https://code.claude.com/docs/en/plugin-evals
