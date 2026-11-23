# COMPATIBILITY

## Verified

| Item | Value |
|---|---|
| Sublime Text build | 4215 |
| macOS | 25.6 (Darwin, Apple silicon) |
| Display | Retina 2× |
| Package format | plain directory in `Packages/` |

The theme targets Sublime Text 4 (4143+). Everything it relies on is
documented at <https://www.sublimetext.com/docs/themes.html> and
<https://www.sublimetext.com/docs/settings.html>.

## Load-bearing dependencies on the stock theme

The package extends `Default.sublime-theme`. Several visual outcomes depend on
properties *this package does not define*:

| Relied on | Where it comes from | Consequence if it changes |
|---|---|---|
| `extends: Default.sublime-theme` | stock theme | rules fill gaps; without it the UI loses unthemed controls |
| `tint_index: 0` on `text_line_control`, `auto_complete` | stock theme | the package overrides it to `-1`; if the stock value changes, check inputs and popups for re-tinting |
| settings-gated `content_margin: 0` for tab scroll arrows / new-tab button | stock theme | the package mirrors the gates; if the stock gate is renamed, buttons reappear |
| `Theme - Default/common/*.png` textures (tab close, panel close, folder chevrons, scroll, branch) | stock theme | referenced by path; a rename breaks those glyphs |
| Widget color schemes (`Widget - Default*.hidden-color-scheme`) | stock theme | drives find-panel text and popup text colours |

After a Sublime Text update, re-run the visual pass in
`docs/VISUAL-REFERENCE.md`. Candidate regressions to look at first:
tab-strip buttons reappearing, input fields turning near-black, popup borders
vanishing on light backgrounds.

## Settings the package sets

`theme`, `color_scheme`, `light_theme`, `dark_theme`, `light_color_scheme`,
`dark_color_scheme`, `file_tab_style`, `themed_title_bar`,
`highlight_modified_tabs`, `bold_folder_labels`,
`overlay_scroll_bars`, `hide_tab_scrolling_buttons`, `hide_new_tab_button`,
`draw_shadows`, `show_minimap`, `show_sidebar_button`, and it clears a stale
`file_icon_theme`.

Not touched: fonts, font sizes, indentation, wrapping, key bindings, project
files, `ignored_packages`.

## Cross-platform notes

- The theme loads on Windows and Linux; `title_bar` `bg`/`fg` only take effect
  on macOS 10.10+ with `themed_title_bar: true`.
- Windows and Linux draw their own window frame, so the "island gap" reads as
  the client area background rather than as chrome.
- Retina correctness depends on `@2x`/`@3x` textures; both are shipped for
  every texture and icon.
