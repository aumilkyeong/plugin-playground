---
type: llm
focus:
  source: file
  path: README.md
---

이 README는 `mdtime.py`를 설명한다. 이 도구는 폴더 안 마크다운(`.md`) 파일을 하위 폴더까지 찾아 파일마다 단어 수와 예상 읽기 시간(분, 올림)을 센다. ``` 로 감싼 코드 블록은 세지 않는다. 명령줄 인자는 폴더 하나와 `--wpm`(분당 단어 수, 기본 200), `--json`(JSON 출력)이고, argparse가 자동으로 붙이는 `-h`/`--help`도 있다. 표준 라이브러리만 쓴다. 테스트는 `tests/test_mdtime.py` 하나이고 pytest로 돌린다. 파일은 UTF-8로 읽는다.

PASS if 제목 바로 아래, 첫 번째 소제목(`##`)이 나오기 전 부분만 읽어도 이 도구가 무엇을 하는지와 실제로 실행할 명령(`python mdtime.py <폴더>` 꼴)을 둘 다 알 수 있다.
FAIL if 둘 중 하나라도 첫 번째 소제목 뒤에야 나온다.
