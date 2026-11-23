# DESIGN

## What was built

A native Sublime Text 4 theme package that reproduces the IntelliJ IDEA
Islands UI, with Dark and Light in one install. The package does not patch the
application, inject code into `Sublime Text.app`, or alter its signature: it
uses only the documented `.sublime-theme`, `.sublime-color-scheme` and
`.sublime-file-icons` formats, plus a small `ApplicationCommand` plugin for
switching.

## Design tokens

Every colour lives in `scripts/build_themes.py` as a `jb_*` palette entry, and
in `scripts/build_color_schemes.py` for editor tokens. Both flavours are
generated from the same structure, so a rule never has to be written twice.

| Token | Dark | Light | Role |
|---|---|---|---|
| `jb_window_bg` | `#26282C` | `#E9EAEE` | island gap, title bar, status bar |
| `jb_toolwindow_bg` | `#1E1F22` | `#F7F8FA` | sidebar and tool windows |
| `jb_tab_bar_bg` | `#191A1C` | `#FFFFFF` | editor tab strip |
| `jb_panel_bg` | `#191A1C` | `#FFFFFF` | find / replace / output panels |
| `jb_popup_bg` | `#26282C` | `#FFFFFF` | quick panel, completion, tooltip |
| `jb_status_bg` | `#26282C` | `#E9EAEE` | status bar |
| `jb_tab_active_bg` | `#233558` | `#E3EBFE` | selected tab pill |
| `jb_tab_active_border` | `#2E4D89` | `#A7C5FF` | selected tab pill outline |
| `jb_row_selected` | `#2A4371` | `#D0DFFE` | tree / list selection |
| `jb_text` | `#D1D3D9` | `#080808` | primary text |
| `jb_text_dim` | `#9FA2A8` | `#5F6269` | secondary text |
| `jb_accent` | `#3871E1` | `#3871E1` | focus ring, links, toggle-on |
| `jb_input_bg` | `#191A1C` | `#FFFFFF` | text fields |
| `jb_input_border` | `#40434A` | `#D1D3D9` | field and button outlines |
| `jb_scroll_thumb` | `#808080` | `#808080` | overlay scroll puck |

Light is an independent design, not an inversion of Dark: surfaces sit in a
`#FFFFFF → #F7F8FA → #E9EAEE` ladder so the editor stays the brightest plane
and the window chrome the darkest, which is how Islands reads on a light
display.

## Theme structure

`JetBrains Islands {Dark,Light}.sublime-theme` extend `Default.sublime-theme`
and only override variables plus the rules that carry the Islands look. This is
why keyboard navigation, hover semantics, scroll behaviour and every control
not named below keep working exactly as in the stock theme.

Layers used per surface:

- **Window gap** — `title_bar` background `jb_window_bg`; the 2 px
  `grid_layout_control` border uses the same colour, so split panes read as
  separate islands rather than as boxes with a line between them.
- **Tool window** — `sidebar_container` on `jb_toolwindow_bg`. Since that
  surface differs from the editor, the split reads without adding a divider
  line (a stretched 1 px texture would smear into a band; verified and rejected
  during visual acceptance).
- **Tab strip** — `tabset_control` on `jb_tab_bar_bg`, i.e. the editor colour,
  matching IntelliJ's `EditorTabs.background`.
- **Selected tab** — a rounded pill texture (`textures/tab_pill.png`) plus a
  1 px outline layer (`tab_pill_border.png`), tinted per flavour. Inactive
  tabs are flat; hover raises a translucent fill. The tab close button is
  hidden on inactive tabs and appears on hover or selected. Label padding is
  `[12, 5, 9, 5]` and the close glyph adds `[9, 9, 5, 9]`, calibrated against
  IntelliJ's own Islands tab asset so the pill is optically symmetric: 8.5 pt
  from the pill edge to the first glyph on the left, 8.0 pt to the close
  glyph on the right (measured on Retina captures in both flavours). The reference also shows a
  file-type icon before the label, which Sublime's tab classes cannot express
  (only `tab_control`, `tab_label`, `tab_close_button` exist), so the pill is
  narrower than IntelliJ's and the padding is balanced for the icon-less case.
