# THIRD-PARTY NOTICES

JetBrains Islands for Sublime Text 4 bundles third-party file-type icons.
No JetBrains-proprietary artwork (SVG, PNG, font or icon font) is included or
redistributed. The Islands UI look is reproduced only through the native
Sublime Text theme mechanism.

## Bundled assets

| Asset | Source | Version | License | Modifications | Notice requirement |
|---|---|---|---|---|---|
| File type PNG icons (`icons/*.png`, `@2x`, `@3x`) | [Material Icon Theme](https://github.com/material-extensions/vscode-material-icon-theme) | 5.40.0 | MIT | Re-rasterised to PNG at 16/32/48 px; colour-adjusted per flavour to reach ≥3:1 contrast against the Islands Dark `#191A1C` and Light `#FFFFFF` backgrounds (`scripts/fix_icon_contrast.py`) | MIT copyright notice (below) |
| Folder / chevron / pill textures (`textures/*.png`) | Original to this project | — | MIT (same as this project) | — | — |

## MIT License (Material Icon Theme)

```
The MIT License (MIT)
Copyright (c) 2025 Material Extensions

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Referenced (not bundled)

- IntelliJ IDEA Islands UI — visual reference only. JetBrains, IntelliJ and the
  IntelliJ IDEA logo are trademarks of JetBrains s.r.o. This project is not
  affiliated with or endorsed by JetBrains.
- Sublime Text and its `Theme - Default` package textures are referenced by
  path at runtime (for example `Theme - Default/common/tab_close.png`). Sublime
  Text ships those textures; this package does not redistribute them.
