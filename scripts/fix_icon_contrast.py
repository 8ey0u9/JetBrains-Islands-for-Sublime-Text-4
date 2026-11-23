"""
Post-process the third-party Material Icon Theme icons for both flavours.

Material ships a dark-optimised set. For each icon we measure contrast against
the target background:

  * Dark: colours below 3.0:1 are lightened.
  * Light: colours below 3.0:1 are darkened.

Icons needing no change are shared by both themes (base name); adjusted ones
are emitted as file_type_dark_<icon> / file_type_light_<icon>.
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("MATERIAL_ICONS", "/tmp/vscode-material-icon-theme-main/icons")
OUT = os.path.join(ROOT, "icons")
MAP = json.load(open(os.path.join(ROOT, "scripts", "icon-map.json")))
ICONS = sorted(set(MAP["mapping"].values()) | set(MAP["nameMapping"].values()))

DARK_BG = (25, 26, 28)
LIGHT_BG = (255, 255, 255)
MIN_CONTRAST = 3.0


def parse_hex(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def f(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.05) / 1.055) ** 2.4
    return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2])


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


COLOUR_RE = re.compile(r'(fill|stroke)="(#[0-9A-Fa-f]{4,8})"')


def colours(svg):
    out = []
    for _, raw in COLOUR_RE.findall(svg):
        if len(raw) in (4, 7):
            out.append(parse_hex(raw))
    return out


def adjust(svg, bg, lighten):
    def fix(m):
        attr, raw = m.group(1), m.group(2)
        if len(raw) not in (4, 7):
            return m.group(0)
        rgb = parse_hex(raw)
        if contrast(rgb, bg) >= MIN_CONTRAST:
            return m.group(0)
        for _ in range(80):
            if lighten:
                rgb = tuple(min(255, int(v + (255 - v) * 0.12)) for v in rgb)
            else:
                rgb = tuple(int(v * 0.90) for v in rgb)
            if contrast(rgb, bg) >= MIN_CONTRAST:
                break
        return f'{attr}="#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"'
    return COLOUR_RE.sub(fix, svg)


RENDER = r"""
const fs = require('fs');
const { Resvg } = require('@resvg/resvg-js');
const [src, out, spec] = process.argv.slice(2);
for (const pair of JSON.parse(spec)) {
  const [srcName, outName] = pair;
  const svg = fs.readFileSync(`${src}/${srcName}.svg`, 'utf8');
  for (const [size, suffix] of [[16, ''], [32, '@2x'], [48, '@3x']]) {
    fs.writeFileSync(`${out}/${outName}${suffix}.png`,
      new Resvg(svg, { fitTo: { mode: 'width', value: size } }).render().asPng());
  }
}
"""
script = "/tmp/npmtest/_render2.cjs"
open(script, "w").write(RENDER)


def render_batch(pairs):
    subprocess.run(["node", script, SRC, OUT, json.dumps(pairs)], check=True)


variants = {}
pending = []
for icon in ICONS:
    svg = open(os.path.join(SRC, icon + ".svg")).read()
    cols = colours(svg)
    if not cols:
        continue
    dark = min(contrast(c, DARK_BG) for c in cols) < MIN_CONTRAST
    light = min(contrast(c, LIGHT_BG) for c in cols) < MIN_CONTRAST
    tag = {}
    if dark:
        temp = "_tmp_dark_" + icon
        open(os.path.join(SRC, temp + ".svg"), "w").write(adjust(svg, DARK_BG, True))
        pending.append((temp, "file_type_dark_" + icon))
        tag["dark"] = "file_type_dark_" + icon
    if light:
        temp = "_tmp_light_" + icon
        open(os.path.join(SRC, temp + ".svg"), "w").write(adjust(svg, LIGHT_BG, False))
        pending.append((temp, "file_type_light_" + icon))
        tag["light"] = "file_type_light_" + icon
    if tag:
        variants[icon] = tag

# Base icons, rendered once and shared where no variant is needed.
for icon in ICONS:
    pending.append((icon, "file_type_" + icon))
render_batch(pending)

json.dump(variants, open(os.path.join(ROOT, "scripts", "icon-variants.json"), "w"), indent=1)
print("variants:", len(variants))
print("  dark only:", sum(1 for v in variants.values() if "dark" in v))
print("  light only:", sum(1 for v in variants.values() if "light" in v))
