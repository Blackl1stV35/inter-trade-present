"""Render the slide sketches: outline/sketches/src/<id>.html (one fragment per page) -> outline/sketches/png/<id>.png at 1920x1080.

usage (from the repo root, after dot-sourcing scripts/env.ps1 so tools/fonts exists):
    python -I -X utf8 scripts/build_sketches.py                # every fragment
    python -I -X utf8 scripts/build_sketches.py S7 S9 A3       # only these ids
    python -I -X utf8 scripts/build_sketches.py --sheet        # also build the contact sheets

A fragment starts with one META comment (JSON) and then the HTML of the main area:
    <!--META {"id":"S7","chapter":"CH2","min":1.5,"label":"Observed data","chips":["M","Q","P"],
              "title":"...","foot":"Does not show ...","tags":"Comext DS-045409 · U24"} -->
    <div class="row grow"> ... </div>
The frame (ribbon, evidence label, title, footer, variable chips) comes from this script; see outline/sketches/README.md.
Each render also checks the page (overflow, text outside the slide, smallest font) and writes outline/sketches/png/_report/<id>.json.
"""
import html
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = os.getcwd()
SRC = os.path.join(ROOT, "outline", "sketches", "src")
OUT = os.path.join(ROOT, "outline", "sketches", "png")
CSS = os.path.join(ROOT, "outline", "sketches", "style.css")
VARS = ["X", "M", "NX", "BOP", "Q", "P", "GDP", "Tax", "C", "I", "G"]
LABELS = {
    "Observed data": "observed", "Policy rule": "policy", "Model-based result": "model",
    "Theoretical-illustrative": "theory", "Company announcement": "company", "Team judgement": "team",
}
CHAPTERS = [("CH1", "CH1 Policy"), ("CH2", "CH2 Economic effects"), ("CH3", "CH3 Conclusion"), ("BK", "Backup")]
MIN_FONT_PX = 38  # anything smaller than this (19 pt) is reported, except .tag text; body text should be 56 px (28 pt)

CHECK_JS = """
() => {
  const slide = document.getElementById('slide').getBoundingClientRect();
  const main = document.getElementById('main');
  const out = {overflow: [], outside: [], small: [], minFont: 999};
  if (main.scrollHeight > main.clientHeight + 24) out.overflow.push('main scrollHeight ' + main.scrollHeight + ' > ' + main.clientHeight);
  if (main.scrollWidth > main.clientWidth + 24) out.overflow.push('main scrollWidth ' + main.scrollWidth + ' > ' + main.clientWidth);
  const mr = main.getBoundingClientRect();
  for (const el of main.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.bottom > mr.bottom + 2 || r.right > mr.right + 2 || r.left < mr.left - 2 || r.top < mr.top - 2) {
      out.outside.push((el.tagName + '.' + (el.className || '')).slice(0, 40) + ' ' + Math.round(r.right - mr.right) + 'px right, ' + Math.round(r.bottom - mr.bottom) + 'px below');
    }
    const own = Array.from(el.childNodes).filter(n => n.nodeType === 3 && n.textContent.trim()).length;
    if (own && !el.classList.contains('tag')) {
      const fs = parseFloat(getComputedStyle(el).fontSize);
      out.minFont = Math.min(out.minFont, fs);
      if (fs < %d) out.small.push((el.textContent.trim().slice(0, 30)) + ' ' + fs + 'px');
    }
  }
  for (const id of ['title', 'foot']) {
    const el = document.getElementById(id);
    const kids = Array.from(el.children);
    let bottom = 0, top = 1e9;
    for (const k of kids) { const r = k.getBoundingClientRect(); bottom = Math.max(bottom, r.bottom); top = Math.min(top, r.top); }
    const box = el.getBoundingClientRect();
    if (kids.length && (bottom > box.bottom + 4 || top < box.top - 4)) out.overflow.push(id + ' content ' + Math.round(bottom - top) + 'px high in a ' + Math.round(box.height) + 'px box');
  }
  for (const img of document.images) { if (!img.complete || img.naturalWidth === 0) out.outside.push('broken image ' + img.getAttribute('src')); }
  out.outside = out.outside.slice(0, 8); out.small = out.small.slice(0, 8);
  return out;
}
""" % MIN_FONT_PX


