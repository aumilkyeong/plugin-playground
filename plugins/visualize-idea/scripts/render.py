#!/usr/bin/env python3
"""도식 파일을 Chrome 계열 브라우저로 화면 없이 그려 PNG로 저장한다 (visualize-idea 렌더·마감 단계용).

입력: .svg, .html, .mmd(Mermaid 코드), .md(첫 번째 ```mermaid 블록)
출력: 만든 PNG의 절대 경로를 한 줄씩 출력한다. 기본 위치는 임시 폴더다.

브라우저는 샌드박스 안에서 뜨지 않는다. 샌드박스가 켜진 세션에서는 샌드박스 밖에서 실행한다.
Mermaid는 cdn.jsdelivr.net에서 불러오므로 네트워크가 필요하다.
"""
import argparse
import glob
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"
MAC_APPS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]
LINUX_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"]
PALETTE = {False: ("#ffffff", "#161a23"), True: ("#0f1218", "#e4e7ee")}
EXIT_NO_BROWSER, EXIT_BROWSER_FAILED, EXIT_MERMAID_ERROR = 3, 4, 5


def find_browser():
    env = os.environ.get("VISUALIZE_BROWSER")
    if env:
        return env
    for path in MAC_APPS:
        if os.path.exists(path):
            return path
    for name in LINUX_NAMES:
        found = shutil.which(name)
        if found:
            return found
    # Playwright가 내려받아 둔 Chromium
    cache = os.path.expanduser("~/Library/Caches/ms-playwright") if sys.platform == "darwin" else os.path.expanduser("~/.cache/ms-playwright")
    for pattern in ("chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium", "chromium-*/chrome-linux/chrome"):
        hits = sorted(glob.glob(os.path.join(cache, pattern)))
        if hits:
            return hits[-1]
    return None


def svg_size(svg):
    """루트 <svg>의 width·height, 없으면 viewBox에서 크기를 읽는다."""
    root = re.search(r"<svg\b[^>]*>", svg, re.S)
    attrs = root.group(0) if root else ""

    def num(name):
        m = re.search(rf'\b{name}\s*=\s*"([\d.]+)(px)?"', attrs)
        return float(m.group(1)) if m else None

    w, h = num("width"), num("height")
    vb = re.search(r'viewBox\s*=\s*"\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', attrs)
    if (w is None or h is None) and vb:
        vw, vh = float(vb.group(1)), float(vb.group(2))
        w = w or (h * vw / vh if h else vw)
        h = h or w * vh / vw
    return int(w or 800), int(h or 600)


# 모든 CSS 애니메이션을 끝 장면으로 보내고, SMIL 애니메이션은 시계를 끝으로 돌린다
END_STATE = ('<style>*,*::before,*::after{animation-delay:-3600s!important;'
             'animation-iteration-count:1!important;transition:none!important}</style>'
             '<script>addEventListener("load",()=>document.querySelectorAll("svg").forEach('
             's=>{if(s.setCurrentTime){s.pauseAnimations();s.setCurrentTime(3600)}}))</script>')


def page(body, dark, extra_head="", svg_box=None):
    bg, fg = PALETTE[dark]
    size = f".pad>svg{{display:block;width:{svg_box[0]}px;height:{svg_box[1]}px}}" if svg_box else ""
    return (f'<!doctype html><html><head><meta charset="utf-8">{extra_head}'
            f'<style>html,body{{margin:0;background:{bg};color:{fg};'
            f'font-family:"Apple SD Gothic Neo","Noto Sans KR",sans-serif}}'
            f'.pad{{padding:24px;display:inline-block}}{size}</style></head>'
            f'<body><div class="pad">{body}</div></body></html>')


def mermaid_source(path, text):
    if path.endswith(".md"):
        m = re.search(r"```mermaid\s*\n(.*?)```", text, re.S)
        if not m:
            sys.exit(f"{path}: ```mermaid 블록이 없다")
        return m.group(1)
    return text


def build(path, dark, end):
    """입력 파일을 브라우저에 줄 HTML 문서로 바꾼다. (문서, 창 크기, mermaid 여부)"""
    text = open(path, encoding="utf-8").read()
    ext = os.path.splitext(path)[1].lower()
    if ext == ".svg":
        svg = re.sub(r"<\?xml[^>]*\?>", "", text)
        w, h = svg_size(svg)
        return page(svg, dark, END_STATE if end else "", (w, h)), (w + 48, h + 48), False
    if ext in (".mmd", ".md"):
        src = mermaid_source(path, text)
        theme = "dark" if dark else "default"
        head = (f'<script src="{MERMAID_URL}"></script>'
                f'<script>mermaid.initialize({{startOnLoad:true,theme:"{theme}",securityLevel:"loose"}});</script>')
        return page(f'<pre class="mermaid">{html.escape(src)}</pre>', dark, head), None, True
    if ext in (".html", ".htm"):
        return None, None, False  # 원본 HTML은 상대 경로 자원을 위해 그 자리에서 연다
    sys.exit(f"{path}: 지원하지 않는 형식이다 (.svg, .html, .mmd, .md)")


