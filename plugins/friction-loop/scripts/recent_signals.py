#!/usr/bin/env python3
"""최근 N일 대화 기록에서 사용자가 말로 하지 않은 마찰 신호를 뽑는다 (/friction-loop:improve 수집 단계용).

신호: 사용자가 직접 답한 권한 확인, 권한 거절(사용자·규칙·자동 모드·hook), 도구 오류, 사용자 중단.
신호마다 어떤 도구와 입력이었는지 붙이고, 신호 뒤에 사용자가 처음 한 말을 함께 보여 준다.
읽기만 한다. 서브에이전트 기록(하위 폴더)은 제외한다.
"""
import argparse
import collections
import datetime as dt
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # 설치된 플러그인 폴더에 __pycache__를 남기지 않는다
from recent_prompts import INTERRUPT, parse_ts, project_name, prompt_text, session_files

INPUT_KEYS = ("command", "file_path", "path", "url", "skill", "pattern", "description", "query")
SUBCOMMAND = re.compile(r"^[a-z][a-z0-9-]*$")
SCRIPT = re.compile(r"\.(?:py|sh|js|mjs|ts)$")
RESPONDING = ("응답 중", "응답")
# 사용자에게 묻는 것이 본래 일인 도구. 답한 것을 권한 확인으로 세지 않는다
ASKING_TOOLS = {"AskUserQuestion", "ExitPlanMode"}


def command_head(command):
    """'cd x && git -C y push origin'을 'git push'로 줄인다. 반복을 셀 때만 쓰는 대략적인 묶음 키다."""
    for seg in re.split(r"&&|\|\||[;|\n]", command):
        words = [w.strip("\"'") for w in seg.split()]
        while words and re.match(r"^\w+=", words[0]):
            words.pop(0)
        if not words or words[0] in ("cd", "export", "set"):
            continue
        first, rest, i = os.path.basename(words[0]), words[1:], 0
        while i < len(rest) and rest[i].startswith("-"):
            i += 2 if len(rest[i]) == 2 else 1  # '-C 경로' 같은 짧은 옵션은 값까지 건너뛴다
        if i < len(rest) and (SUBCOMMAND.match(rest[i]) or SCRIPT.search(rest[i])):
            return f"{first} {os.path.basename(rest[i])}"
        return first
    return ""


def describe(name, inp):
    """도구 호출을 (출력용 요약, 반복을 셀 묶음 키)로 바꾼다."""
    inp = inp if isinstance(inp, dict) else {}
    value = next((inp[k] for k in INPUT_KEYS if isinstance(inp.get(k), str) and inp[k]), "")
    if name == "Bash":
        key = f"Bash {command_head(value)}".strip()
    elif name == "Skill":
        key = f"Skill {value}"
    else:
        key = name
    return (f"{name}: {value}" if value else name), key


def result_text(block):
    content = block.get("content")
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return content if isinstance(content, str) else ""


def reject_kind(decision):
    if decision.get("reasonType") == "classifier":
        return "자동 모드 거절"
    if decision.get("source") == "hook":
        return "hook 차단"
    if decision.get("reasonType") == "rule":
        return "규칙 거절"
    if decision.get("source") == "user_reject":
        return "사용자 거절"
    return "설정 거절"


def result_kinds(rec, block):
    decision = rec.get("permissionDecision") or {}
    if decision.get("decision") == "reject":
        return [reject_kind(decision)]
    kinds = []
    if decision.get("decision") == "accept" and str(decision.get("source", "")).startswith("user"):
        kinds.append("직접 승인")
    if block.get("is_error"):
        kinds.append("중단" if INTERRUPT.match(result_text(block).strip()) else "도구 오류")
    return kinds


def detail(kind, text):
    """신호의 요점만 남긴다. 거절 안내문처럼 매번 같은 문장은 버린다."""
    if kind in ("직접 승인", "중단"):
        return ""
    if kind == "자동 모드 거절":
        m = re.search(r"Reason: (.*?)(?:\. If you have|$)", text, re.S)
        return m.group(1) if m else ""
    if kind == "사용자 거절":
        return text.partition("the user said:")[2]
    if kind == "hook 차단":
        return re.sub(r"^\S+ hook error:\s*", "", text)
    lines = [line for line in re.sub(r"</?tool_use_error>", "", text).splitlines() if line.strip()]
    if not lines:
        return ""
    # 명령 실패는 첫 줄이 'Exit code N'이고 원인은 대개 마지막 줄에 있다
    if re.match(r"(?:Error: )?Exit code \d+", lines[0]) and len(lines) > 1:
        return f"{lines[0]} · {lines[-1]}"
    return lines[0]


