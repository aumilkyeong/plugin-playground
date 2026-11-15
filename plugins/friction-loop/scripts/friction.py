#!/usr/bin/env python3
"""마찰 기록 도구.

  hook                       UserPromptSubmit hook. '마찰:'로 시작하는 프롬프트를 기록하고 막는다.
  add TEXT                   한 줄 직접 기록한다.
  list [--open] [--decisions FILE] [--days N] [--json]
  stats [--decisions FILE]

데이터 폴더: --data DIR, 없으면 CLAUDE_PLUGIN_DATA 환경 변수.
마찰 ID가 결정 기록 파일(docs/decisions.md)에 적히면 처리된 것으로 본다.
"""
import argparse
import datetime as dt
import fcntl
import json
import os
import re
import sys

PREFIX = re.compile(r"^\s*(?:마찰|friction)\s*[:：]\s*", re.IGNORECASE)
ID_RE = re.compile(r"\bF-\d{3,}\b")
LOG_NAME = "friction.jsonl"


def data_dir(arg, create=False):
    d = arg or os.environ.get("CLAUDE_PLUGIN_DATA")
    if not d:
        raise RuntimeError("데이터 폴더를 모릅니다. --data를 주거나 CLAUDE_PLUGIN_DATA를 설정하세요")
    if create:
        os.makedirs(d, exist_ok=True)
    return d


def read_entries(d):
    path = os.path.join(d, LOG_NAME)
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def append_entry(d, text, cwd="", session_id="", source="manual"):
    path = os.path.join(d, LOG_NAME)
    with open(path, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        count = sum(1 for line in f if line.strip())
        entry = {
            "id": f"F-{count + 1:03d}",
            "ts": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "text": text,
            "project": os.path.basename(cwd.rstrip("/")) if cwd else "",
            "cwd": cwd,
            "session_id": session_id,
            "source": source,
        }
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry, count + 1


def resolved_ids(decisions):
    if not decisions:
        return set()
    if not os.path.exists(decisions):
        raise RuntimeError(f"결정 기록 파일이 없습니다: {decisions}")
    with open(decisions, encoding="utf-8") as f:
        return set(ID_RE.findall(f.read()))


def parse_ts(value):
    try:
        return dt.datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def short(text, limit=80):
    return text if len(text) <= limit else text[: limit - 1] + "…"


def block(reason):
    print(json.dumps({
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "suppressOriginalPrompt": True},
    }, ensure_ascii=False))
    return 0


def cmd_hook(args):
    # 이 hook은 모든 프롬프트(/loop, 백그라운드 agent 보고 포함)에 불린다.
    # 접두어가 없으면 아무것도 출력하지 않는다. 출력하면 Claude의 컨텍스트에 들어간다.
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = payload.get("prompt") or ""
    m = PREFIX.match(prompt)
    if not m:
        return 0
    text = " ".join(prompt[m.end():].split())
    if not text:
        return block("마찰 내용을 함께 적어 주세요. 예: 마찰: 커밋 메시지 형식을 또 설명했다")
    try:
        d = data_dir(args.data, create=True)
        entry, total = append_entry(d, text, payload.get("cwd") or "", payload.get("session_id") or "", "prompt")
    except Exception as e:
        return block(f"마찰을 기록하지 못했습니다 ({e}). 입력한 내용: {text}")
    return block(f"마찰 {entry['id']} 기록 · 누적 {total}건 · 검토는 /friction-loop:improve\n\"{short(text)}\"")


def cmd_add(args):
    text = " ".join(" ".join(args.text).split())
    if not text:
        print("기록할 내용이 비어 있습니다", file=sys.stderr)
        return 1
    entry, total = append_entry(data_dir(args.data, create=True), text, os.getcwd(), "", "manual")
    print(f"{entry['id']} 기록 · 누적 {total}건")
    return 0


def filtered(args):
    entries = read_entries(data_dir(args.data))
    if getattr(args, "open", False):
        done = resolved_ids(args.decisions)
        entries = [e for e in entries if e.get("id") not in done]
    if getattr(args, "days", None):
        cutoff = dt.datetime.now().astimezone() - dt.timedelta(days=args.days)
        entries = [e for e in entries if (parse_ts(e.get("ts")) or cutoff) >= cutoff]
    return entries


def cmd_list(args):
    if args.open and not args.decisions:
        print("--open에는 --decisions가 필요합니다", file=sys.stderr)
        return 1
    entries = filtered(args)
    for e in entries:
        if args.json:
            print(json.dumps(e, ensure_ascii=False))
        else:
            when = (e.get("ts") or "")[:16].replace("T", " ")
            print(f"{e.get('id')}\t{when}\t{e.get('project') or '-'}\t{e.get('text')}")
    if not args.json:
        label = "열린 마찰" if args.open else "마찰"
        print(f"# {label} {len(entries)}건")
    return 0


def cmd_stats(args):
    entries = read_entries(data_dir(args.data))
    cutoff = dt.datetime.now().astimezone() - dt.timedelta(days=7)
    recent = [e for e in entries if (parse_ts(e.get("ts")) or cutoff) > cutoff]
    parts = [f"전체 {len(entries)}건", f"최근 7일 {len(recent)}건"]
    if args.decisions:
        done = resolved_ids(args.decisions)
        parts.append(f"열림 {sum(1 for e in entries if e.get('id') not in done)}건")
    print(" · ".join(parts))
    return 0


def main():
    ap = argparse.ArgumentParser(description="마찰 기록 도구")
    ap.add_argument("--data", help="데이터 폴더 (기본: CLAUDE_PLUGIN_DATA)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("hook", help="UserPromptSubmit hook으로 실행")
    p_add = sub.add_parser("add", help="한 줄 기록")
    p_add.add_argument("text", nargs="+")
    p_list = sub.add_parser("list", help="기록 보기")
    p_list.add_argument("--open", action="store_true", help="결정 기록에 ID가 없는 것만")
    p_list.add_argument("--decisions", help="결정 기록 파일 경로")
    p_list.add_argument("--days", type=float, help="최근 N일만")
    p_list.add_argument("--json", action="store_true")
    p_stats = sub.add_parser("stats", help="건수 요약")
    p_stats.add_argument("--decisions", help="결정 기록 파일 경로")
    args = ap.parse_args()
    handlers = {"hook": cmd_hook, "add": cmd_add, "list": cmd_list, "stats": cmd_stats}
    try:
        return handlers[args.cmd](args)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
