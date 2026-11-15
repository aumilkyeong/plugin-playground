#!/usr/bin/env bash
# README가 없는 작은 CLI 저장소를 만든다. 옵션은 --wpm과 --json 두 개뿐이다.
set -euo pipefail

cat > mdtime.py <<'PY'
"""마크다운 문서의 단어 수와 예상 읽기 시간을 센다."""
import argparse
import json
import math
import pathlib
import re

CODE_BLOCK = re.compile(r"```.*?```", re.S)


def count_words(text):
    return len(CODE_BLOCK.sub("", text).split())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="마크다운 파일을 찾을 폴더")
    parser.add_argument("--wpm", type=int, default=200, help="분당 읽는 단어 수")
    parser.add_argument("--json", action="store_true", help="JSON으로 출력")
    args = parser.parse_args()

    rows = []
    for path in sorted(pathlib.Path(args.folder).rglob("*.md")):
        words = count_words(path.read_text(encoding="utf-8"))
        rows.append({"file": str(path), "words": words, "minutes": math.ceil(words / args.wpm)})

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print(f"{row['minutes']:>3}분  {row['words']:>6}단어  {row['file']}")


if __name__ == "__main__":
    main()
PY

mkdir -p tests
cat > tests/test_mdtime.py <<'PY'
from mdtime import count_words


def test_code_blocks_are_not_counted():
    assert count_words("하나 둘\n```\nskip me\n```\n셋") == 3
PY
