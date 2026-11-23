# FILE ICONS

## Source and licence

File-type icons come from
[Material Icon Theme](https://github.com/material-extensions/vscode-material-icon-theme)
version 5.40.0, MIT licensed. The upstream set ships SVG; this project
rasterises the subset it needs to PNG.

No JetBrains icon artwork is bundled, extracted or redistributed. Islands'
icon *look* is approximated only through the third-party set plus colour
adjustment.

## Mechanics

Sublime Text loads a `.sublime-file-icons` file from the global
`file_icon_theme` setting **and** from any icon theme whose name matches the
currently active `.sublime-theme`. Both sources are applied in order, later
overriding earlier.

This package therefore relies on name matching:

- `JetBrains Islands Dark.sublime-theme` → `JetBrains Islands Dark.sublime-file-icons`
- `JetBrains Islands Light.sublime-theme` → `JetBrains Islands Light.sublime-file-icons`

**Never set `file_icon_theme` manually.** Doing so pins one mapping and forces
its variants in both flavours; the switch plugin clears the key for this
reason.

PNG files live at the package top level inside `icons/` (Sublime also accepts
the top level itself) and are referenced without the `.png` extension.

## Contrast pass

Material's icons are dark-optimised. `scripts/fix_icon_contrast.py` measures
each icon's dominant colour against the target background:

- Dark target `#191A1C`, minimum contrast 3.0:1 → lighten below threshold.
- Light target `#FFFFFF`, minimum contrast 3.0:1 → darken below threshold.

Icons passing on both backgrounds stay as a single shared file. Icons that
needed adjustment are emitted twice:

- `file_type_dark_<name>.png`
- `file_type_light_<name>.png`

`scripts/icon-variants.json` records which icons are dual variants;
`JetBrains Islands Dark.sublime-file-icons` points at the `dark` names and the
Light mapping at the `light` names. 69 of 138 mappings currently differ.

## Sizes

Each icon is emitted at 1× (16×16), `@2x` (32×32) and `@3x` (48×48) so Retina
and 300 % scaling both stay sharp. Sublime picks the variant automatically.

## Coverage

138 extension/name mappings, including:

- languages: TypeScript, JavaScript, React, Vue, Svelte, Python, Go, Rust,
  Java, Kotlin, Swift, C/C++, C#, Ruby, PHP, Dart, Scala, Elixir, Haskell
- markup/data: HTML, CSS, SCSS/Less, JSON, YAML, TOML, XML, Markdown, SQL
- tooling: Dockerfile, Makefile, CMake, Gradle, Maven, Bazel, Terraform
- config: `.gitignore`, `.editorconfig`, `.env`, lockfiles, editor settings

Adding coverage means adding an entry to `scripts/icon-map.json` (extension →
icon) or `nameMapping` (exact filename → icon), re-running
`fix_icon_contrast.py` and then `build_themes.py`, which regenerates both
`.sublime-file-icons` mappings.

## Adding a new icon

```bash
export MATERIAL_ICONS=/path/to/vscode-material-icon-theme-main/icons
python3 scripts/fix_icon_contrast.py   # writes icons/*.png
python3 scripts/build_themes.py         # rewrites both mappings
```

The SVG→PNG step needs `resvg` (or `svg2png`) on PATH. Generated PNGs are
committed, so a normal build does not need that tool.
