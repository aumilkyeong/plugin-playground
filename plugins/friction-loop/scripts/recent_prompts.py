#!/usr/bin/env python3
"""최근 N일 동안 직접 입력한 프롬프트를 대화 기록에서 뽑는다 (/friction-loop:improve 수집 단계용).

대화 기록: ~/.claude/projects/<프로젝트>/<세션>.jsonl (cleanupPeriodDays가 지나면 지워진다)
읽기만 한다. 서브에이전트 기록(하위 폴더), '마찰:' 프롬프트, 중단 표시, 압축 요약은 제외한다.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re

FRICTION = re.compile(r"^\s*(?:마찰|friction)\s*[:：]", re.IGNORECASE)
# 중단 표시는 사용자가 입력한 말이 아니다. recent_signals.py가 따로 센다
INTERRUPT = re.compile(r"^\[Request interrupted by user")
HUMAN_SOURCES = {"typed", "suggestion_accepted"}


def session_files(projects_dir, cutoff):
    """cutoff 이후에 바뀐 세션 기록. 서브에이전트 기록은 하위 폴더에 있어 빠진다."""
    for path in glob.glob(os.path.join(projects_dir, "*", "*.jsonl")):
        try:
            if dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc) >= cutoff:
                yield path
        except OSError:
            continue


def project_name(rec, path):
    return os.path.basename((rec.get("cwd") or "").rstrip("/")) or os.path.basename(os.path.dirname(path))


def prompt_text(rec):
    if rec.get("type") != "user" or rec.get("isMeta") or rec.get("isCompactSummary") or rec.get("isSidechain"):
        return None
    source = rec.get("promptSource")
    if source is not None and source not in HUMAN_SOURCES:
        return None
    content = (rec.get("message") or {}).get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        text = "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    else:
        return None
    text = text.strip()
    # '<'로 시작하는 것은 슬래시 명령, 알림, 시스템 메시지다
    if not text or text.startswith("<") or FRICTION.match(text) or INTERRUPT.match(text):
        return None
    return text


def parse_ts(value):
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser(description="최근 직접 입력한 프롬프트 모으기")
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--limit", type=int, default=300, help="최근 것부터 최대 개수")
    ap.add_argument("--max-chars", type=int, default=200, help="프롬프트당 최대 글자 수")
    ap.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"))
    a = ap.parse_args()

    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    rows = []
    for path in session_files(a.projects_dir, cutoff):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    if '"user"' not in line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    text = prompt_text(rec)
                    ts = parse_ts(rec.get("timestamp"))
                    if text is None or ts is None or ts < cutoff:
                        continue
                    rows.append((ts, project_name(rec, path), text))
        except OSError:
            continue

    rows.sort(key=lambda r: r[0])
    dropped = max(0, len(rows) - a.limit)
    rows = rows[dropped:]
    projects = {p for _, p, _ in rows}
    header = f"# 최근 {a.days:g}일 직접 입력한 프롬프트 {len(rows)}개 · 프로젝트 {len(projects)}곳"
    print(header + (f" · 오래된 {dropped}개 생략" if dropped else ""))
    for ts, project, text in rows:
        one = " ".join(text.split())
        if len(one) > a.max_chars:
            one = one[: a.max_chars - 1] + "…"
        print(f"{ts.astimezone():%m-%d %H:%M}\t{project}\t{one}")


if __name__ == "__main__":
    main()
