#!/usr/bin/env python3
"""Generate the 1200x630 share-card art for the Homme Thai Supper Club site.
System fonts (Palatino.ttc, Supplemental/Georgia Italic.ttf, Helvetica.ttc);
geometry derived from measured text extents; output public/og.png."""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
CREAM = (248, 241, 226)
CARD = (255, 250, 240)
BUTTER = (240, 215, 136)
BRICK = (155, 61, 34)
INK = (43, 32, 24)
SMOKE = (107, 95, 79)

def F(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

PALA = "/System/Library/Fonts/Palatino.ttc"
GEORGIA_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
HELV = "/System/Library/Fonts/Helvetica.ttc"

def spaced(draw, xy, text, font, fill, ls=0.0, anchor="la"):
    x, y = xy
    if not ls:
        draw.text((x, y), text, font=font, fill=fill, anchor=anchor)
        return draw.textlength(text, font=font)
    total = draw.textlength(text, font=font) + ls * max(0, len(text) - 1)
    if anchor == "ma":
        x -= total / 2
    elif anchor == "ra":
        x -= total
    cy = x
    for ch in text:
        draw.text((cy, y), ch, font=font, fill=fill)
        cy += draw.textlength(ch, font=font) + ls
    return total - ls

def fit_font(draw, text, path, start, max_w, index=0):
    size = start
    while size > 12 and draw.textlength(text, font=F(path, size, index)) > max_w:
        size -= 2
    return F(path, size, index)

def main(out_path="public/og.png"):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # double rule frame
    d.rectangle([22, 22, W - 22, H - 22], outline=BRICK, width=2)
    d.rectangle([31, 31, W - 31, H - 31], outline=INK, width=1)

    # right side: brick plate roundel with butter rings + cream H
    cx, cy, r = 952, 318, 152
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRICK)
    d.ellipse([cx - r + 13, cy - r + 13, cx + r - 13, cy + r - 13], outline=BUTTER, width=3)
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], outline=BUTTER, width=1)
    hf = F(PALA, 168, 0)
    d.text((cx, cy), "H", font=hf, fill=CREAM, anchor="mm")

    # left copy block — keep clear of the plate (text area ends x=780)
    tx = 72
    kicker_f = F(HELV, 21, 1)  # Helvetica Bold
    spaced(d, (tx, 78), "UPTOWN PHOENIX · SOUTHERN THAI SUPPER CLUB", kicker_f, BRICK, ls=4.2)
    d.line([(tx, 116), (780, 116)], fill=BUTTER, width=3)

    # headline (Palatino bold, fit inside the copy column)
    head = "HOMME"
    hf2 = fit_font(d, head, PALA, 190, 660, index=2)
    d.text((tx, 150), head, font=hf2, fill=INK, anchor="la")
    hl_bot = 150 + hf2.size * 1.25
    pron_f = F(GEORGIA_I, 40)
    d.text((tx + 6, hl_bot + 6), "pronounced “homey”", font=pron_f, fill=BRICK, anchor="la")

    # tagline (Palatino regular + italic emphasis line)
    tag_f = fit_font(d, "Generational Thai recipes,", PALA, 46, 680, index=0)
    d.text((tx, 400), "Generational Thai recipes,", font=tag_f, fill=INK, anchor="la")
    ital_f = F(PALA, 44, 1)
    d.text((tx, 458), "shared around the table.", font=ital_f, fill=INK, anchor="la")

    # bottom line + butter foot rule
    foot_f = F(HELV, 21, 0)  # Helvetica regular
    spaced(d, (tx, 552), "322 E. CAMELBACK ROAD · PHOENIX, ARIZONA · OPEN TUE–SUN", foot_f, (70, 57, 43), ls=2.4)
    d.line([(tx, 588), (W - 72, 588)], fill=BUTTER, width=2)

    img.save(out_path, "PNG", optimize=True)
    print(out_path, img.size)

if __name__ == "__main__":
    main(*(sys.argv[1:] or []))
