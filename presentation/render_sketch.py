"""Render the pitch sketch as 1600x900 PNG slides and the externality dial as a GIF.

Run from any folder:  python presentation/render_sketch.py
Reads  presentation/pitch-sketch.md
Writes presentation/png/page-01.png ... page-12.png and presentation/png/externality-dial.gif
"""
import pathlib
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent
SKETCH = ROOT / "pitch-sketch.md"
OUT = ROOT / "png"
OUT.mkdir(exist_ok=True)

FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"

W, H = 1600, 900
MARGIN = 90
BODY_TOP = 200
BODY_BOTTOM = H - 80
CONTENT_W = W - 2 * MARGIN
BODY_SIZES = [32, 30, 28, 26, 24, 22, 20]

NAVY = (38, 52, 68)
BLUE = (43, 92, 152)
TEAL = (22, 122, 103)
GREY = (60, 68, 78)
MUTED = (120, 130, 140)
WHITE = (255, 255, 255)
PAPER = (250, 251, 252)

LABEL_RE = re.compile(r"^([^:]{1,34}):\s+(.*)$")


def font(path, size):
    return ImageFont.truetype(path, size)


def parse_sketch(text):
    pages = []
    cur = None
    for raw in text.splitlines():
        m = re.match(r"^## Page (\d+)\. (.*)$", raw)
        if m:
            cur = {"num": int(m.group(1)), "title": m.group(2).strip(), "lines": []}
            pages.append(cur)
            continue
        if raw.startswith("## "):
            cur = None
            continue
        if cur is None or raw.strip() in ("", "---"):
            continue
        cur["lines"].append(raw)
    return pages


def wrap(draw, text, fnt, width, first_width=None):
    words = text.split()
    lines, cur = [], ""
    limit = first_width if first_width is not None else width
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= limit or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            limit = width
    if cur:
        lines.append(cur)
    return lines


def layout_body(draw, lines, size):
    """Return (commands, total_height). A command is (x, y, text, fnt, color)."""
    fnt = font(FONT_REG, size)
    bold = font(FONT_BOLD, size)
    line_h = int(size * 1.42)
    gap = int(size * 0.55)
    cmds = []
    y = 0
    for raw in lines:
        indent = 0
        stripped = raw
        if raw.startswith("  "):
            indent = 60
            stripped = raw.strip()
        if stripped.startswith("- "):
            stripped = stripped[2:]
        m = LABEL_RE.match(stripped)
        if m and len(m.group(1)) <= 34:
            label = m.group(1) + ":"
            content = m.group(2)
            lab_w = draw.textlength(label + " ", font=bold)
            first_w = CONTENT_W - indent - lab_w
            wrapped = wrap(draw, content, fnt, CONTENT_W - indent, first_w)
            cmds.append((indent, y, label, bold, BLUE))
            if wrapped:
                cmds.append((indent + lab_w, y, wrapped[0], fnt, GREY))
                y += line_h
                for ln in wrapped[1:]:
                    cmds.append((indent, y, ln, fnt, GREY))
                    y += line_h
            else:
                y += line_h
        else:
            wrapped = wrap(draw, stripped, fnt, CONTENT_W - indent)
            for ln in wrapped:
                cmds.append((indent, y, ln, fnt, GREY))
                y += line_h
        y += gap
    return cmds, y


