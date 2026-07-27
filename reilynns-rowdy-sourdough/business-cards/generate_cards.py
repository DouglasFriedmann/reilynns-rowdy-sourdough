"""
Generate UPS Store print-ready business cards for Reilynn's Rowdy Sourdough.
Creates: SVG, PDF (with bleed), and 300 DPI PNG for front + back.
"""
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, HexColor
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Ellipse, Group, Polygon
from reportlab.graphics import renderPDF, renderPM

OUT = Path(__file__).resolve().parent
FONTS = Path(r"C:\Windows\Fonts")

# Register fonts
pdfmetrics.registerFont(TTFont("BrandSans", str(FONTS / "ARIALNB.TTF")))  # condensed bold
pdfmetrics.registerFont(TTFont("BodySans", str(FONTS / "segoeui.ttf")))
pdfmetrics.registerFont(TTFont("BodySansBold", str(FONTS / "segoeuib.ttf")))
pdfmetrics.registerFont(TTFont("Script", str(FONTS / "segoesc.ttf")))
pdfmetrics.registerFont(TTFont("ScriptBold", str(FONTS / "segoescb.ttf")))

# Brand colors
CREAM = HexColor("#F6F0E4")
BROWN = HexColor("#4A2318")
PINK = HexColor("#E891AE")
PINK_DEEP = HexColor("#D9789A")
PINK_SOFT = HexColor("#F5C4D5")
GOLD = HexColor("#C9A04A")
WHITE = HexColor("#FFFFFF")

# Sizes
TRIM_W, TRIM_H = 3.5 * inch, 2.0 * inch
BLEED = 0.125 * inch
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED  # 3.75 x 2.25


def draw_bowl_mark(c, cx, cy, scale=1.0):
    """Draw pink bowl + spoon + sparkle stars (brand mark)."""
    s = scale

    # Flour/sparkle dots
    c.setFillColor(HexColor("#FFF8F0"))
    for x, y, r in [(-18, 16, 2.2), (-8, 22, 3.0), (4, 20, 2.0), (14, 12, 1.6)]:
        c.circle(cx + x * s, cy + y * s, r * s, fill=1, stroke=0)

    # Stars
    def star(sx, sy, r, color):
        c.setFillColor(color)
        pts = []
        import math
        for i in range(8):
            ang = math.radians(-90 + i * 45)
            rad = r if i % 2 == 0 else r * 0.4
            pts.append((sx + rad * math.cos(ang), sy + rad * math.sin(ang)))
        p = c.beginPath()
        p.moveTo(pts[0][0], pts[0][1])
        for px, py in pts[1:]:
            p.lineTo(px, py)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    star(cx - 22 * s, cy + 18 * s, 5.5 * s, PINK)
    star(cx + 20 * s, cy + 22 * s, 4 * s, GOLD)
    star(cx - 28 * s, cy + 6 * s, 3.2 * s, PINK)

    # Spoon (rotated-ish via offset)
    c.setFillColor(PINK_DEEP)
    c.saveState()
    c.translate(cx + 10 * s, cy + 2 * s)
    c.rotate(18)
    c.roundRect(-2.2 * s, -8 * s, 4.4 * s, 28 * s, 2.2 * s, fill=1, stroke=0)
    c.ellipse(-5 * s, 16 * s, 5 * s, 28 * s, fill=1, stroke=0)
    c.restoreState()

    # Dough in bowl
    c.setFillColor(HexColor("#FBEEDF"))
    c.ellipse(cx - 22 * s, cy - 4 * s, cx + 22 * s, cy + 8 * s, fill=1, stroke=0)

    # Bowl body
    c.setFillColor(PINK_SOFT)
    p = c.beginPath()
    p.moveTo(cx - 26 * s, cy)
    p.curveTo(cx - 26 * s, cy - 28 * s, cx + 26 * s, cy - 28 * s, cx + 26 * s, cy)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Bowl rim
    c.setFillColor(HexColor("#FCE0EA"))
    c.ellipse(cx - 26 * s, cy - 3 * s, cx + 26 * s, cy + 4 * s, fill=1, stroke=0)


def draw_globe(c, x, y, size=8):
    c.setStrokeColor(PINK_DEEP)
    c.setFillColor(PINK_DEEP)
    c.setLineWidth(0.9)
    c.circle(x, y, size, fill=0, stroke=1)
    c.ellipse(x - size * 0.45, y - size, x + size * 0.45, y + size, fill=0, stroke=1)
    c.line(x - size, y, x + size, y)
    c.line(x - size * 0.75, y + size * 0.5, x + size * 0.75, y + size * 0.5)
    c.line(x - size * 0.75, y - size * 0.5, x + size * 0.75, y - size * 0.5)


