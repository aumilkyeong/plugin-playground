# writing-for-human: 사람이 읽을 글 쓰기

Claude가 사람에게 내보내는 글(문서, README, PR 설명, 커밋 메시지)을 독자가 한 번 읽고 움직일 수 있게 쓰도록 하는 플러그인이다. 설치해 두면 그런 글을 쓸 때 skill이 저절로 발동하므로 따로 부를 일이 없다. 평소 채팅 답변에는 발동하지 않는다.

```bash
claude plugin install writing-for-human@aumilkyeong
```

이런 글에서 Claude가 가장 자주 실패하는 이유는 지식의 저주(curse of knowledge)다. 대화에서 정한 이름과 결정을 독자도 안다고 여기고 쓴다. 그래서 무거운 글은 대화 맥락이 없는 독자(`cold-reader` agent)에게 먼저 읽힌다. 그 독자가 요점을 자기 말로 다시 말하고 막힌 곳을 짚으면, 그것을 보고 고친다.

## 쓰는 순서

```mermaid
flowchart LR
  A[무게 정하기] --> B[설계 메모<br>독자 · 목적 · 핵심 메시지]
  B --> C[초고<br>요점 먼저]
  C --> D[구조 고쳐 쓰기<br>역개요]
  D --> E[문장 훑어 읽기<br>개인 기준 → 항목별 → 한국어]
  E --> F[독자 테스트<br>cold-reader]
  F --> G[내보내기 전 확인]
```

글이 가벼우면 단계를 건너뛴다.

| 무게 | 예 | 거치는 단계 |
|---|---|---|
| 가벼움 | 커밋 메시지, 짧은 메시지 | 설계 메모(속으로), 개인 기준, 확인 |
| 보통 | PR 설명, 이슈, 문서의 한 절 | 독자 테스트를 뺀 전부 |
| 무거움 | 새 문서, README, 보고서, 제안서 | 전부 |

## 구성

| 파일 | 역할 |
|---|---|
| `skills/write/SKILL.md` | 쓰는 절차. 사람이 읽을 글을 파일이나 대화 밖으로 내보낼 때 발동한다 |
| `skills/write/references/standards.md` | 개인 기준. 이 저장소 주인에게 지적받은 실패와 해법 |
| `skills/write/references/passes.md` | 문장 훑어 읽기 항목 7묶음(맥락, 요점, 덜어 내기, 행위자, 정확, 목소리, 서식) |
| `skills/write/references/korean.md` | 한국어 문체, 자주 틀리는 표기, 번역투, 쉬운 말 |
| `agents/cold-reader.md` | 독자 테스트. 대화 맥락 없이 초안만 읽고, 쓸 수 있는 도구는 Read뿐이다 |
| `evals/` | README 작성, 커밋 메시지, 채팅 답변에서 발동하지 않음을 확인하는 케이스 |

## 개인 기준은 friction-loop가 키운다

`standards.md`의 항목은 대화 기록에서 같은 지시가 되풀이된 것을 근거로 했다. 예를 들어 "요점과 할 일을 맨 앞에 둔다"는 2주 동안 5번 나온 지시다. 앞으로 글을 고치라고 한 말이 마찰로 쌓이면 [`/friction-loop:improve`](../friction-loop/README.md)가 이 목록에 항목을 더하거나, 지켜져서 더는 지적이 없는 항목을 지우자고 제안한다.

이 저장소를 포크해서 쓴다면 `standards.md`의 항목을 지우고 자기 기준으로 채운다.

## 근거

절차와 점검 항목은 작문가 역량지도(10개 영역, 40개 역량)를 바탕으로 했다. 파일 곳곳의 괄호 번호(예: 4.1)가 그 역량 번호다. 역량지도는 개인 조사 문서라 저장소에 넣지 않았다.

## 개발

설치하지 않고 이 세션에만 불러온다. 저장소 루트에서 실행한다.

```bash
claude --plugin-dir ./plugins/writing-for-human
```

eval 실행 방법은 [`evals/README.md`](evals/README.md)에 있다.
