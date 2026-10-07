#!/usr/bin/env python3
"""guide.md → guide.pdf (에디토리얼 인쇄판).

사용법:
    <venv>/bin/python tools/build_guide_pdf.py      (macOS·Linux)
    py tools\\build_guide_pdf.py                      (Windows)

- markdown 패키지로 본문 변환, 검사 도구와 같은 디자인 토큰의 인쇄 CSS로 감싼 뒤
  Chrome 헤드리스 --print-to-pdf로 A4 PDF 생성, reportlab+pypdf로 쪽번호 스탬프.
- 필요 패키지: markdown, pypdf, reportlab. Chrome 설치 필요(경로가 다르면 CHROME 환경변수로 지정).
"""
import os, re, shutil, subprocess, sys, tempfile
from io import BytesIO
from pathlib import Path

import markdown
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "guide.md"
OUT = ROOT / "guide.pdf"


def find_chrome():
    """CHROME 환경변수 → OS별 기본 설치 경로 → PATH 순으로 Chrome을 찾는다."""
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for c in candidates:
        if Path(c).is_file():
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("Chrome을 찾지 못했습니다. CHROME 환경변수에 실행 파일 경로를 지정하세요.")


CHROME = find_chrome()

md_text = SRC.read_text(encoding="utf-8")

# ---- 표제부 분리: 첫 "## " 이전 = 제목·메타·중요 안내 ----
head, _, body = md_text.partition("\n## ")
body = "## " + body
title = ""
meta_lines, notice_lines = [], []
for line in head.splitlines():
    s = line.strip()
    if s.startswith("# "):
        title = s[2:].strip()
    elif s.startswith(">"):
        notice_lines.append(s.lstrip("> ").strip())
    elif s:
        meta_lines.append(s.rstrip("\\").strip())

conv = lambda t: markdown.markdown(t, extensions=["tables", "sane_lists"])
notice_html = conv(" ".join(notice_lines)) if notice_lines else ""
body_html = conv(body)

# 제목의 "v0.1" 꼬리를 작게
title_html = re.sub(r"\s*(v[\d.]+)$", r' <span class="ver">\1</span>', title)

html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 20mm 18mm 22mm; }}
  :root {{
    --ink:#272217; --faint:#837b68; --line:#ded5c0; --soft:#f1ede2; --gold:#9c7a2c;
    --serif:"KoPub Batang","KoPubWorld Batang","MaruBuri","Noto Serif KR","Nanum Myeongjo","HANBatang","Batang","AppleMyungjo",serif;
    --sans:"Pretendard Variable","Pretendard","Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif;
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;color:var(--ink);font-family:var(--sans);font-size:10.5pt;line-height:1.78;word-break:keep-all;overflow-wrap:break-word}}
  .masthead{{border-top:3px solid var(--ink);position:relative;padding-top:12pt;margin-bottom:18pt}}
  .masthead::before{{content:"";position:absolute;top:3.5pt;left:0;right:0;border-top:1px solid var(--ink)}}
  .mast-top{{display:flex;justify-content:space-between;font-size:8pt;letter-spacing:.14em;font-weight:600;color:var(--faint)}}
  h1{{font-family:var(--serif);font-weight:700;font-size:21pt;line-height:1.4;letter-spacing:-.01em;margin:14pt 0 8pt}}
  h1 .ver{{font-size:11pt;color:var(--gold);letter-spacing:.05em}}
  .mast-meta{{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:6pt 0;font-size:9pt;color:var(--faint)}}
  .mast-meta span+span::before{{content:"·";margin:0 6pt;color:var(--line)}}
  .notice{{border:1px solid var(--ink);padding:11pt 12pt 8pt;position:relative;margin:14pt 0 4pt;break-inside:avoid}}
  .notice::before{{content:"일 러 두 기";position:absolute;top:-6.5pt;left:10pt;background:#fff;padding:0 6pt;font-size:7.5pt;letter-spacing:.24em;font-weight:700;color:var(--gold)}}
  .notice p{{margin:3pt 0;font-size:9.5pt;line-height:1.75}}
  h2{{font-family:var(--serif);font-size:14pt;font-weight:700;letter-spacing:-.01em;border-top:2px solid var(--ink);padding-top:9pt;margin:26pt 0 8pt;break-after:avoid}}
  h3{{font-family:var(--serif);font-size:11.5pt;font-weight:700;margin:16pt 0 6pt;break-after:avoid}}
  h3::before{{content:"";display:inline-block;width:9pt;height:2.5pt;background:var(--gold);margin-right:6pt;vertical-align:3pt}}
  p{{margin:6pt 0}}
  ul,ol{{margin:6pt 0;padding-left:18pt}}
  li{{margin:3pt 0}}
  strong{{font-weight:700}}
  a{{color:var(--ink);text-decoration:underline;text-underline-offset:2pt;text-decoration-color:var(--faint)}}
  code{{font-family:inherit;background:var(--soft);padding:0 3pt;border-radius:2pt;font-size:9.5pt}}
  table{{width:100%;border-collapse:collapse;margin:10pt 0;font-size:9pt;line-height:1.6}}
  th{{font-weight:700;text-align:left;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:5pt 6pt;background:#faf8f1}}
  td{{border-bottom:1px solid var(--line);padding:5pt 6pt;vertical-align:top}}
  tr{{break-inside:avoid}}
  .colophon{{margin-top:24pt;border-top:2px solid var(--ink);padding-top:6pt;display:flex;justify-content:space-between;font-size:8pt;color:var(--faint);letter-spacing:.05em}}
</style>
</head>
<body>
  <header class="masthead">
    <div class="mast-top"><span>LEV LAB 진로교육 연구도구 · 부록</span><span>연구·수업용 프로토타입</span></div>
    <h1>{title_html}</h1>
    <div class="mast-meta">{"".join(f"<span>{m}</span>" for m in meta_lines)}</div>
  </header>
  <aside class="notice">{notice_html}</aside>
  {body_html}
  <footer class="colophon"><span>Lev Lab — 진로·사회정서교육 연구도구</span><span>cleveranawim-source.github.io/career-compass</span></footer>
</body>
</html>"""

with tempfile.TemporaryDirectory() as td:
    src_html = Path(td) / "guide_print.html"
    src_html.write_text(html, encoding="utf-8")
    raw_pdf = Path(td) / "raw.pdf"
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu",
        f"--user-data-dir={td}/profile", "--no-pdf-header-footer",
        f"--print-to-pdf={raw_pdf}", src_html.as_uri(),
    ], check=True, capture_output=True)

    # ---- 쪽번호 스탬프 ----
    reader = PdfReader(str(raw_pdf))
    n = len(reader.pages)
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    for i in range(n):
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(0.51, 0.48, 0.41)
        c.drawCentredString(A4[0] / 2, 26, f"–  {i + 1} / {n}  –")
        c.showPage()
    c.save()
    buf.seek(0)
    overlay = PdfReader(buf)
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        page.merge_page(overlay.pages[i])
        writer.add_page(page)
    with open(OUT, "wb") as f:
        writer.write(f)

print(f"OK: {OUT} ({n} pages)")
