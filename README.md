---
title: JetBrains Islands
description: An independent Islands-inspired theme for Sublime Text 4, with Dark and Light variants.
author: beyoug
---

# JetBrains Islands for Sublime Text 4

An independent Sublime Text 4 theme inspired by IntelliJ IDEA's Islands
interface. One install includes Dark and Light themes, matching editor and
input-widget colour schemes, and file icons at 1x, 2x and 3x resolution.

**Pre-release:** public distribution is pending review of 12 icon variant
licenses and the project/package name. See [Licensing and publication](docs/LICENSING.md).
This project is not affiliated with, endorsed by or sponsored by JetBrains or Sublime HQ.

## Install

Requires Sublime Text 4 build 4170 or newer. macOS is the primary development
platform; Windows and Linux remain unverified. No Node.js, Python or IDE
installation is needed to use an already-built theme package.

1. Obtain the package archive from `dist/`, or build it using `python3 scripts/manage.py build`.
2. Open **Preferences → Browse Packages**. The `Installed Packages` directory
   is beside the `Packages` directory that opens.
3. Copy `JetBrains Islands.sublime-package` into `Installed Packages`.

If `Packages/JetBrains Islands/` already exists, back it up and move it outside
`Packages`: unpacked resources override the archive. For an editable install,
unzip the archive into `Packages/JetBrains Islands/` instead. Keep that folder
name because theme resources refer to it.

## Activate and configure

Use Sublime Text's native theme selection:

1. Open the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux).
2. Run **UI: Select Theme** and choose **JetBrains Islands Dark** (or Light).
3. Run **UI: Select Color Scheme** and choose **JetBrains Islands Dark** (or Light).

Or configure them directly in your `Preferences.sublime-settings`:

### Dark Appearance (Default)
```json
{
    "theme": "JetBrains Islands Dark.sublime-theme",
    "color_scheme": "JetBrains Islands Dark.sublime-color-scheme"
}
```

### Follow System Appearance (Auto Dark/Light)
```json
{
    "theme": "auto",
    "color_scheme": "auto",
    "dark_theme": "JetBrains Islands Dark.sublime-theme",
    "light_theme": "JetBrains Islands Light.sublime-theme",
    "dark_color_scheme": "JetBrains Islands Dark.sublime-color-scheme",
    "light_color_scheme": "JetBrains Islands Light.sublime-color-scheme"
}
```

### Reference and Recommended Tweaks
Open the command palette and run:
- **JetBrains Islands: 设置说明（中文）**: Opens the annotated settings template beside your preferences using Sublime's native settings editor. Copy only the keys you need; templates do not load automatically.

You can also opt into Islands recommended tweaks (such as compact tab bar buttons and modified tab highlights):
```json
{
    "highlight_modified_tabs": true,
    "hide_new_tab_button": true,
    "hide_tab_scrolling_buttons": true,
    "draw_shadows": false,
    "overlay_scroll_bars": "enabled"
}
```

Fonts, editor font size, indentation, folding preferences, key bindings and
project files remain yours. The [Chinese settings reference](docs/SETTINGS.zh-CN.md)
explains the managed values and optional switches.

File icons load automatically by matching the active theme's name. The theme contains
42 file-icon types covering 138 extension/name mappings per variant.

## Popups and native behavior

The theme styles documentation, diagnostics, completion and native folding
controls. Actual signatures, text, links, Quick Fixes and navigation come from
Sublime and installed providers such as LSP; those packages are not patched.

If you use mdpopups / LSP, you can reference the styled popup sheet in your settings:
```json
{
    "mdpopups.user_css": "Packages/JetBrains Islands/styles/mdpopups.css"
}
```
Existing User CSS (`Packages/User/mdpopups.css`) is composed and included last.

When upgrading from a version with theme files at the package root, replace the
old archive or unpacked folder, then restart Sublime to refresh cached resource
paths. If cached popups retain the previous style, save work and restart Sublime normally.

## Limits

- Native control layout differs from IntelliJ: no tool-window stripe, breadcrumb
  bar, file icons inside tabs or added gap between sidebar and editor.
- Theme/input textures use PNG. Source SVGs are rendered during development;
  Sublime loads the prebuilt density variants.
- Native title-bar styling depends on the platform. The minimap is shown/hidden
  through the View menu; the theme does not install a separate toggle.
- Popup placement, size limits, dismissal and available actions belong to
  Sublime and providers. The theme does not add browser-style popup controls.

## Uninstall

1. Restore your previous `theme` and `color_scheme`. If you use `auto`, restore
   the `light_*` / `dark_*` pairs too.
2. Remove or restore `mdpopups.user_css` if it points to
   `Packages/JetBrains Islands/styles/mdpopups.css`.
3. Remove the installed archive or unpacked `Packages/JetBrains Islands/` folder.
   Layout preferences already saved remain until you change or remove them.

## Documentation and development

| Need | Read |
|---|---|
| Understand palettes, widgets, popups and icon sources | [Design](docs/DESIGN.md) |
| Look up settings in Chinese | [Settings](docs/SETTINGS.zh-CN.md) |
| Review publication requirements | [Licensing and publication](docs/LICENSING.md) |

### Development commands

```bash
# Build theme resources and generate the package
python3 scripts/manage.py build

# Run all regression tests
python3 scripts/manage.py test

# Validate resources and archive integrity
python3 scripts/manage.py check
```

## Credits and license

Original code, documentation and textures: [MIT](LICENSE). Third-party icons
retain their upstream rights; see [Third-party licensing](docs/LICENSING.md),
[NOTICE](NOTICE), the [Apache-2.0 text](LICENSES/Apache-2.0.txt) and
[asset manifest](icons/upstream/manifest.json).

JetBrains and IntelliJ IDEA are trademarks of [JetBrains s.r.o.](https://www.jetbrains.com/).
Copyright licenses do not authorize use of those marks as this project's branding.
