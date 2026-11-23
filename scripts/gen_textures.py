"""
Generate the raster textures used by the JetBrains Islands UI themes.

Sublime Text themes are raster based: every texture is a PNG (white where it
should be tinted by the theme) plus @2x / @3x variants for Retina displays.
All output is white with alpha; the theme tints it through layer#.tint.
"""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "textures")
os.makedirs(OUT, exist_ok=True)
SS = 8  # supersampling factor, downsampled to 1x with Lanczos
WHITE = (255, 255, 255, 255)


def _rrect(size, box, radius, fill=None, outline=None, width=1):
    im = Image.new("RGBA", (size[0] * SS, size[1] * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = (v * SS for v in box)
    r = radius * SS
    kw = dict(radius=r)
    if fill:
        d.rounded_rectangle([x0, y0, x1, y1], fill=fill, **kw)
    if outline:
        d.rounded_rectangle([x0, y0, x1, y1], outline=outline, width=width * SS, **kw)
    return im


def emit(im, name):
    for idx, sfx in ((1, ""), (2, "@2x"), (3, "@3x")):
        out = im.resize((im.width * idx, im.height * idx), Image.LANCZOS) if idx > 1 else im
        out.save(os.path.join(OUT, f"{name}{sfx}.png"))


def pill(name, size, box, radius, stroke=False):
    """A rounded rectangle. stroke=True yields a 1px outline only (border layer)."""
    if stroke:
        im = _rrect(size, box, radius, outline=WHITE, width=1)
    else:
        im = _rrect(size, box, radius, fill=WHITE)
    emit(im.resize(size, Image.LANCZOS), name)


# Tab pill (44x32 canvas: 2px vertical breathing room, 6px corner radius, Islands arc 10/2)
pill("tab_pill", (44, 32), (5, 4, 38, 28), 6)
pill("tab_pill_border", (44, 32), (4.5, 3.5, 38.5, 28.5), 6.5, stroke=True)
# Sidebar selection row pill
pill("row_pill", (44, 24), (2, 2, 41, 21), 5)
# Editor/panel input pill + its border
pill("input_pill", (36, 30), (1, 1, 34, 28), 6)
pill("input_pill_border", (36, 30), (0.5, 0.5, 34.5, 28.5), 6, stroke=True)
# Buttons
pill("button_pill", (24, 24), (1, 1, 22, 22), 5)
pill("button_pill_border", (24, 24), (0.5, 0.5, 22.5, 22.5), 5.5, stroke=True)
pill("icon_button_pill", (24, 24), (2, 2, 21, 21), 4)


def chevron(name, points):
    im = Image.new("RGBA", (16 * SS, 16 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(x * SS, y * SS) for x, y in points], fill=WHITE, width=int(1.5 * SS), joint="curve")
    emit(im.resize((16, 16), Image.LANCZOS), name)


# IntelliJ expUI chevrons: small, 16px box, ~4px glyph
chevron("chevron_right", [(6, 5), (10, 8), (6, 11)])
chevron("chevron_down", [(5, 6), (8, 10), (11, 6)])


def line(name, size, box):
    """A 1px separator line texture (white), tinted by the theme."""
    im = Image.new("RGBA", (size[0] * SS, size[1] * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([v * SS for v in box], fill=WHITE)
    emit(im.resize(size, Image.LANCZOS), name)


line("separator_v", (3, 24), (1, 0, 2, 23))
line("separator_h", (24, 3), (0, 1, 23, 2))
line("tab_underline", (44, 8), (8, 5, 35, 6))
line("tabset_underline", (8, 4), (0, 2, 7, 2))

# Folder glyphs: 16x16 monochrome (tinted by icon_tint)
def folder(name, opened):
    im = Image.new("RGBA", (16 * SS, 16 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = int(1.2 * SS)
    r = 2 * SS
    if opened:
        d.rounded_rectangle([1 * SS, 3 * SS, 15 * SS - 1, 14 * SS - 1], radius=r, outline=WHITE, width=w)
        d.line([(1 * SS, 6 * SS), (15 * SS - 1, 6 * SS)], fill=WHITE, width=w)
        d.polygon([(3 * SS, 7 * SS), (15 * SS - 1, 7 * SS), (13 * SS, 13 * SS), (1 * SS, 13 * SS)],
                  fill=(255, 255, 255, 90), outline=WHITE, width=w)
    else:
        d.rounded_rectangle([1 * SS, 4 * SS, 15 * SS - 1, 14 * SS - 1], radius=r, outline=WHITE, width=w)
        d.line([(1 * SS, 6 * SS), (7 * SS, 6 * SS)], fill=WHITE, width=w)
        d.line([(4 * SS, 3 * SS), (7 * SS, 3 * SS)], fill=WHITE, width=w)
        d.line([(4 * SS, 3 * SS), (4 * SS, 4 * SS)], fill=WHITE, width=w)
        d.line([(7 * SS, 3 * SS), (7 * SS, 4 * SS)], fill=WHITE, width=w)
    emit(im.resize((16, 16), Image.LANCZOS), name)


folder("folder_closed", False)
folder("folder_open", True)

# Symlinked / duplicate folder: folder with a return arrow
im = Image.new("RGBA", (16 * SS, 16 * SS), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
w = int(1.2 * SS)
d.rounded_rectangle([1 * SS, 4 * SS, 12 * SS, 14 * SS - 1], radius=2 * SS, outline=WHITE, width=w)
d.line([(3 * SS, 3 * SS), (6 * SS, 3 * SS)], fill=WHITE, width=w)
d.polygon([(10 * SS, 2 * SS), (15 * SS, 5 * SS), (10 * SS, 8 * SS)], fill=WHITE)
emit(im.resize((16, 16), Image.LANCZOS), "folder_symlink")

print("textures:", len(os.listdir(OUT)))