def render_page(page, dummy_draw):
    chosen = None
    for size in BODY_SIZES:
        cmds, height = layout_body(dummy_draw, page["lines"], size)
        if BODY_TOP + height <= BODY_BOTTOM:
            chosen = (size, cmds)
            break
    if chosen is None:
        size = BODY_SIZES[-1]
        cmds, _ = layout_body(dummy_draw, page["lines"], size)
        chosen = (size, cmds)
        print(f"WARNING: page {page['num']} overflows at {size} pt")

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=NAVY)

    num_font = font(FONT_BOLD, 26)
    title_font = font(FONT_BOLD, 54)
    foot_font = font(FONT_REG, 20)
    d.text((MARGIN, 52), f"PAGE {page['num']} OF 12", font=num_font, fill=TEAL)
    d.text((MARGIN, 88), page["title"], font=title_font, fill=NAVY)
    d.line([(MARGIN, 165), (W - MARGIN, 165)], fill=(210, 216, 222), width=2)

    size, cmds = chosen
    for x, y, text, fnt, color in cmds:
        d.text((MARGIN + x, BODY_TOP + y), text, font=fnt, fill=color)

    d.text((MARGIN, H - 50),
           "The Steel Question | Final deck draft | Facts from the report, policy as of 2 November 2026",
           font=foot_font, fill=MUTED)
    return img


def dial_frame(t):
    q = np.linspace(0, 120, 300)
    demand = 120 - q
    pmc = 20 + q
    smc = 20 + q + t
    q_soc = (100 - t) / 2
    p_soc = 120 - q_soc

    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=100)
    ax.plot(q, demand, color="#263444", lw=3, label="Demand: P = 120 - Q")
    ax.plot(q, pmc, color="#2B5C98", lw=2.5, ls="--", label="Private marginal cost: P = 20 + Q")
    ax.plot(q, smc, color="#167A67", lw=3.5, label=f"Social marginal cost: private cost + {t}")
    ax.axvline(50, color="#2B5C98", lw=1.5, ls=":")
    ax.axvline(q_soc, color="#167A67", lw=1.5, ls=":")
    ax.scatter([50], [70], s=160, color="#2B5C98", zorder=5)
    ax.scatter([q_soc], [p_soc], s=160, color="#167A67", zorder=5)
    ax.annotate(f"Market: Q = 50, P = 70", xy=(50, 70), xytext=(56, 40),
                fontsize=15, color="#2B5C98",
                arrowprops=dict(arrowstyle="-", color="#2B5C98"))
    if t == 0:
        ax.annotate("Social optimum = market", xy=(q_soc, p_soc), xytext=(58, 118),
                    fontsize=15, color="#167A67",
                    arrowprops=dict(arrowstyle="-", color="#167A67"))
    else:
        ax.annotate(f"Social optimum: Q = {q_soc:g}, P = {p_soc:g}", xy=(q_soc, p_soc),
                    xytext=(2, 118), fontsize=15, color="#167A67",
                    arrowprops=dict(arrowstyle="-", color="#167A67"))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 150)
    ax.set_xlabel("Quantity (illustrative units)", fontsize=15)
    ax.set_ylabel("Price / marginal cost (index)", fontsize=15)
    ax.grid(True, color="#e6e6e6")
    ax.tick_params(labelsize=13)
    ax.legend(loc="upper right", fontsize=12, frameon=False)
    fig.suptitle(f"External cost t = {t:>2}   (illustrative model, invented numbers)",
                 fontsize=18, color="#263444", y=0.97)
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.11, top=0.90)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[..., :3].copy()
    plt.close(fig)
    return Image.fromarray(buf)


def build_gif(path):
    sequence = [0, 5, 10, 15, 20, 25, 30, 35, 40, 35, 30, 25, 20, 15, 10, 5]
    frames, durations = [], []
    for t in sequence:
        frame = dial_frame(t).quantize(colors=128, method=Image.Quantize.MEDIANCUT)
        frames.append(frame)
        durations.append(900 if t in (0, 40) else 380)
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)


def main():
    pages = parse_sketch(SKETCH.read_text(encoding="utf-8"))
    dummy = ImageDraw.Draw(Image.new("RGB", (W, H)))
    for page in pages:
        img = render_page(page, dummy)
        img.save(OUT / f"page-{page['num']:02d}.png", optimize=True)
    print(f"Rendered {len(pages)} pages to {OUT}")
    gif_path = OUT / "externality-dial.gif"
    build_gif(gif_path)
    print(f"Wrote {gif_path}")


if __name__ == "__main__":
    main()
