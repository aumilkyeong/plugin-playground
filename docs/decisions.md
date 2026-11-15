# 자가개선 시스템 결정 기록

`/friction-loop:improve`가 읽고 쓰는 파일이다. 마찰 ID(`F-` 뒤에 번호)가 이 파일에 적히면 처리된 것으로 본다. 그러니 설명 문장에 실제 ID 모양의 예시를 쓰지 않는다.

## 형태 선택 기준

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

## 주간 지표

북극성 지표는 '반복 지시'(같은 지시를 여러 세션에서 되풀이한 묶음 수)다. 줄어들수록 좋다.

| 주(시작일) | 마찰 기록 | 반복 지시 | 반영 | 지움 | 메모 |
|---|---|---|---|---|---|
| 2026-11-15 | 0 | – | – | – | 기준선, friction-loop 0.1.0 |

## 변경 기록

형식: `- 날짜 · 처리(만들기/고치기/승격/지우기/보류/기각) · 대상과 버전 · 마찰 ID · 한 줄 설명`

- 2026-11-15 · 만들기 · friction-loop 0.1.0 · – · 마찰 포착 hook, `/friction-loop:improve` 검토 skill, 기록·수집 스크립트