def draw_chat_icon(c, x, y, size=9):
    c.setFillColor(PINK_DEEP)
    c.roundRect(x - size, y - size * 0.55, size * 2, size * 1.35, size * 0.35, fill=1, stroke=0)
    # little tail
    p = c.beginPath()
    p.moveTo(x - size * 0.2, y - size * 0.55)
    p.lineTo(x - size * 0.75, y - size * 1.15)
    p.lineTo(x + size * 0.35, y - size * 0.55)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # phone silhouette
    c.setFillColor(CREAM)
    c.roundRect(x - size * 0.35, y - size * 0.25, size * 0.7, size * 0.95, 1.2, fill=1, stroke=0)


def draw_star_line(c, x1, x2, y, color=PINK):
    mid = (x1 + x2) / 2
    c.setStrokeColor(color)
    c.setLineWidth(1.0)
    c.line(x1, y, mid - 8, y)
    c.line(mid + 8, y, x2, y)
    # star
    import math
    c.setFillColor(color)
    r = 4.5
    pts = []
    for i in range(8):
        ang = math.radians(-90 + i * 45)
        rad = r if i % 2 == 0 else r * 0.38
        pts.append((mid + rad * math.cos(ang), y + rad * math.sin(ang)))
    p = c.beginPath()
    p.moveTo(pts[0][0], pts[0][1])
    for px, py in pts[1:]:
        p.lineTo(px, py)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def draw_front(c):
    # Full bleed background
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Content sits in trim area (offset by bleed)
    ox, oy = BLEED, BLEED

    # Vertical divider
    div_x = ox + 1.15 * inch
    c.setStrokeColor(HexColor("#C9B7A5"))
    c.setLineWidth(0.8)
    c.line(div_x, oy + 0.18 * inch, div_x, oy + TRIM_H - 0.18 * inch)

    # Left: bowl mark
    draw_bowl_mark(c, ox + 0.58 * inch, oy + 1.05 * inch, scale=1.55)

    # Right content
    rx = div_x + 0.16 * inch
    right_w = ox + TRIM_W - rx - 0.14 * inch

    # Brand name
    c.setFillColor(BROWN)
    c.setFont("BrandSans", 13.5)
    c.drawString(rx, oy + 1.52 * inch, "REILYNN'S")
    c.drawString(rx, oy + 1.30 * inch, "ROWDY")
    c.drawString(rx, oy + 1.08 * inch, "SOURDOUGH")

    # Star divider
    draw_star_line(c, rx, rx + right_w, oy + 0.92 * inch, PINK)

    # Website
    draw_globe(c, rx + 6, oy + 0.72 * inch, size=5.5)
    c.setFillColor(BROWN)
    c.setFont("BodySans", 8.5)
    c.drawString(rx + 16, oy + 0.68 * inch, "www.rowdysourdough.com")

    # Text orders
    draw_chat_icon(c, rx + 7, oy + 0.46 * inch, size=6.5)
    c.setFillColor(PINK_DEEP)
    c.setFont("BodySansBold", 8)
    c.drawString(rx + 18, oy + 0.42 * inch, "TEXT ORDERS")

    # Phone
    c.setFillColor(BROWN)
    c.setFont("BrandSans", 16)
    c.drawString(rx, oy + 0.18 * inch, "201-572-4418")


