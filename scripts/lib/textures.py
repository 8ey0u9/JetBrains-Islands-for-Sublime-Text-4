"""Render the theme's white/alpha PNG textures at 1x, 2x and 3x."""
from PIL import Image, ImageDraw

from . import ROOT, SRC

OUT = SRC / "textures"
SS = 8  # Each density is downsampled directly from the supersampled master.
WHITE = (255, 255, 255, 255)


def _rrect(size, box, radius, fill=None, outline=None, width=1):
    im = Image.new("RGBA", (size[0] * SS, size[1] * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = (v * SS for v in box)
    r = radius * SS
    if fill:
        d.rounded_rectangle([x0, y0, x1, y1], fill=fill, radius=r)
    if outline:
        d.rounded_rectangle([x0, y0, x1, y1], outline=outline, width=width * SS, radius=r)
    return im


def emit(im, name):
    for scale, suffix in ((1, ""), (2, "@2x"), (3, "@3x")):
        out = im.resize((im.width // SS * scale, im.height // SS * scale), Image.LANCZOS)
        out.save(OUT / f"{name}{suffix}.png")


def pill(name, size, box, radius, stroke=False):
    if stroke:
        im = _rrect(size, box, radius, outline=WHITE, width=1)
    else:
        im = _rrect(size, box, radius, fill=WHITE)
    emit(im, name)


def chevron(name, points):
    im = Image.new("RGBA", (16 * SS, 16 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(x * SS, y * SS) for x, y in points], fill=WHITE, width=int(1.5 * SS), joint="curve")
    emit(im, name)


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
    emit(im, name)


def build():
    OUT.mkdir(exist_ok=True)
    # Rounded and square tabs share the same canvas and spacing.
    pill("tab_pill", (44, 32), (5, 4, 38, 28), 6)
    pill("tab_pill_border", (44, 32), (4.5, 3.5, 38.5, 28.5), 6.5, stroke=True)
    pill("tab_square", (44, 32), (5, 4, 38, 28), 0)
    pill("tab_square_border", (44, 32), (4.5, 3.5, 38.5, 28.5), 0, stroke=True)
    pill("row_pill", (44, 24), (2, 2, 41, 21), 5)
    pill("input_pill", (36, 30), (1, 1, 34, 28), 6)
    pill("input_pill_border", (36, 30), (0.5, 0.5, 34.5, 28.5), 6, stroke=True)
    pill("button_pill", (24, 24), (1, 1, 22, 22), 5)
    pill("button_pill_border", (24, 24), (0.5, 0.5, 22.5, 22.5), 5.5, stroke=True)
    pill("icon_button_pill", (24, 24), (2, 2, 21, 21), 4)
    pill("popup_pill", (40, 40), (1, 1, 39, 39), 8)
    pill("popup_pill_border", (40, 40), (0.5, 0.5, 39.5, 39.5), 8.5, stroke=True)
    chevron("chevron_right", [(6, 5), (10, 8), (6, 11)])
    chevron("chevron_down", [(5, 6), (8, 10), (11, 6)])
    folder("folder_closed", False)
    folder("folder_open", True)

    # Symlinked / duplicate folder: folder with a return arrow.
    im = Image.new("RGBA", (16 * SS, 16 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = int(1.2 * SS)
    d.rounded_rectangle([1 * SS, 4 * SS, 12 * SS, 14 * SS - 1], radius=2 * SS, outline=WHITE, width=w)
    d.line([(3 * SS, 3 * SS), (6 * SS, 3 * SS)], fill=WHITE, width=w)
    d.polygon([(10 * SS, 2 * SS), (15 * SS, 5 * SS), (10 * SS, 8 * SS)], fill=WHITE)
    emit(im, "folder_symlink")
    print("textures:", len(list(OUT.glob("*.png"))))
