# DEVELOPMENT NOTES

## Build

```bash
python3 scripts/gen_textures.py         # textures/*.png (+ @2x/@3x)
python3 scripts/build_themes.py         # both themes + both icon mappings
python3 scripts/build_color_schemes.py  # both color schemes
```

`build_themes.py` requires Pillow. Icon rasterisation additionally requires
`MATERIAL_ICONS` (a Material Icon Theme 5.40.0 checkout) and `resvg`.

Everything is generated: do not hand-edit a `.sublime-theme` or
`.sublime-color-scheme`, because the next build overwrites it. Change the
palette or the rule list in the script instead.

## Why the two files are generated, not authored

Both flavours share one rule list and one selector table; only the palette
differs. Generating them keeps Dark and Light structurally identical, which
matters because a rule added to one flavour and forgotten in the other shows up
as an inconsistency the eye catches immediately.

## Testing loop used here

1. Copy the repo into
   `~/Library/Application Support/Sublime Text/Packages/JetBrains Islands/`.
2. Set `theme`, `color_scheme` and tab-layout keys in `Preferences`.
3. Kill and relaunch Sublime (`pkill -9 -f MacOS/sublime_text`) — editing the
   theme in place does reload, but a fresh process removes stale-window
   confusion from stacked `open -a` invocations.
4. Capture with `CGWindowListCreateImage` for the specific window number.
5. Sample pixels at known coordinates and crop the region for inspection.

### Gotchas found the hard way

- `open -na "Sublime Text" --args <path>` on top of a running instance stacks
  windows; the oldest window is the one with the theme in it. Clear
  `Local/Session.sublime_session` or keep one window.
- `w.open_file()` opens a *new window* per call. Use the `subl` CLI to get
  multiple files into one window.
- A 1 px texture cannot draw a 1 px edge line inside a control: the nine-slice
  inner margins consume the whole texture and the fill stretches across the
  control. Use a surface-colour difference instead (this is why the sidebar is
  `#1E1F22` rather than the editor colour).
- Settings-gated rules from the base theme are overridden by later
  *unfiltered* rules. Mirror the gate.
- Do not shrink `sidebar_heading`'s `font.size` to hide or compress the
  "FOLDERS" row: `sidebar_tree` inherits that size as its row-height basis and
  every tree row collapses into an overlapping stack. Change `fg` only.

## Verifying a theme actually loaded

Rather than trusting the screenshot, read the runtime state:

```python
import sublime
sublime.load_settings("Preferences.sublime-settings").get("theme")
sublime.ui_info()["color_scheme"]["palette"]["background"]
```

A mismatch between the setting and the sampled window means the change did not
apply, not that the theme is wrong.

## Repository layout

```text
JetBrains Islands {Dark,Light}.sublime-theme   generated UI themes
JetBrains Islands {Dark,Light}.sublime-color-scheme
JetBrains Islands {Dark,Light}.sublime-file-icons
JetBrains Islands.sublime-commands             palette entries
islands_theme.py                               switch commands
textures/                                      generated pill/edge textures
icons/                                         generated third-party PNGs
settings/                                      copy-pasteable settings templates
scripts/                                       generators and icon tooling
docs/                                          design, icon, compatibility, install
```

`scripts/` is not required at runtime; it is excluded when syncing to
`Packages/` in some test passes, and can be excluded from a released
`.sublime-package`.