def font_face_css():
    reg = os.path.join(ROOT, "tools", "fonts", "thsarabunnew-webfont.ttf")
    bold = os.path.join(ROOT, "tools", "fonts", "thsarabunnew_bold-webfont.ttf")
    if not (os.path.exists(reg) and os.path.exists(bold)):
        raise SystemExit("TH Sarabun New copies missing in tools/fonts; dot-source scripts/env.ps1 first")
    u = lambda p: "file:///" + p.replace("\\", "/")
    return ("@font-face{font-family:'TH Sarabun New';src:url('%s');font-weight:normal;}"
            "@font-face{font-family:'TH Sarabun New';src:url('%s');font-weight:bold;}" % (u(reg), u(bold)))


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->", text, re.S)
    if not m:
        raise SystemExit("%s: missing <!--META {...} --> comment" % path)
    meta = json.loads(m.group(1))
    return meta, text[m.end():]


def page_html(meta, body):
    ch = meta.get("chapter", "CH1")
    ribbon = "".join('<span class="%s">%s</span>' % ("on" if k == ch else "", html.escape(t)) for k, t in CHAPTERS)
    cls = LABELS.get(meta.get("label", ""), "team")
    label = '<div id="label" class="%s">%s</div>' % (cls, html.escape(meta.get("label", "")))
    lit = set(meta.get("chips", []))
    chips = "".join('<span class="%s">%s</span>' % ("on" if v in lit else "", v) for v in VARS)
    foot = html.escape(meta.get("foot", ""))
    if meta.get("tags"):
        foot += '<span class="tags">%s</span>' % html.escape(meta["tags"])
    sk = ("%s · %s min · sketch" % (meta["id"], meta["min"])) if meta.get("min") else ("%s · backup · sketch" % meta["id"])
    return (
        "<!doctype html><html><head><meta charset='utf-8'><base href='file:///%s/'>"
        "<style>%s</style><style>%s</style></head><body><div id='slide'>"
        "<div id='ribbon'>%s</div>%s<div id='title'><span>%s</span></div>"
        "<div id='main'>%s</div><div id='foot'>%s</div><div id='chips'>%s</div><div id='sktag'>%s</div>"
        "</div></body></html>"
    ) % (ROOT.replace("\\", "/"), font_face_css(), open(CSS, encoding="utf-8").read(), ribbon, label,
         html.escape(meta.get("title", "")), body, foot, chips, html.escape(sk))


def render(ids):
    os.makedirs(OUT, exist_ok=True)
    tmpdir = os.path.join(ROOT, "outline", "sketches", ".build")
    os.makedirs(tmpdir, exist_ok=True)
    rdir = os.path.join(OUT, "_report")
    os.makedirs(rdir, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        for sid in ids:
            src = os.path.join(SRC, sid + ".html")
            meta, body = parse(src)
            meta.setdefault("id", sid)
            tmp = os.path.join(tmpdir, sid + ".html")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(page_html(meta, body))
            page.goto("file:///" + tmp.replace("\\", "/"))
            page.evaluate("document.fonts.ready")
            page.wait_for_load_state("load")
            res = page.evaluate(CHECK_JS)
            page.screenshot(path=os.path.join(OUT, sid + ".png"))
            ok = not (res["overflow"] or res["outside"])
            json.dump({"id": sid, "ok": ok, **res}, open(os.path.join(rdir, sid + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            print("%-4s %s  minFont %spx%s" % (sid, "ok  " if ok else "FAIL", res["minFont"],
                  "" if ok else "  " + "; ".join(res["overflow"] + res["outside"])[:300]))
            if res["small"]:
                print("      small text:", "; ".join(res["small"]))
        browser.close()


def sheets():
    from PIL import Image
    ids = sorted((f[:-5] for f in os.listdir(SRC) if f.endswith(".html")),
                 key=lambda s: (s[0] != "S", int(re.sub(r"\D", "", s))))
    for prefix, name in (("S", "contact-sheet-main.png"), ("A", "contact-sheet-backup.png")):
        sel = [i for i in ids if i.startswith(prefix) and os.path.exists(os.path.join(OUT, i + ".png"))]
        if not sel:
            continue
        w, h, cols = 640, 360, 3
        rows = (len(sel) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + 12) + 12), (225, 228, 231))
        for n, i in enumerate(sel):
            im = Image.open(os.path.join(OUT, i + ".png")).convert("RGB").resize((w, h), Image.LANCZOS)
            sheet.paste(im, (12 + (n % cols) * (w + 12), 12 + (n // cols) * (h + 12)))
        sheet.save(os.path.join(ROOT, "outline", "sketches", name))
        print("wrote", name, len(sel), "pages")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ids = args or sorted((f[:-5] for f in os.listdir(SRC) if f.endswith(".html")),
                         key=lambda s: (s[0] != "S", int(re.sub(r"\D", "", s))))
    render(ids)
    if "--sheet" in sys.argv:
        sheets()
