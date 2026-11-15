#!/usr/bin/env python3
"""터미널 텍스트 도식에서 상자 테두리가 맞는지 검사한다 (visualize-idea 렌더·마감 단계용).

한글, 한자, 이모지는 터미널에서 2칸을 차지한다. 글자 수로 테두리를 맞추면 오른쪽 테두리가 어긋난다.
이 스크립트는 화면에 보이는 칸 수로 세어, ┌…┐로 시작한 상자의 양쪽 테두리가 아래 줄에서도 같은 칸에 있는지 본다.

사용: python3 textwidth.py [파일]   (파일이 없으면 표준 입력)
종료 코드: 0 이상 없음, 1 어긋난 곳 있음
"""
import argparse
import sys
import unicodedata

TOP_LEFT, TOP_RIGHT = "┌╭╔┏", "┐╮╗┓"
BOTTOM_LEFT, BOTTOM_RIGHT = "└╰╚┗", "┘╯╝┛"
LEFT_SIDE = "│║┃├╟┠"
RIGHT_SIDE = "│║┃┤╢┨"


def char_width(ch, ambiguous_wide):
    if unicodedata.combining(ch) or ch in "​‍️":
        return 0
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("W", "F"):
        return 2
    if eaw == "A" and ambiguous_wide:
        return 2
    return 1


def columns(line, ambiguous_wide):
    """줄의 각 글자가 시작하는 칸 번호 → 글자."""
    cells, col = {}, 0
    for ch in line.rstrip("\n"):
        cells[col] = ch
        col += char_width(ch, ambiguous_wide)
    return cells


def check(lines, ambiguous_wide=False):
    grid = [columns(l, ambiguous_wide) for l in lines]
    problems = []
    for r, cells in enumerate(grid):
        for c in sorted(cells):
            if cells[c] not in TOP_LEFT:
                continue
            right = next((x for x in sorted(cells) if x > c and cells[x] in TOP_RIGHT), None)
            if right is None:
                continue
            for r2 in range(r + 1, len(grid)):
                row = grid[r2]
                left_ch, right_ch = row.get(c, " "), row.get(right, " ")
                if left_ch in BOTTOM_LEFT:
                    if right_ch not in BOTTOM_RIGHT:
                        problems.append((r2, c, right, "아래 오른쪽 모서리", row))
                    break
                if left_ch not in LEFT_SIDE:
                    break  # 왼쪽 테두리가 끊기면 상자가 아니었던 것으로 본다
                if right_ch not in RIGHT_SIDE:
                    problems.append((r2, c, right, "오른쪽 테두리", row))
    return problems


def main():
    p = argparse.ArgumentParser(description="텍스트 도식의 상자 테두리 정렬 검사")
    p.add_argument("file", nargs="?")
    p.add_argument("--ambiguous-wide", action="store_true", help="모호한 폭 글자(상자 문자 등)를 2칸으로 센다")
    a = p.parse_args()
    text = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    lines = text.splitlines()
    problems = check(lines, a.ambiguous_wide)
    if not problems:
        print("상자 테두리 이상 없음")
        return
    for r2, c, right, what, row in problems:
        found = [x for x in sorted(row) if x > c and row[x] in RIGHT_SIDE + "".join(BOTTOM_RIGHT)]
        where = f"칸 {found[0]}에 있음" if found else "찾지 못함"
        print(f"{r2 + 1}번째 줄: 칸 {c}~{right} 상자의 {what}가 칸 {right}에 없다({where}) | {lines[r2]}")
    print("한글·한자·이모지는 2칸으로 세어 공백을 맞춘다.")
    sys.exit(1)


if __name__ == "__main__":
    main()
