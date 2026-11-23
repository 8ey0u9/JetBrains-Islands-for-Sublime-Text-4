# COLOR SYSTEM

All colours are generated from two palettes in `scripts/build_themes.py`
(`DARK`, `LIGHT`) and two editor palettes in `scripts/build_color_schemes.py`.
Nothing is chosen inline in a rule.

## UI tokens

| Token | Dark | Light | Used by |
|---|---|---|---|
| `jb_window_bg` | `#26282C` | `#E9EAEE` | title bar, status bar, pane gap |
| `jb_toolwindow_bg` | `#1E1F22` | `#F7F8FA` | sidebar container |
| `jb_panel_bg` | `#191A1C` | `#FFFFFF` | find / replace / console panel |
| `jb_tab_bar_bg` | `#191A1C` | `#FFFFFF` | tab strip (editor colour) |
| `jb_popup_bg` | `#26282C` | `#FFFFFF` | quick panel, completion, tooltip |
| `jb_popup_border` | `#33353B` | `#D1D3D9` | popup hairline |
| `jb_status_bg` | `#26282C` | `#E9EAEE` | status bar |
| `jb_tab_active_bg` | `#233558` | `#E3EBFE` | selected tab fill |
| `jb_tab_active_border` | `#2E4D89` | `#A7C5FF` | selected tab outline |
| `jb_tab_inactive_bg` | `#26282C` | `#E9EAEE` | inactive tab fill |
| `jb_tab_inactive_border` | `#40434A` | `#D1D3D9` | inactive tab outline |
| `jb_row_selected` | `#2A4371` | `#D0DFFE` | tree/list/completion selection |
| `jb_hover_bg` | white @ 9 % | black @ 7 % | hover fill |
| `jb_border` | `#33353B` | `#D1D3D9` | subtle separators |
| `jb_border_strong` | `#40434A` | `#D1D3D9` | control outlines |
| `jb_text` | `#D1D3D9` | `#080808` | primary text |
| `jb_text_dim` | `#9FA2A8` | `#5F6269` | secondary text, icons |
| `jb_text_faint` | `#6F737A` | `#9FA2A8` | hints, path labels |
| `jb_accent` | `#3871E1` | `#3871E1` | focus, links, toggle-on |
| `jb_accent_soft` | `#2E4D89` | `#BDD3FF` | pressed fill |
| `jb_link` | `#71A1FE` | `#2F5EB9` | match highlight text |
| `jb_input_bg` | `#191A1C` | `#FFFFFF` | text field fill |
| `jb_input_border` | `#40434A` | `#D1D3D9` | field/button outline |
| `jb_input_focus_border` | `#3871E1` | `#3871E1` | focused outline |
| `jb_scroll_thumb` | `#808080` | `#808080` | overlay puck |
| `jb_error` | `#F57E84` | `#C54E58` | error feedback |
| `jb_warning` | `#D59637` | `#A56906` | warning feedback |
| `jb_success` | `#6DB083` | `#338555` | success feedback |

### Why Light is not an inversion

Light keeps a three-step ladder — editor `#FFFFFF`, tool window `#F7F8FA`,
window chrome `#E9EAEE` — so the brightest plane is still "where you type"
and the chrome recedes. Inverting Dark's values would make the sidebar
brighter than the editor and the accents muddy.

## Editor tokens

Full tables in `docs/DESIGN.md`; the source of truth is
`scripts/build_color_schemes.py`. Notable values:

| | Dark | Light |
|---|---|---|
| background | `#191A1C` | `#FFFFFF` |
| foreground | `#BCBEC4` | `#080808` |
| caret | `#CED0D6` | `#000000` |
| selection | `#2A4371` | `#A6D2FF` |
| line highlight | `#1F2024` | `#F5F8FE` |
| gutter text | `#4B5059` | `#AEB3C2` |
| find highlight | `#114957` | scheme equivalent |

## Contrast rules applied

- Body text against its own surface: `#D1D3D9` on `#26282C` (≈9.3:1),
  `#080808` on `#FFFFFF` (≈19.7:1).
- Secondary text `#9FA2A8` on `#26282C` (≈4.8:1) and `#5F6269` on `#F7F8FA`
  (≈5.7:1) both clear 4.5:1.
- Faint text `#6F737A` on `#26282C` is ≈3.3:1 — reserved for hints, matching
  IntelliJ's own faint label contrast.
- Selection fills are deliberately lower-contrast than text: `#2A4371` on
  `#191A1C` and `#D0DFFE` on `#F7F8FA`, with text re-set to `jb_text` on top.
- File icons are contrast-corrected to ≥3:1 against both backgrounds by
  `scripts/fix_icon_contrast.py`.

## States covered

Each interactive surface has idle, hover, selected, and (where Sublime exposes
it) pressed/disabled rules:

| Surface | idle | hover | selected |
|---|---|---|---|
| tree row | transparent | `jb_hover_bg` pill | `jb_row_selected` pill |
| tab | `jb_tab_bar_bg` | `jb_hover_bg` | `jb_tab_active_bg` + border |
| quick panel row | transparent | n/a | `jb_row_selected` pill |
| icon button | transparent | `jb_hover_bg` pill | `jb_accent_soft` pill |
| button | transparent + outline | `jb_hover_bg` | `jb_accent_soft` + accent outline |
| text field | `jb_input_bg` + `jb_input_border` | n/a | focus border `jb_input_focus_border` |

`disabled` states reuse the idle colour at reduced opacity (buttons 0.5,
tab close 0.7) rather than introducing a new token, so a disabled control never
reads as a different design.