def run(browser, args, timeout):
    try:
        return subprocess.run([browser] + args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None


def main():
    p = argparse.ArgumentParser(description="도식 파일을 PNG로 그린다")
    p.add_argument("input")
    p.add_argument("--out", help="PNG 경로 (기본: 임시 폴더)")
    p.add_argument("--dark", action="store_true", help="어두운 배경과 prefers-color-scheme: dark로 그린다")
    p.add_argument("--reduced-motion", action="store_true", help="prefers-reduced-motion: reduce로 그린다 (움직이는 SVG의 정지 장면)")
    p.add_argument("--end", action="store_true", help="SVG 애니메이션을 끝 장면으로 보내고 그린다")
    p.add_argument("--wait", type=int, default=0, help="찍기 전에 흘려보낼 시간(ms). 스크립트가 그리는 HTML")
    p.add_argument("--size", help="창 크기 WxH (기본: SVG는 그림 크기, 나머지는 1280x900)")
    p.add_argument("--scale", type=float, default=2, help="픽셀 배율 (기본 2)")
    a = p.parse_args()

    src = os.path.abspath(a.input)
    if not os.path.exists(src):
        sys.exit(f"{src}: 파일이 없다")
    browser = find_browser()
    if not browser:
        print("Chrome 계열 브라우저를 찾지 못했다. VISUALIZE_BROWSER에 실행 파일 경로를 지정한다.", file=sys.stderr)
        sys.exit(EXIT_NO_BROWSER)

    doc, size, is_mermaid = build(src, a.dark, a.end)
    if a.size:
        w, h = (int(x) for x in a.size.lower().split("x"))
        size = (w, h)
    size = size or (1280, 900)
    wait = a.wait or (4000 if is_mermaid else 0)

    work = tempfile.mkdtemp(prefix="visualize-idea-")
    try:
        page_path = src
        if doc is not None:
            page_path = os.path.join(work, "page.html")
            with open(page_path, "w", encoding="utf-8") as f:
                f.write(doc)
        url = "file://" + page_path

        stem = os.path.splitext(os.path.basename(src))[0]
        suffix = "-dark" if a.dark else ""
        suffix += "-static" if a.reduced_motion else ""
        out = os.path.abspath(a.out) if a.out else os.path.join(tempfile.gettempdir(), "visualize-idea", f"{stem}{suffix}.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)

        common = ["--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                  "--hide-scrollbars", f"--user-data-dir={os.path.join(work, 'profile')}",
                  f"--force-device-scale-factor={a.scale}", f"--window-size={size[0]},{size[1]}"]
        # 지정하지 않으면 운영체제의 다크 모드를 따라가므로 밝은 쪽도 못 박는다 (0: 어두움, 1: 밝음)
        common.append(f"--blink-settings=preferredColorScheme={0 if a.dark else 1}")
        if a.dark:
            common.append("--force-dark-mode")
        if a.reduced_motion:
            common.append("--force-prefers-reduced-motion")
        if wait:
            common.append(f"--virtual-time-budget={wait}")

        if is_mermaid:
            dom = run(browser, common + ["--dump-dom", url], 90)
            if dom is None or dom.returncode != 0:
                print("브라우저가 실행되지 않았다. 샌드박스 안이면 밖에서 다시 실행한다.", file=sys.stderr)
                sys.exit(EXIT_BROWSER_FAILED)
            if re.search(r"Syntax error|Parse error", dom.stdout):
                msg = re.search(r"(Parse error[^<]*|Syntax error[^<]*)", dom.stdout)
                print(f"Mermaid 문법 오류: {html.unescape(msg.group(1)) if msg else '알 수 없음'}", file=sys.stderr)
                sys.exit(EXIT_MERMAID_ERROR)
            drawn = re.search(r'<svg[^>]*viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', dom.stdout)
            if not drawn:
                print("Mermaid가 그려지지 않았다. 네트워크(cdn.jsdelivr.net)를 확인한다.", file=sys.stderr)
                sys.exit(EXIT_BROWSER_FAILED)
            if not a.size:  # 그려진 그림 크기에 창을 맞춘다
                size = (int(float(drawn.group(1))) + 64, int(float(drawn.group(2))) + 64)
                common = [c for c in common if not c.startswith("--window-size=")] + [f"--window-size={size[0]},{size[1]}"]

        shot = run(browser, common + [f"--screenshot={out}", url], 90)
        if shot is None or shot.returncode != 0 or not os.path.exists(out):
            tail = (shot.stderr.strip().splitlines()[-1:] if shot else ["시간 초과"])
            print(f"브라우저가 PNG를 만들지 못했다: {tail[0] if tail else ''}", file=sys.stderr)
            print("샌드박스 안이면 밖에서 다시 실행한다.", file=sys.stderr)
            sys.exit(EXIT_BROWSER_FAILED)
        print(out)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