- **Quick panel / completion / tooltip** — `overlay_control`,
  `quick_panel`, `auto_complete`, `popup_control` and `tool_tip_control` all
  sit on `jb_popup_bg` with `jb_popup_border` outlines. In Light this border is
  required: a white panel over a white editor is otherwise invisible.
- **Text inputs** — `input_pill.png` fill plus `input_pill_border.png`
  outline, rounded like the Islands search field.
- **Selection** — `row_pill.png` nine-slice on tree rows, quick panel rows and
  completion rows.

### Two bugs worth remembering

1. `text_line_control` and `auto_complete` inherit `tint_index: 0` from
   `Default.sublime-theme`. That re-tints layer 0 with the color scheme
   background and crushed the input fill to `#0E0E10` (measured). The rules
   therefore set `tint_index: -1`.
2. `Default.sublime-theme` hides the tab scroll arrows and the new-tab button
   with *settings-gated* `content_margin: 0` rules. A later unfiltered rule
   silently resurrects them, so every tab-strip button rule in this package
   mirrors the matching `settings` gate, and the overflow dropdown is
   collapsed to zero width because Islands has no equivalent.
3. `inactive_sheet_dimming: true` makes `Default` apply
   `text_widget_dark_modifier` (`l(-5%)`) to an unfocused input field, which
   crushed the Islands input fill to `#0D0D0F` on a `#26282C` popup. The
   setting is therefore not enabled by this package.

### The editor/minimap boundary

Sublime draws a 15 px dark gradient between the editor and the minimap
whenever `draw_shadows` is on. Under Islands Dark it runs from `#191A1C` down
to `#0D0D0E`, i.e. it *darkens* the edge of the editor instead of separating
two surfaces, and the gradient's hard start reads as a smear rather than as a
border.

The stock `Default Dark` theme shows the same gradient (`#FFFFFF` →
`#939393`), so it is Sublime behaviour, not something this package introduced.
It cannot be replaced by a hairline: `minimap_control` accepts only
`viewport_color` and `viewport_opacity` — probe rules using
`background_modifier`, `layer0.tint` and a 1 px texture were all ignored, and
`Minimap.sublime-settings`'s `rulers` draws inside the thumbnail, not at its
edge.

Islands has no shadow in this position, so the package sets
`draw_shadows: false`. The minimap then meets the editor edge-to-edge in the
same colour, which is what IntelliJ does too. Text contrast is unaffected
either way (glyphs near the edge stay at full `#BCBEC4`).

## Color schemes

`JetBrains Islands {Dark,Light}.sublime-color-scheme` carry the Islands editor
palette, not a generic JetBrains scheme:

| | Dark | Light |
|---|---|---|
| background | `#191A1C` | `#FFFFFF` |
| foreground | `#BCBEC4` | `#080808` |
| keyword | `#CF8E6D` | `#0033B3` |
| string | `#6AAB73` | `#067D17` |
| number | `#2AACB8` | `#1750EB` |
| comment | `#7A7E85` | `#8C8C8C` |
| function | `#56A8F5` | `#00627A` |
| selection | `#2A4371` | `#A6D2FF` |
| gutter | `#191A1C` | `#FFFFFF` |
| gutter text | `#4B5059` | `#AEB3C2` |
| caret | `#CED0D6` | `#000000` |

The syntax rules are generated from IntelliJ attribute names so both flavours
share one selector table; see `scripts/build_color_schemes.py`.

## File icons

`.sublime-file-icons` files are named after their theme, so Sublime loads the
matching mapping automatically and no `file_icon_theme` setting is needed. The
Dark mapping points at `file_type_dark_*` variants and the Light mapping at
`file_type_light_*` for the ~69 icons whose source colour failed the 3:1
contrast target on either background; the rest are shared.

## What is deliberately not attempted

- No 1:1 pixel match of IntelliJ's native layout engine. Sublime's layout and
  control inventory differ, so the acceptance bar is structure, colour
  hierarchy and control proportion (see `docs/VISUAL-REFERENCE.md`).
- No injected code, no patched `sublime_text` binary, no font substitution.