def scan(path, cutoff):
    """세션 하나의 신호. 신호가 이어진 뒤 사용자가 처음 한 말은 마지막 신호의 next에 붙는다."""
    session = os.path.splitext(os.path.basename(path))[0][:8]
    signals, pending, tool_uses, last_action = [], [], {}, RESPONDING
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("isSidechain") or rec.get("type") not in ("user", "assistant"):
                continue
            content = (rec.get("message") or {}).get("content")
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            blocks = [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []
            if rec["type"] == "assistant":
                for b in blocks:
                    if b.get("type") == "tool_use":
                        tool_uses[b.get("id")] = last_action = describe(b.get("name", "?"), b.get("input"))
                continue
            ts = parse_ts(rec.get("timestamp"))
            if ts is None or ts < cutoff:
                continue
            text = prompt_text(rec)
            if text is not None:
                if pending:
                    pending[-1]["next"] = text
                pending, last_action = [], RESPONDING
                continue
            found = []
            for b in blocks:
                if b.get("type") == "text" and INTERRUPT.match((b.get("text") or "").strip()):
                    found.append(("중단", last_action, ""))
                elif b.get("type") == "tool_result":
                    action = tool_uses.get(b.get("tool_use_id"), ("?", "?"))
                    found.extend((kind, action, detail(kind, result_text(b))) for kind in result_kinds(rec, b)
                                 if not (kind == "직접 승인" and action[1] in ASKING_TOOLS))
            for kind, (summary, key), info in found:
                sig = {"ts": ts, "project": project_name(rec, path), "session": session,
                       "kind": kind, "action": summary, "key": key, "detail": info, "next": None}
                signals.append(sig)
                pending.append(sig)
    return signals


def clip(text, limit):
    one = " ".join((text or "").split())
    return one if len(one) <= limit else one[: limit - 1] + "…"


def main():
    ap = argparse.ArgumentParser(description="최근 Claude 쪽 마찰 신호 모으기")
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--limit", type=int, default=300, help="세션별 목록에 보일 최근 신호 최대 개수")
    ap.add_argument("--top", type=int, default=20, help="반복 목록 최대 줄 수")
    ap.add_argument("--max-chars", type=int, default=120, help="칸당 최대 글자 수")
    ap.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"))
    a = ap.parse_args()

    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    signals = []
    for path in session_files(a.projects_dir, cutoff):
        try:
            signals.extend(scan(path, cutoff))
        except OSError:
            continue

    signals.sort(key=lambda s: s["ts"])
    dropped = max(0, len(signals) - a.limit)
    sessions = {(s["project"], s["session"]) for s in signals}
    projects = {s["project"] for s in signals}
    header = f"# 최근 {a.days:g}일 Claude 쪽 마찰 신호 {len(signals)}개 · 세션 {len(sessions)}개 · 프로젝트 {len(projects)}곳"
    print(header + (f" · 오래된 {dropped}개는 세션별 목록에서 생략" if dropped else ""))
    if not signals:
        return
    kinds = collections.Counter(s["kind"] for s in signals)
    print("종류별: " + " · ".join(f"{k} {n}" for k, n in kinds.most_common()))

    print("\n## 반복 (같은 종류·같은 도구나 명령이 2회 이상)")
    repeats = [(n, k, key) for (k, key), n in collections.Counter((s["kind"], s["key"]) for s in signals).most_common() if n >= 2]
    for n, k, key in repeats[: a.top]:
        print(f"{n}\t{k}\t{key}")
    if not repeats:
        print("없음")

    print("\n## 세션별 ('→'는 신호 뒤에 사용자가 처음 한 말)")
    groups = collections.defaultdict(list)
    for s in signals[dropped:]:
        groups[(s["project"], s["session"])].append(s)
    for (project, session), items in groups.items():
        print(f"### {project} · {session}")
        for s in items:
            cols = [f"{s['ts'].astimezone():%m-%d %H:%M}", s["kind"], clip(s["action"], a.max_chars)]
            if s["detail"]:
                cols.append(clip(s["detail"], a.max_chars))
            print("\t".join(cols))
            if s["next"]:
                print(f"\t→ {clip(s['next'], a.max_chars)}")


if __name__ == "__main__":
    main()
