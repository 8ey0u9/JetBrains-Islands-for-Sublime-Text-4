# INSTALLATION

## Requirements

- Sublime Text 4, build 4143 or newer (verified on 4215 / macOS).
- macOS is the primary target; the theme also loads on Windows and Linux.

## Install

The package is a single directory that ships both flavours, both color
schemes and both icon mappings. **One install gives you Dark and Light.**

### Option A — Package Control (recommended, once published)

1. Install [Package Control](https://packagecontrol.io/installation).
2. `Cmd+Shift+P` → **Package Control: Add Repository** → paste this repo URL.
3. `Cmd+Shift+P` → **Package Control: Install Package** → **JetBrains Islands**.

### Option B — manual copy

```bash
git clone <repo-url> ~/Library/Application\ Support/Sublime\ Text/Packages/JetBrains\ Islands
```

Or unzip the release into
`~/Library/Application Support/Sublime Text/Packages/JetBrains Islands/`.
Keep the directory name **without** a `.sublime-package` extension so the
source tree stays editable.

### Activate

`Cmd+Shift+P` → **JetBrains Islands: Switch to Dark** (or **Switch to Light**).
The command sets the UI theme, color scheme and icon flavour together.

If you prefer to edit settings by hand, copy the keys from
`settings/JetBrains Islands Dark.sublime-settings` (or the Light variant) into
`Packages/User/Preferences.sublime-settings`. Do not copy the whole file
wholesale: it only lists theme-related keys so that fonts, indentation and
other personal preferences stay yours.

### Follow the system appearance

`Cmd+Shift+P` → **JetBrains Islands: Follow System Appearance** sets
`theme: "auto"` and `color_scheme: "auto"` plus the paired
`light_theme` / `dark_theme` / `light_color_scheme` / `dark_color_scheme`
values, so macOS Dark/Light switching lands on the matching Islands flavour.

## File icons

The `.sublime-file-icons` file whose name matches the active
`.sublime-theme` loads automatically: `JetBrains Islands Dark.sublime-theme`
pairs with `JetBrains Islands Dark.sublime-file-icons`, and the Light pair the
same way. **Do not set `file_icon_theme` yourself** — pinning it to one file
forces the Dark icon variants even in Light mode.

## Uninstall

1. `Cmd+Shift+P` → **JetBrains Islands: Switch to Dark** is *not* an uninstall.
2. Remove the package directory (or **Package Control: Remove Package**).
3. Restore your previous appearance by setting `theme` and `color_scheme`
   back, for example:

```json
{
    "theme": "Default.sublime-theme",
    "color_scheme": "Mariana",
    "file_icon_theme": []
}
```

`file_icon_theme` may be omitted entirely to return to the built-in icons.

## Restoring defaults

All changes this package makes are limited to:

`theme`, `color_scheme`, `light_theme`, `dark_theme`, `light_color_scheme`,
`dark_color_scheme`, `file_tab_style`, `themed_title_bar`,
`highlight_modified_tabs`, `bold_folder_labels`,
`overlay_scroll_bars`, `hide_tab_scrolling_buttons`, `hide_new_tab_button`,
`draw_shadows`, `show_minimap`, `show_sidebar_button`,
and clearing a stale `file_icon_theme`.

Nothing else in `Preferences.sublime-settings`, no project file and no key
binding is touched.

## Build from source

```bash
python3 scripts/gen_textures.py        # pill / chevron / folder textures
python3 scripts/build_themes.py        # .sublime-theme + .sublime-file-icons
python3 scripts/build_color_schemes.py # .sublime-color-scheme
```

`build_themes.py` needs `Pillow`. Icon rasterisation additionally needs
`MATERIAL_ICONS` pointing at a checkout of Material Icon Theme 5.40.0 and
`resvg` (or `svg2png`) on PATH; the generated PNGs are committed so a normal
build does not require them.
