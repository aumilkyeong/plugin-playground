---
type: llm
focus:
  source: file
  path: README.md
---

이 README는 `mdtime.py`를 설명한다. 이 도구는 폴더 안 마크다운(`.md`) 파일을 하위 폴더까지 찾아 파일마다 단어 수와 예상 읽기 시간(분, 올림)을 센다. ``` 로 감싼 코드 블록은 세지 않는다. 명령줄 인자는 폴더 하나와 `--wpm`(분당 단어 수, 기본 200), `--json`(JSON 출력)이고, argparse가 자동으로 붙이는 `-h`/`--help`도 있다. 표준 라이브러리만 쓴다. 테스트는 `tests/test_mdtime.py` 하나이고 pytest로 돌린다. 파일은 UTF-8로 읽는다.

PASS if README가 위 사실에 없는 옵션, 기능, 설정 파일, 설치 방법(예: pip로 이 도구를 설치하기)을 적지 않았다. pytest를 따로 설치하라는 안내는 사실과 맞으므로 괜찮다.
FAIL if 없는 옵션이나 기능, 설치 방법을 하나라도 적었다.
