# 형태 선택 기준

`/friction-loop:improve`가 개선안을 담을 형태를 고를 때 따른다. 위치는 자가개선 시스템 저장소 루트를 기준으로 한다.

| 요구 | 형태 | 위치 |
|---|---|---|
| 모든 세션에서 항상 알아야 할 맥락 | CLAUDE.md | `~/.claude/CLAUDE.md`, 프로젝트 `CLAUDE.md` |
| 특정 경로의 파일을 다룰 때만 필요한 규칙 | rule (`paths` frontmatter) | `.claude/rules/` |
| 필요할 때만 꺼내 쓰는 절차와 판단 기준 | skill | `plugins/<플러그인>/skills/<이름>/SKILL.md` |
| 부작용이 있어 내가 직접 부를 때만 돌아야 하는 작업 | skill + `disable-model-invocation: true` | 위와 같음 |
| 맥락이나 권한을 떼어 놓아야 하는 역할 | agent | `plugins/<플러그인>/agents/<이름>.md` |
| 반드시 일어나야 하거나 반드시 막아야 하는 일 | hook | `plugins/<플러그인>/hooks/hooks.json` |
| 외부 시스템과 데이터 | MCP 서버 | `plugins/<플러그인>/.mcp.json` |
| 반복되는 결정적 처리(검사, 변환, 집계) | 스크립트 | `plugins/<플러그인>/scripts/` |
| 여러 단계를 정해진 순서로 | workflow | `plugins/<플러그인>/workflows/<이름>.js` |

판단이 갈리면 약한 형태로 시작하고, 지켜지지 않을 때 승격한다(CLAUDE.md → rule·skill → hook). 무언가를 더할 때는 지울 조건도 같이 적는다.
