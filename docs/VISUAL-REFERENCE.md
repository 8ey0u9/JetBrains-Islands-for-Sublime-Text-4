# VISUAL REFERENCE & ACCEPTANCE

Reference target: IntelliJ IDEA 2025.2+ Islands UI. Verification environment:
Sublime Text 4 build 4215 on macOS 25.6 (Darwin), Retina 2× display, window
800×632 logical points.

## How the screenshots were taken

Each acceptance pass captured the live window with `CGWindowListCreateImage`
(no simulator, no mock), then sampled pixels and inspected crops. The numbers
below are measured from those captures, not estimated.

## Dark — measured

| Region | Expected | Measured |
|---|---|---|
| Title bar | `jb_window_bg` `#26282C` | `#26282C` |
| Tab strip background | editor colour `#191A1C` | `#191A1C` |
| Selected tab pill fill | `#233558` | `#233558` |
| Selected tab pill border | `#2E4D89` | `#2A4272`–`#2E4D89` (antialiased edge) |
| Editor background | `#191A1C` | `#191A1C` |
| Sidebar | `#1E1F22` | `#1E1F22` |
| Status bar | `#26282C` | `#26282C` |
| Quick panel fill | `#26282C` | `#26282C` |
| Quick panel selected row | `#2A4371` | `#2A4371` |
| Text field fill | `#191A1C` | `#191A1C` |
| Gutter text | `#4B5059` | `#4B5059` |

## Light — measured

| Region | Expected | Measured |
|---|---|---|
| Title bar | `#E9EAEE` | `#E9EAEE` |
| Tab strip background | `#FFFFFF` | `#FFFFFF` |
| Selected tab pill fill | `#E3EBFE` | `#E3EBFE` |
| Editor background | `#FFFFFF` | `#FFFFFF` |
| Sidebar | `#F7F8FA` | `#F7F8FA` |
| Status bar | `#E9EAEE` | `#E9EAEE` |
| Quick panel fill | `#FFFFFF` | `#FFFFFF` |
| Quick panel border | `#D1D3D9` | `#E2E3E7` (1 px antialiased edge) |
| Text field fill | `#FFFFFF` | `#FFFFFF` |
| Find panel fill | `#F7F8FA` | `#F7F8FA` |
| Gutter text | `#AEB3C2` | `#AEB3C2` |

## Scenarios checked

- [x] Main window: island gap, tool window, editor, status bar layers
- [x] Tab strip: pill tab, inactive flat tabs, hover fill, close button on
      selected only, no scroll arrows, no new-tab button, no overflow dropdown
- [x] Sidebar: folder/file icons, indentation, selection pill
- [x] Editor: Dark and Light syntax colours against the real palette
- [x] Command palette: panel fill, selected row pill, key-hint colour
- [x] Find panel: text field, toggle buttons, action buttons
- [x] Auto complete: popup fill, selected row pill
- [x] Status bar: height, background, label colour
- [x] Multi-window: two windows open at once sampled independently — both
      `title #26282C`, `editor #191A1C`, `status #26282C`
- [x] One-command switch: Dark → Light changes theme, scheme, and drops the
      pinned `file_icon_theme` in the same save (verified by reading back
      `file_icon_theme: []` and sampling the resulting window)
- [x] Packaged install: `JetBrains Islands.sublime-package` placed in
      `Installed Packages/` with no `Packages/JetBrains Islands/` directory
      renders identically to the source-tree install
- [x] Full screen: `toggle_full_screen` captured both flavours at 2560×1440.
      Title bar disappears, tab strip meets the top edge, sidebar
      `#1E1F22` / `#F7F8FA`, editor `#191A1C` / `#FFFFFF`, status bar
      `#26282C` / `#E9EAEE`. Command palette in full screen: panel
      `#26282C` / `#FFFFFF`, input field `#191A1C` / `#FFFFFF`, selected row
      `#2A4371` / `#D0DFFE`.

## Selected tab — measured against the Islands reference

Reference: the Islands documentation asset
`plugins.jetbrains.com/docs/intellij/images/islands_tabs.png` (2x asset, so
pixel values are halved below).

| Property | Official Islands | This theme | Status |
|---|---|---|---|
| pill fill | `#233558` | `#233558` | exact |
| pill border | `#2E4D89` | `#2E4D89` | exact |
| label colour | `#D1D3D9` | `#D1D3D9` | exact |
| pill height | 28.0 pt | 27.5 pt | 0.5 pt |
| pill corner radius | 5.0 pt | 5.0 pt | exact |
| left edge → label glyph | 7.0 pt | 8.5 pt | 1.5 pt |
| right edge → close glyph | 10.5 pt | 8.0 pt | 2.5 pt |
| left/right symmetry | — | 8.5 vs 8.0 pt (0.5 pt) | symmetric |
| pill width (single tab) | 141.0 pt (with icon) | 86.0 pt (no icon) | see below |

Light flavour equivalent: fill `#E3EBFE`, border `#A7C5FF`, both measured.

### Known limitation: no file icon in tabs

`islands_tabs.png` shows the icon → label → close order. Sublime Text exposes
only `tab_control`, `tab_label` and `tab_close_button` for tabs; there is no
icon element, so the icon segment (7 pt + icon + 8.5 pt ≈ 30 pt) cannot be
reproduced. That is the whole 141 vs 86 pt width difference. Padding was
re-calibrated to the no-icon case so the pill reads balanced rather than
stretched.

## Editor / minimap boundary

| | Value |
|---|---|
| With `draw_shadows: true` (stock behaviour) | 15 px gradient, `#191A1C` → `#0D0D0E` |
| With `draw_shadows: false` (shipped setting) | hard boundary at x=1512, both sides `#191A1C` |
| Glyph brightness at the boundary | unchanged, peak `#BCBEC4` |
| Stock `Default Dark` for comparison | same 15 px gradient, `#FFFFFF` → `#939393` |

Decision: `draw_shadows: false`, because the gradient darkens the editor edge
instead of separating it, and Islands draws no shadow there.

## Deliberate divergences from IntelliJ

- Tab corner radius and pill height are closing values, not IntelliJ's exact
  arc geometry; Sublime exposes `tab_height` but not the arc parameters.
- The overflow dropdown button is invisible rather than absent: Sublime has no
  setting to remove it, so it is collapsed to zero content margin.
- IntelliJ's gutter separator and indent guides are drawn by Sublime's color
  scheme, not by the theme, so their colour comes from `guide` /
  `active_guide` tokens rather than from theme rules.
