# Changelog

Version scheme: `0.x` while the visual target is still being tightened,
`1.0.0` at first public release.

## 0.9.0 — 2026-11-23

First complete build: Dark and Light from a single install.

**Themes**
- Islands Dark / Light UI themes, generated from one shared rule list.
- Islands Dark / Light color schemes covering 60 scope rules.
- 138 file-type icon mappings with `@2x`/`@3x` retina variants, contrast-adjusted
  to ≥3:1 against both backgrounds.
- Pill tabs (not full-bleed blocks), calibrated to 8.5 pt left / 8.0 pt right
  padding against IntelliJ's own Islands tab asset.
- One-command switching (`islands_switch_dark` / `_light` / `_auto`) plus a
  settings-template pair.

**Fixed during acceptance**
- Input fields crushed to `#0E0E10` by the inherited `tint_index: 0`; set to `-1`.
- Tab scroll arrows and new-tab button resurrected by unfiltered rules placed
  after the base theme's settings-gated ones; gates mirrored.
- Tab close button pinned flush to the pill's right edge; padding recalibrated.
- Selected tab label pressed against the pill's left edge (2.5 pt); now 8.5 pt.
- Bracket matching was a faint stipple; now a solid underline with a blue
  foreground.
- `inactive_sheet_dimming` darkened unfocused inputs via `text_widget_dark_modifier`;
  no longer enabled.

**Known limits** (documented in `docs/COMPATIBILITY.md`)
- No island gap between sidebar and editor: `grid_layout_control` does not
  cover the sidebar and 1 px textures stretch into a band.
- No tool-window stripe, breadcrumb, or tab icons: Sublime has no such controls.
- `show_minimap` is an internal view flag, not a settable preference.