def draw_back(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    ox, oy = BLEED, BLEED
    left = ox + 0.35 * inch
    right = ox + TRIM_W - 0.35 * inch

    # Top star line
    draw_star_line(c, left, right, oy + TRIM_H - 0.42 * inch, PINK)

    # Script line
    c.setFillColor(BROWN)
    c.setFont("ScriptBold", 28)
    text = "Homemade in NJ"
    tw = c.stringWidth(text, "ScriptBold", 28)
    c.drawString((PAGE_W - tw) / 2, oy + 0.95 * inch, text)

    # Tagline
    c.setFont("BodySans", 11)
    tag = "Not your average dough!"
    tw2 = c.stringWidth(tag, "BodySans", 11)
    c.drawString((PAGE_W - tw2) / 2, oy + 0.62 * inch, tag)

    # Bottom star line
    draw_star_line(c, left, right, oy + 0.38 * inch, PINK)


def write_pdf(path, drawer):
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    drawer(c)
    # Optional: light crop marks outside bleed aren't needed when bleed is in page.
    # UPS usually wants clean bleed PDF without crop marks.
    c.showPage()
    c.save()


def write_png(path, drawer, dpi=300):
    # Render via a temporary PDF then rasterize with Pillow + pypdfium2 if available,
    # otherwise draw with reportlab renderPM via a workaround: use pdf2image-free approach.
    # Simplest reliable path: write PDF then use PIL with reportlab's renderPM on a Drawing —
    # For full fidelity, convert PDF pages with pillow by re-drawing at pixel size using reportlab.
    from reportlab.lib.utils import ImageReader
    import io

    # Draw to PDF in memory, then use a high-res canvas via PIL by replaying isn't easy.
    # Use reportlab canvas to PNG via ghostscript-free method: pixel canvas with scale.
    px_w = int(3.75 * dpi)
    px_h = int(2.25 * dpi)
    scale = dpi / 72.0  # reportlab points are 1/72"

    # Create PDF then rasterize with PyMuPDF if present; else fall back to SVG note.
    tmp_pdf = path.with_suffix(".tmp.pdf")
    write_pdf(tmp_pdf, drawer)

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(tmp_pdf)
        page = doc[0]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(str(path))
        doc.close()
        tmp_pdf.unlink(missing_ok=True)
        return True
    except Exception:
        # Fallback: keep PDF only; copy tmp as final if needed
        tmp_pdf.unlink(missing_ok=True)
        return False


def write_svg_front(path):
    # Vector SVG at trim size with bleed viewBox in inches converted to px at 96dpi for screen,
    # but sized correctly for print (use inches in SVG).
    w, h = 3.75, 2.25
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}in" height="{h}in" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="#F6F0E4"/>
  <!-- trim guide (do not print): 0.125in inset -->
  <g transform="translate(0.125,0.125)">
    <line x1="1.15" y1="0.18" x2="1.15" y2="1.82" stroke="#C9B7A5" stroke-width="0.01"/>
    <!-- bowl icon simplified -->
    <g transform="translate(0.58,0.95)">
      <circle cx="-0.22" cy="-0.22" r="0.03" fill="#FFF8F0"/>
      <circle cx="-0.08" cy="-0.28" r="0.04" fill="#FFF8F0"/>
      <path d="M-0.28,-0.22 l0.03,0.06 -0.065,0.01 0.047,0.045 -0.012,0.065 0.057,-0.03 0.057,0.03 -0.012,-0.065 0.047,-0.045 -0.065,-0.01z" fill="#E891AE"/>
      <path d="M0.22,-0.28 l0.02,0.04 -0.043,0.007 0.031,0.03 -0.008,0.043 0.038,-0.02 0.038,0.02 -0.008,-0.043 0.031,-0.03 -0.043,-0.007z" fill="#C9A04A"/>
      <g transform="rotate(18 0.12 -0.02)">
        <rect x="0.09" y="-0.12" width="0.06" height="0.38" rx="0.03" fill="#D9789A"/>
        <ellipse cx="0.12" cy="-0.14" rx="0.07" ry="0.09" fill="#D9789A"/>
      </g>
      <ellipse cx="0" cy="-0.02" rx="0.30" ry="0.08" fill="#FBEEDF"/>
      <path d="M-0.34,0 C-0.34,0.36 0.34,0.36 0.34,0 Z" fill="#F5C4D5"/>
      <ellipse cx="0" cy="0" rx="0.34" ry="0.05" fill="#FCE0EA"/>
    </g>
    <text x="1.35" y="0.42" font-family="Arial Narrow, Arial, sans-serif" font-weight="700" font-size="0.19" fill="#4A2318">REILYNN'S</text>
    <text x="1.35" y="0.62" font-family="Arial Narrow, Arial, sans-serif" font-weight="700" font-size="0.19" fill="#4A2318">ROWDY</text>
    <text x="1.35" y="0.82" font-family="Arial Narrow, Arial, sans-serif" font-weight="700" font-size="0.19" fill="#4A2318">SOURDOUGH</text>
    <line x1="1.35" y1="0.98" x2="2.05" y2="0.98" stroke="#E891AE" stroke-width="0.012"/>
    <line x1="2.25" y1="0.98" x2="3.20" y2="0.98" stroke="#E891AE" stroke-width="0.012"/>
    <path d="M2.15,0.98 l0.015,0.03 -0.033,0.005 0.024,0.022 -0.006,0.033 0.029,-0.015 0.029,0.015 -0.006,-0.033 0.024,-0.022 -0.033,-0.005z" fill="#E891AE"/>
    <text x="1.55" y="1.22" font-family="Segoe UI, Arial, sans-serif" font-size="0.12" fill="#4A2318">www.rowdysourdough.com</text>
    <circle cx="1.43" cy="1.18" r="0.07" fill="none" stroke="#D9789A" stroke-width="0.012"/>
    <text x="1.55" y="1.48" font-family="Segoe UI, Arial, sans-serif" font-weight="700" font-size="0.11" fill="#D9789A">TEXT ORDERS</text>
    <text x="1.35" y="1.78" font-family="Arial Narrow, Arial, sans-serif" font-weight="700" font-size="0.24" fill="#4A2318">201-572-4418</text>
  </g>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def write_svg_back(path):
    w, h = 3.75, 2.25
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}in" height="{h}in" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="#F6F0E4"/>
  <g transform="translate(0.125,0.125)">
    <line x1="0.35" y1="0.40" x2="1.55" y2="0.40" stroke="#E891AE" stroke-width="0.012"/>
    <line x1="1.95" y1="0.40" x2="3.15" y2="0.40" stroke="#E891AE" stroke-width="0.012"/>
    <path d="M1.75,0.40 l0.02,0.04 -0.044,0.007 0.032,0.03 -0.008,0.044 0.038,-0.02 0.038,0.02 -0.008,-0.044 0.032,-0.03 -0.044,-0.007z" fill="#E891AE"/>
    <text x="1.75" y="1.05" text-anchor="middle" font-family="Segoe Script, Brush Script MT, cursive" font-size="0.42" fill="#4A2318">Homemade in NJ</text>
    <text x="1.75" y="1.40" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="0.16" fill="#4A2318">Not your average dough!</text>
    <line x1="0.35" y1="1.60" x2="1.55" y2="1.60" stroke="#E891AE" stroke-width="0.012"/>
    <line x1="1.95" y1="1.60" x2="3.15" y2="1.60" stroke="#E891AE" stroke-width="0.012"/>
    <path d="M1.75,1.60 l0.02,0.04 -0.044,0.007 0.032,0.03 -0.008,0.044 0.038,-0.02 0.038,0.02 -0.008,-0.044 0.032,-0.03 -0.044,-0.007z" fill="#E891AE"/>
  </g>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def main():
    write_pdf(OUT / "business-card-front.pdf", draw_front)
    write_pdf(OUT / "business-card-back.pdf", draw_back)

    # Combined single PDF (front then back) — handy for UPS
    combined = OUT / "business-cards-print-ready.pdf"
    c = canvas.Canvas(str(combined), pagesize=(PAGE_W, PAGE_H))
    draw_front(c)
    c.showPage()
    draw_back(c)
    c.showPage()
    c.save()

    write_svg_front(OUT / "business-card-front.svg")
    write_svg_back(OUT / "business-card-back.svg")

    png_ok = write_png(OUT / "business-card-front-300dpi.png", draw_front)
    png_ok = write_png(OUT / "business-card-back-300dpi.png", draw_back) and png_ok

    readme = OUT / "PRINT-INSTRUCTIONS.txt"
    readme.write_text(
        """Reilynn's Rowdy Sourdough — Business Card Print Pack
=====================================================

WHAT TO GIVE THE UPS STORE
--------------------------
Best option (recommended):
  business-cards-print-ready.pdf
    • Page 1 = FRONT
    • Page 2 = BACK
    • Includes 0.125" bleed on all sides
    • Trim size: 3.5" × 2"
    • Full page size with bleed: 3.75" × 2.25"

Also included (if they ask):
  business-card-front.pdf
  business-card-back.pdf
  business-card-front.svg / business-card-back.svg  (vector sources)
  business-card-front-300dpi.png / business-card-back-300dpi.png  (if generated)

TELL THE PRINT ASSOCIATE
------------------------
  • Quantity: 100 (or however many you want)
  • Size: Standard business card 3.5" × 2"
  • Sides: Double-sided (front + back)
  • Paper: Soft gloss / matte / linen — cream/ivory stock looks nicest with this design
  • Color: Full color both sides
  • File already includes bleed (0.125")
  • Safe margin: keep important text away from edges (already done)
  • Do NOT scale to fit — print at 100% / actual size

CARD CONTENT
------------
FRONT
  Reilynn's Rowdy Sourdough
  www.rowdysourdough.com
  TEXT ORDERS  201-572-4418

BACK
  Homemade in NJ
  Not your average dough!

NOTES
-----
• Colors are rich cream + sourdough brown + pink to match your brand.
• UPS Store can usually print the PDF same day.
• Ask to see a digital proof on screen before they run all 100.
""",
        encoding="utf-8",
    )

    print("Wrote files to", OUT)
    for p in sorted(OUT.glob("business-card*")):
        print(" -", p.name, f"({p.stat().st_size} bytes)")
    print(" -", readme.name)
    print("PNG generated:" if png_ok else "PNG skipped (install pymupdf for PNG):", png_ok)


if __name__ == "__main__":
    main()
