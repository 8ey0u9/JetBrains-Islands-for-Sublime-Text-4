# Design and implementation

The runtime uses native Sublime theme resources with zero runtime scripts. Dark and Light share generator rules with independent palettes. Main
UI rules extend `Default.sublime-theme`; inherited controls retain native behavior.
`themes/` holds UI themes and matching file-icon mappings; `schemes/` holds editor
and hidden widget schemes. `settings/` holds widget bindings, user templates and
command-palette entries. Preferences select themes and schemes by their existing
file names, so the directory layout does not change the configured names.

## Theme surfaces and colours

UI tokens live in `scripts/lib/themes.py`. The window, sidebar and editor use
separate surfaces. Light keeps the editor brightest rather than inverting Dark.

| Token | Dark | Light | Used by |
|---|---|---|---|
| `jb_window_bg` | `#26282C` | `#E9EAEE` | title bar, status bar, pane gap |
| `jb_toolwindow_bg` | `#1E1F22` | `#F7F8FA` | sidebar container |
| `jb_panel_bg` | `#191A1C` | `#FFFFFF` | find / replace / console panel |
| `jb_tab_bar_bg` | `#191A1C` | `#FFFFFF` | tab strip (editor colour) |
| `jb_popup_bg` | `#26282C` | `#FFFFFF` | quick panel, completion, documentation |
| `jb_popup_border` | `#33353B` | `#D1D3D9` | popup hairline |
| `jb_tooltip_bg` | `#33353B` | `#FFFFFF` | native tooltip fill |
| `jb_tooltip_border` | `#33353B` | `#D1D3D9` | native tooltip outline |
| `jb_status_bg` | `#26282C` | `#E9EAEE` | status bar |
| `jb_tab_active_bg` | `#233558` | `#E3EBFE` | selected tab fill |
| `jb_tab_active_border` | `#2E4D89` | `#A7C5FF` | selected tab outline |
| `jb_tab_inactive_bg` | `#26282C` | `#E9EAEE` | inactive tab fill |
| `jb_tab_inactive_border` | `#40434A` | `#D1D3D9` | inactive tab outline |
| `jb_row_selected` | `#2A4371` | `#D0DFFE` | tree/list/completion selection |
| `jb_hover_bg` | white @ 9 % | black @ 7 % | hover fill |
| `jb_border` | `#33353B` | `#E9EAEE` | subtle separators |
| `jb_border_strong` | `#40434A` | `#D1D3D9` | control outlines |
| `jb_text` | `#D1D3D9` | `#080808` | primary text |
| `jb_text_dim` | `#9FA2A8` | `#5F6269` | secondary text, icons |
| `jb_text_faint` | `#6F737A` | `#73767C` | hints, path labels |
| `jb_accent` | `#3871E1` | `#3871E1` | focus, links, toggle-on |
| `jb_accent_soft` | `#2E4D89` | `#BDD3FF` | pressed fill |
| `jb_link` | `#71A1FE` | `#2F5EB9` | match highlight text |
| `jb_input_bg` | `#191A1C` | `#FFFFFF` | text field fill |
| `jb_input_border` | `#40434A` | `#D1D3D9` | field/button outline |
| `jb_scroll_thumb` | `#808080` | `#808080` | overlay puck |
| `jb_error` | `#F57E84` | `#C54E58` | error feedback |
| `jb_warning` | `#D59637` | `#A56906` | warning feedback |
| `jb_success` | `#6DB083` | `#338555` | success feedback |

Selected tabs use rounded fill/outline textures. `file_tab_style: "square"`
selects square textures; `"angled"` retains the inherited shape. Dirty tabs keep
their marker. Tree rows, quick panels and completion rows use selection pills.
Native tooltips have their own surface tokens.

## Editor and input widgets

`scripts/lib/schemes.py` defines the editor palette and shared syntax selectors.

| | Dark | Light |
|---|---|---|
| background | `#191A1C` | `#FFFFFF` |
| foreground | `#BCBEC4` | `#080808` |
| keyword | `#CF8E6D` | `#0033B3` |
| string | `#6AAB73` | `#067D17` |
| number | `#2AACB8` | `#1750EB` |
| comment | `#7A7E85` | `#8C8C8C` |
| function | `#56A8F5` | `#00627A` |
| caret | `#CED0D6` | `#000000` |
| selection | `#2A4371` | `#A6D2FF` |
| line highlight | `#1F2024` | `#F5F8FE` |
| gutter | `#191A1C` | `#FFFFFF` |
| gutter text | `#4B5059` | `#AEB3C2` |
| find highlight | `#114957` | `#FCD47E` |

Theme-specific `Widget - JetBrains Islands {Dark,Light}.sublime-settings` files
bind matching hidden schemes. Native picker placeholders use the widget
scheme's `rulers` colour independently of list labels and editor rulers.

| Token | Dark | Light |
|---|---|---|
| `widget_fg` | `#D1D3D9` | `#080808` |
| `widget_placeholder` (`rulers`, `invisibles`) | `#9FA2A8` | `#5F6269` |
| background (editor surface) | `#191A1C` | `#FFFFFF` |

Placeholder contrast exceeds 4.5:1 in both variants. Editor rulers retain their
subtle guide colour. Widget bindings only set `color_scheme`, preserving user
fonts and native regex syntax. Hidden schemes stay out of the editor scheme
picker. Selection colours follow each editor palette.

## Documentation popups and folding

`styles/popup.css` is the source template; palette tokens come from
`scripts/lib/schemes.py`. The build expands it into editor schemes and
`styles/popup-{dark,light}.css`. Edit the template and regenerate.

| Surface | Dark | Light |
|---|---|---|
| Documentation | `#26282C` | `#FFFFFF` |
| Documentation text | `#D1D3D9` | `#000000` |
| Secondary text | `#9FA2A8` | `#5F6269` |
| Links | `#71A1FE` | `#2F5EB9` |
| Separators | `#33353B` | `#E9EAEE` |
| Action strip | `#26282C` | `#F7F8F9` |
| Error feedback | `#56272B` | `#FFF6F5` |
| Warning feedback | `#44321D` | `#FFF6E9` |

The mdpopups adapter applies after provider CSS for Islands popup contexts and
includes `Packages/User/mdpopups.css` last. Switch commands preserve an explicit
custom hook. Other schemes, phantoms and HTML sheets retain provider styles;
explicit `phantom_css` prevents popup styling leaking into inline hints.

The adapter covers headings, paragraphs, lists, quotes, inline/fenced code,
`div.highlight`, diagnostics, copy links, action strips and signature help.
Provider-generated syntax spans, active-parameter emphasis and wrapper spacers
are preserved. Text, capabilities, navigation and async updates remain owned by
Sublime/LSP; no callbacks are intercepted or LSP files patched. The validator
rejects `:hover` and `!important` in this minihtml stylesheet.

Popup size/placement/dismissal remain native. LSP's optional
`popup_max_characters_width` and `popup_max_characters_height` are unchanged.
The minimum Sublime build is 4170 for wrapped preformatted content.

Folding uses the sidebar's right/down chevrons with expanded and hover states.
Sublime determines fold ranges, collapsed-marker behavior and shortcuts.
`fold_buttons`, `fade_fold_buttons` and `fold_style` retain native meanings.
The colour scheme supplies `fold_marker`; no separate fold-marker fill is emulated.

## File icons and textures

`scripts/icon-map.json` contains extension and exact-filename mappings. The
same-named `.sublime-file-icons` file follows the active theme automatically.
Unmapped files retain the inherited generic icon.

The 42 icon types produce 84 Dark/Light variant records and 252 PNGs at
16/32/48 pixels. The renderer starts from SVG for every size, then adds source,
license and modification metadata. Sublime loads PNGs; it does not render those
source SVGs as theme textures. The sources and evidence live in
[the asset manifest](../icons/upstream/manifest.json).

Original pill, folder and chevron textures are generated as white/alpha images
and tinted by theme layers. Each density is downsampled from a supersampled
master. Retain 1x, 2x and 3x assets together.

See the [licensing guide](LICENSING.md) for outstanding icon/publication decisions.

## Native dependencies and constraints

| Dependency | Implementation constraint |
|---|---|
| `Default.sublime-theme` | inherited rules fill controls not overridden here |
| Default `tint_index: 0` | inputs and completion override it to `-1` to preserve their own fills |
| Settings-gated tab buttons | mirror the gates; an unconditional later rule can make hidden buttons reappear |
| `Theme - Default/common/*.png` | close/dirty/navigation/sidebar/branch glyph paths must remain valid |
| Theme-specific Widget settings | preserve native regex settings and user typography |
| Inactive-sheet dimming | surface blends prevent unfocused fields becoming excessively dark |

`sidebar_heading` font size affects tree row height; do not shrink it to hide
headings. A 1px texture cannot serve as a nine-slice 1px border if its inner
margins consume it. Preserve the existing surface-based sidebar separation.
The recommended `draw_shadows: false` removes the editor-edge gradient while
respecting explicit user preferences. Minimap viewport settings affect the
viewport, not the editor/minimap separator.

Native title bars vary by platform. Windows/Linux remain unverified. Sublime
has no theme controls for a tool-window stripe, tab file icons, breadcrumb bar
or synthetic input-focus ring. After Sublime updates, check UI states such as
tab buttons, field fills and Light popup borders. Official format references:
[themes](https://www.sublimetext.com/docs/themes.html) and
[settings](https://www.sublimetext.com/docs/settings.html).
