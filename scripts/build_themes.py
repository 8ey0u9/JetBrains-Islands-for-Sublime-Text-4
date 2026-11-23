"""
Build the JetBrains Islands UI themes (.sublime-theme) and file icon themes.

Single source of truth: Dark / Light share one rule list, only the palette and
the luminosity flags differ. Colours come from the IntelliJ IDEA Islands
themes (platform-resources/src/themes/islands/*.theme.json):

    MainWindow.background  -> jb_window_bg      (lighter than editor in Dark,
                                                 darker than editor in Light)
    ToolWindow / Editor    -> jb_toolwindow_bg  (= editor background)
    EditorTabs.background  -> jb_tab_bar_bg     (= editor background)
    EditorTabs.underlinedTabBackground          -> jb_tab_active_bg
    EditorTabs.underlinedBorderColor            -> jb_tab_active_border
    StatusBar.background   -> jb_status_bg      (= main window background)
    Popup.background       -> jb_popup_bg       (one layer above the editor)

Texture paths are relative to Packages/, hence PACKAGE_DIR must match the name
of the installed package folder.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_DIR = "JetBrains Islands"
TEX = PACKAGE_DIR + "/textures"


def theme_path(name):
    return f"{TEX}/{name}.png"


DARK = {
    "name": "JetBrains Islands Dark",
    "dark": True,
    # Backgrounds
    "jb_window_bg": "#26282C",         # island gap, title bar, status bar
    "jb_toolwindow_bg": "#1E1F22",     # sidebar / tool windows (distinct surface)
    "jb_panel_bg": "#191A1C",          # find / console / output panels
    "jb_tab_bar_bg": "#191A1C",        # editor tab strip
    "jb_popup_bg": "#26282C",          # quick panel, auto complete, tooltip
    "jb_popup_border": "#33353B",
    "jb_status_bg": "#26282C",
    # Tabs (Islands selected tab = pill, not a full-bleed block)
    "jb_tab_active_bg": "#233558",
    "jb_tab_active_border": "#2E4D89",
    "jb_tab_inactive_bg": "#26282C",
    "jb_tab_inactive_border": "#40434A",
    "jb_row_selected": "#2A4371",
    "jb_hover_bg": "hsla(0, 0%, 100%, 0.09)",
    # Borders / text
    "jb_border": "#33353B",
    "jb_border_strong": "#40434A",
    "jb_text": "#D1D3D9",
    "jb_text_dim": "#9FA2A8",
    "jb_text_faint": "#6F737A",
    "jb_accent": "#3871E1",
    "jb_accent_soft": "#2E4D89",
    "jb_link": "#71A1FE",
    # Icons
    "jb_icon": "#9DA0A8",
    "jb_folder_icon": "#6F737A",
    # Inputs
    "jb_input_bg": "#191A1C",
    "jb_input_border": "#40434A",
    "jb_input_focus_border": "#3871E1",
    # Scroll bars
    "jb_scroll_thumb": "#808080",
    # Feedback
    "jb_error": "#F57E84",
    "jb_warning": "#D59637",
    "jb_success": "#6DB083",
}

LIGHT = {
    "name": "JetBrains Islands Light",
    "dark": False,
    "jb_window_bg": "#E9EAEE",
    "jb_toolwindow_bg": "#F7F8FA",     # sidebar / tool windows (distinct surface)
    "jb_panel_bg": "#FFFFFF",
    "jb_tab_bar_bg": "#FFFFFF",
    "jb_popup_bg": "#FFFFFF",
    "jb_popup_border": "#D1D3D9",
    "jb_status_bg": "#E9EAEE",
    "jb_tab_active_bg": "#E3EBFE",
    "jb_tab_active_border": "#A7C5FF",
    "jb_tab_inactive_bg": "#E9EAEE",
    "jb_tab_inactive_border": "#D1D3D9",
    "jb_row_selected": "#D0DFFE",
    "jb_hover_bg": "hsla(0, 0%, 0%, 0.07)",
    "jb_border": "#E9EAEE",
    "jb_border_strong": "#D1D3D9",
    "jb_text": "#080808",
    "jb_text_dim": "#5F6269",
    "jb_text_faint": "#9FA2A8",
    "jb_accent": "#3871E1",
    "jb_accent_soft": "#BDD3FF",
    "jb_link": "#2F5EB9",
    "jb_icon": "#6C707E",
    "jb_folder_icon": "#6C707E",
    "jb_input_bg": "#FFFFFF",
    "jb_input_border": "#D1D3D9",
    "jb_input_focus_border": "#3871E1",
    "jb_scroll_thumb": "#808080",
    "jb_error": "#C54E58",
    "jb_warning": "#A56906",
    "jb_success": "#338555",
}

# IntelliJ semantic colours used by the completion kind badges and VCS stripes.
KIND = {
    "kind_function_color": "#56A8F5",
    "kind_keyword_color": "#CF8E6D",
    "kind_markup_color": "#D5B778",
    "kind_namespace_color": "#56A8F5",
    "kind_navigation_color": "#B3AE60",
    "kind_snippet_color": "#6AAB73",
    "kind_type_color": "#C77DBB",
    "kind_variable_color": "#2AACB8",
}


def variables(p):
    """Override the Default theme's variables so inherited rules stay on palette."""
    # Every palette entry must be published as a variable: the rules below
    # reference them through var(jb_*), and an undefined variable resolves to
    # white, which silently breaks the whole island hierarchy.
    v = {k: val for k, val in p.items() if k not in ("name", "dark")}
    v.update({
        "font_face": "system",
        "font_size_sm": 11,
        "font_size": 12,
        "font_size_lg": 13,
        "font_size_title": 24,
        # Base
        "ui_bg": "var(jb_popup_bg)",
        "text_fg": "var(jb_text)",
        "label_color": "var(jb_text)",
        "link_fg": "var(jb_link)",
        "icon_tint": "var(jb_text_dim)",
        "shape_tint": "var(jb_text_dim)",
        "button_label_color": "var(jb_text)",
        "button_label_shadow": "transparent",
        # Sidebar
        "sidebar_bg": "var(jb_toolwindow_bg)",
        "sidebar_row_selected": "var(jb_row_selected)",
        "sidebar_heading": "var(jb_text_faint)",
        "sidebar_heading_shadow": "transparent",
        "sidebar_label": "var(jb_text)",
        "sidebar_label_selected": "var(jb_text)",
        "sidebar_label_ignored": "var(jb_text_faint)",
        "sidebar_button_tint": "var(jb_text_dim)",
        "sidebar_button_new_tint": "var(jb_success)",
        "sidebar_button_modified_tint": "var(jb_text_dim)",
        "sidebar_button_deleted_tint": "var(jb_error)",
        "sidebar_hover_row_tint": "var(jb_hover_bg)",
        # Scroll bars (overlay style, as in IntelliJ)
        "scroll_bar_bg": "var(jb_scroll_thumb)",
        "scroll_bar_puck_bg": "var(jb_scroll_thumb)",
        "scroll_bar_dark_bg": "var(jb_scroll_thumb)",
        "scroll_bar_puck_dark_bg": "var(jb_scroll_thumb)",
        "sidebar_scroll_bar_bg": "var(jb_scroll_thumb)",
        "sidebar_scroll_bar_puck_bg": "var(jb_scroll_thumb)",
        # VCS
        "vcs_untracked": "var(jb_text_dim)",
        "vcs_modified": "var(jb_link)",
        "vcs_missing": "var(jb_error)",
        "vcs_staged": "var(jb_link)",
        "vcs_added": "var(jb_success)",
        "vcs_deleted": "var(jb_error)",
        "vcs_unmerged": "var(jb_warning)",
        # Panels / dialogs
        "panel_bg": "var(jb_panel_bg)",
        "switch_project_bg": "var(jb_popup_bg)",
        "dialog_bg": "var(jb_window_bg)",
        "dialog_button_bg": "var(jb_input_bg)",
        "progress_bar_bg": "color(var(jb_text) a(0.06))",
        "progress_bar_fg": "var(jb_accent)",
        "icon_button_highlight": "var(jb_hover_bg)",
        "tool_tip_bg": "var(jb_popup_bg)",
        "tool_tip_fg": "var(jb_text)",
        # Tabs
        "tabset_dark_bg": "var(jb_tab_bar_bg)",
        "tabset_medium_dark_bg": "var(jb_tab_bar_bg)",
        "tabset_medium_bg": "var(jb_tab_bar_bg)",
        "tabset_light_bg": "var(jb_tab_bar_bg)",
        "tabset_button_light_tint": "var(jb_text_dim)",
        "tabset_button_opacity": {"target": 0.7, "speed": 4.0, "interpolation": "smoothstep"},
        "tabset_new_tab_button_opacity": {"target": 0.55, "speed": 4.0, "interpolation": "smoothstep"},
        "tabset_button_hover_opacity": {"target": 1.0, "speed": 4.0, "interpolation": "smoothstep"},
        "file_tab_selected_label_color": "var(jb_text)",
        "file_tab_unselected_label_color": "var(jb_text_dim)",
        "file_tab_selected_light_label_color": "var(jb_text)",
        "file_tab_unselected_light_label_color": "var(jb_text_dim)",
        "file_tab_close_dark_tint": "var(jb_text_dim)",
        "file_tab_close_light_tint": "var(jb_text_dim)",
        "file_tab_close_dark_new_tint": "var(jb_success)",
        "file_tab_close_dark_modified_tint": "var(jb_text_dim)",
        "file_tab_close_dark_deleted_tint": "var(jb_error)",
        "file_tab_close_light_new_tint": "var(jb_success)",
        "file_tab_close_light_modified_tint": "var(jb_text_dim)",
        "file_tab_close_light_deleted_tint": "var(jb_error)",
        "file_tab_highlight_new_tint": "var(jb_success)",
        "file_tab_highlight_deleted_tint": "var(jb_error)",
        # Quick panel
        "overlay_bg": "var(jb_popup_bg)",
        "quick_panel_label_color": "var(jb_text)",
        "quick_panel_path_label_color": "var(jb_text_faint)",
        "quick_panel_matched_label_color": "var(jb_link)",
        "quick_panel_matched_path_label_color": "var(jb_link)",
        "quick_panel_selected_row_bg": "var(jb_row_selected)",
        "quick_panel_selected_label_color": "var(jb_text)",
        "quick_panel_selected_path_label_color": "var(jb_text_dim)",
        "quick_panel_selected_matched_label_color": "var(jb_link)",
        "quick_panel_selected_matched_path_label_color": "var(jb_link)",
        "quick_panel_link_color": "var(jb_link)",
        # Auto complete
        "auto_complete_bg_dark_tint": "color(var(jb_text) a(0.03))",
        "auto_complete_bg_light_tint": "color(var(jb_text) a(0.03))",
        "auto_complete_selected_row_dark_tint": "var(jb_row_selected)",
        "auto_complete_selected_row_light_tint": "var(jb_row_selected)",
        "auto_complete_text_dark_tint": "var(jb_text)",
        "auto_complete_text_light_tint": "var(jb_text)",
        "auto_complete_detail_pane_dark_tint": "color(var(jb_text) a(0.05))",
        "auto_complete_detail_pane_light_tint": "color(var(jb_text) a(0.05))",
        "auto_complete_detail_panel_mono_dark_bg": "color(var(jb_text) a(0.08))",
        "auto_complete_detail_panel_mono_light_bg": "color(var(jb_text) a(0.06))",
        # Controls
        "checkbox_back": "var(jb_input_bg)",
        "checkbox_border-unselected": "var(jb_input_border)",
        "checkbox_selected": "var(jb_accent)",
        "checkbox_border-selected": "var(jb_accent)",
        "checkbox-disabled": "var(jb_text_faint)",
        "radio_back": "var(jb_input_bg)",
        "radio_border-unselected": "var(jb_input_border)",
        "radio_selected": "var(jb_accent)",
        "radio_border-selected": "var(jb_accent)",
        # Status bar
        "status_bar_bg": "var(jb_status_bg)",
        "status_bar_label_color": "var(jb_text_dim)",
        "status_bar_label_shadow": "transparent",
        "status_bar_icon_tint": "var(jb_text_dim)",
        # Minimap viewport
        "viewport_always_visible_color": "color(var(jb_text) a(0.20))",
        "viewport_hide_show_color": "color(var(jb_text) a(0.28))",
        # Icon opacity (Default drives sidebar/find icons with these)
        "icon_opacity": {"target": 0.85, "speed": 5.0, "interpolation": "smoothstep"},
        "icon_hover_opacity": {"target": 1.0, "speed": 5.0, "interpolation": "smoothstep"},
        "sidebar_button_opacity": {"target": 0.75, "speed": 4.0, "interpolation": "smoothstep"},
        "sidebar_button_hover_opacity": {"target": 1.0, "speed": 4.0, "interpolation": "smoothstep"},
        "sidebar_close_button_opacity": {"target": 0.75, "speed": 4.0, "interpolation": "smoothstep"},
        "sidebar_close_button_hover_opacity": {"target": 1.0, "speed": 4.0, "interpolation": "smoothstep"},
        # Islands shows a tab close button only on the active tab or on hover.
        "file_tab_close_opacity": {"target": 0.0, "speed": 4.0, "interpolation": "smoothstep"},
        "file_tab_close_hover_opacity": {"target": 1.0, "speed": 4.0, "interpolation": "smoothstep"},
        "file_tab_close_selected_opacity": {"target": 0.85, "speed": 4.0, "interpolation": "smoothstep"},
        "file_tab_close_selected_hover_opacity": {"target": 1.0, "speed": 4.0, "interpolation": "smoothstep"},
        "kind_name_label_border_color": "color(var(jb_accent) a(0.8))",
    })
    v.update(KIND)
    return v


def build_rules(p):
    dark = p["dark"]
    rules = []
    add = rules.append

    # ---------------------------------------------------------------- window
    add({
        "class": "title_bar",
        "settings": ["themed_title_bar"],
        "bg": "var(jb_window_bg)",
        "fg": "var(jb_text)",
        "style": "dark" if dark else "light",
    })
    # Island gap between split panes: the main window colour, not a border line.
    add({"class": "grid_layout_control", "border_color": "var(jb_window_bg)", "border_size": 2})

    # --------------------------------------------------------------- sidebar
    add({
        "class": "sidebar_container",
        "layer0.tint": "var(jb_toolwindow_bg)",
        "layer0.opacity": 1.0,
        "content_margin": [0, 4, 0, 4],
    })
    add({
        "class": "sidebar_tree",
        "row_padding": [12, 4, 6, 4],
        "indent": 12,
        "indent_offset": 12,
        "indent_top_level": False,
        "dark_content": dark,
        "spacer_rows": True,
    })
    # Rows: no fill by default, rounded pill on hover / selection (Islands tree).
    add({"class": "tree_row", "attributes": ["!hover", "!selected"], "layer0.opacity": 0.0})
    add({
        "class": "tree_row",
        "attributes": ["selectable", "hover", "!selected"],
        "layer0.texture": theme_path("row_pill"),
        "layer0.inner_margin": [8, 6, 8, 6],
        "layer0.tint": "var(jb_hover_bg)",
        "layer0.opacity": 1.0,
    })
    add({
        "class": "tree_row",
        "attributes": ["selected"],
        "layer0.texture": theme_path("row_pill"),
        "layer0.inner_margin": [8, 6, 8, 6],
        "layer0.tint": "var(jb_row_selected)",
        "layer0.opacity": 1.0,
    })
    add({"class": "tree_row", "attributes": ["highlighted"], "layer0.opacity": 1.0})

    add({
        "class": "sidebar_heading",
        "fg": "var(jb_text_faint)",
        "font.face": "var(font_face)",
        "font.size": 11,
        "font.bold": True,
        "case": "upper",
        "shadow_color": "transparent",
    })
    add({
        "class": "sidebar_label",
        "fg": "var(jb_text)",
        "font.face": "var(font_face)",
        "font.size": 13,
        "shadow_color": "transparent",
    })
    add({
        "class": "sidebar_label",
        "parents": [{"class": "tree_row", "attributes": ["selected"]}],
        "fg": "var(jb_text)",
    })
    add({
        "class": "sidebar_label",
        "parents": [{"class": "tree_row", "attributes": ["expandable"]}],
        "settings": ["bold_folder_labels"],
        "font.bold": True,
    })
    add({
        "class": "sidebar_label",
        "parents": [{"class": "file_system_entry", "attributes": ["ignored"]}],
        "fg": "var(jb_text_faint)",
    })

    # Icons: 16px boxes, monochrome folder/chevron glyphs tinted per theme,
    # third-party file icons keep their own colours (tint = white).
    add({
        "class": "icon_folder",
        "layer0.texture": theme_path("folder_closed"),
        "layer0.inner_margin": [5, 5, 5, 5],
        "layer0.tint": "var(jb_folder_icon)",
        "layer0.opacity": 1.0,
        "content_margin": [8, 8],
    })
    add({
        "class": "icon_folder",
        "parents": [{"class": "tree_row", "attributes": ["expanded"]}],
        "layer0.texture": theme_path("folder_open"),
    })
    add({
        "class": "icon_folder_dup",
        "layer0.texture": theme_path("folder_symlink"),
        "layer0.inner_margin": [5, 5, 5, 5],
        "layer0.tint": "var(jb_folder_icon)",
        "layer0.opacity": 1.0,
        "content_margin": [8, 8],
    })
    add({
        "class": "icon_file_type",
        "layer0.tint": "white",
        "layer0.opacity": 1.0,
        "content_margin": [8, 8],
    })
    add({
        "class": "disclosure_button_control",
        "layer0.texture": theme_path("chevron_right"),
        "layer0.tint": "var(jb_text_dim)",
        "layer0.opacity": 1.0,
        "content_margin": [8, 8],
    })
    add({
        "class": "disclosure_button_control",
        "attributes": ["expanded"],
        "layer0.texture": theme_path("chevron_down"),
    })
    add({
        "class": "close_button",
        "layer0.texture": "Theme - Default/common/open_file_close.png",
        "layer0.tint": "var(jb_text_dim)",
        "layer0.opacity": "var(sidebar_close_button_opacity)",
        "content_margin": [8, 8],
    })
    add({"class": "close_button", "attributes": ["!hover", "dirty"], "layer0.texture": "Theme - Default/common/open_file_dirty.png"})
    add({"class": "file_system_entry", "content_margin": [0, 0, 8, 0], "spacing": 5})

    # ------------------------------------------------------------------ tabs
    add({
        "class": "tabset_control",
        "layer0.opacity": 1.0,
        "layer0.tint": "var(jb_tab_bar_bg)",
        "content_margin": [6, 4, 6, 0],
        "tab_height": 36,
    })
    add({
        "class": "tabset_control",
        "settings": {"file_tab_style": ["", "rounded"]},
        "tab_overlap": 0,
        "tab_height": 36,
        "connector_height": 1,
    })
    add({
        "class": "tabset_control",
        "settings": {"file_tab_style": "square"},
        "tab_overlap": 1,
        "tab_height": 36,
        "connector_height": 0,
        "spacing": 4,
    })
    add({"class": "tab_connector", "layer0.texture": "", "layer0.opacity": 0.0})

    TAB = {"file_tab_style": ["", "rounded", "square"]}
    add({
        "class": "tab_control",
        "settings": TAB,
        "layer0.texture": theme_path("tab_pill"),
        "layer0.inner_margin": [8, 8, 8, 8],
        "layer0.tint": "var(jb_tab_bar_bg)",
        "layer0.opacity": 1.0,
        "layer1.texture": theme_path("tab_pill_border"),
        "layer1.inner_margin": [8, 8, 8, 8],
        "layer1.tint": "var(jb_tab_inactive_border)",
        "layer1.opacity": 0.0,
        "tint_index": 3,
        "layer2.texture": "",
        "layer2.opacity": 0.0,
        "layer3.texture": "",
        "layer3.opacity": 0.0,
        # Islands pads the label well clear of the pill edge: ~14 pt in front
        # and ~10 pt before the close button. content_margin is in addition to
        # the texture's own inner margin, so it must stay generous.
        "content_margin": [12, 5, 9, 5],
        "max_margin_trim": 6,
        "hit_test_level": 0.2,
    })
    add({
        "class": "tab_control",
        "settings": TAB,
        "attributes": ["!selected", "hover"],
        "layer0.tint": "var(jb_hover_bg)",
        "layer1.opacity": 0.0,
        "layer1.tint": "var(jb_tab_inactive_border)",
    })
    add({
        "class": "tab_control",
        "settings": TAB,
        "attributes": ["selected", "left_overhang"],
        "layer0.texture": theme_path("tab_pill"),
        "layer1.texture": theme_path("tab_pill_border"),
    })
    add({
        "class": "tab_control",
        "settings": TAB,
        "attributes": ["selected", "right_overhang"],
        "layer0.texture": theme_path("tab_pill"),
        "layer1.texture": theme_path("tab_pill_border"),
    })
    add({
        "class": "tab_control",
        "settings": TAB,
        "attributes": ["selected"],
        "layer0.tint": "var(jb_tab_active_bg)",
        "layer1.tint": "var(jb_tab_active_border)",
        "layer1.opacity": 1.0,
    })
    add({
        "class": "tab_control",
        "settings": TAB,
        "attributes": ["selected", "!highlighted"],
        "layer0.tint": "var(jb_tab_inactive_bg)",
        "layer1.tint": "var(jb_tab_inactive_border)",
        "layer1.opacity": 1.0,
    })

    add({
        "class": "tab_label",
        "font.face": "var(font_face)",
        "font.size": 13,
        "fg": "var(jb_text_dim)",
        "shadow_color": "transparent",
    })
    add({"class": "tab_label", "attributes": ["transient"], "font.italic": True})
    add({
        "class": "tab_label",
        "parents": [{"class": "tab_control", "attributes": ["!selected", "hover"]}],
        "fg": "var(jb_text)",
    })
    add({
        "class": "tab_label",
        "parents": [{"class": "tab_control", "attributes": ["selected"]}],
        "fg": "var(jb_text)",
    })

    add({
        "class": "tab_close_button",
        "settings": ["show_tab_close_buttons"],
        "layer0.texture": "Theme - Default/common/tab_close.png",
        "layer0.tint": "var(jb_text_dim)",
        # Islands keeps the close glyph well inside the pill, not flush right.
        "content_margin": [9, 9, 5, 9],
    })
    add({"class": "tab_close_button", "settings": ["show_tab_close_buttons_on_left"], "content_margin": [13, 9, 9, 9]})
    add({"class": "tab_close_button", "settings": ["!show_tab_close_buttons"], "content_margin": 0})

    for cls, tex, cm in (
        ("new_tab_button", "Theme - Default/common/new_tab.png", [12, 12]),
        ("scroll_tabs_left_button", "Theme - Default/common/tab_scroll_left.png", [11, 12, 10, 12]),
        ("scroll_tabs_right_button", "Theme - Default/common/tab_scroll_right.png", [10, 12, 11, 12]),
        ("show_tabs_dropdown_button", "Theme - Default/common/tab_dropdown.png", [11, 12]),
    ):
        rule = {
            "class": cls,
            "layer0.texture": tex,
            "layer0.tint": "var(jb_text_dim)",
            "layer0.opacity": "var(tabset_button_opacity)",
            "content_margin": cm,
        }
        # The base theme hides these buttons with settings-gated
        # "content_margin: 0" rules. An unfiltered rule placed after one of
        # those would resurrect the button, so mirror each gate here.
        if cls.startswith("scroll"):
            rule["settings"] = ["!hide_tab_scrolling_buttons"]
        elif cls == "new_tab_button":
            rule["settings"] = ["!hide_new_tab_button"]
        add(rule)
        add({"class": cls, "attributes": ["hover"], "layer0.opacity": "var(tabset_button_hover_opacity)"})

    # Islands has no tab overflow dropdown, so collapse it away entirely.
    add({
        "class": "show_tabs_dropdown_button",
        "layer0.opacity": 0.0,
        "content_margin": 0,
    })

    # ------------------------------------------------------------- status bar
    add({
        "class": "status_bar",
        "layer0.tint": "var(jb_status_bg)",
        "layer0.opacity": 1.0,
        "content_margin": [10, 5, 10, 5],
    })
    add({"class": "status_bar", "attributes": ["panel_visible"], "content_margin": [10, 5, 10, 5]})
    add({"class": "status_container", "content_margin": [8, 0, 0, 0]})
    add({
        "class": "label_control",
        "parents": [{"class": "status_bar"}],
        "font.size": 12,
        "fg": "var(jb_text_dim)",
        "shadow_color": "transparent",
    })
    add({
        "class": "status_button",
        "content_margin": [8, 3, 8, 3],
        "min_size": [0, 0],
        "layer0.texture": theme_path("row_pill"),
        "layer0.inner_margin": [8, 6, 8, 6],
        "layer0.tint": "var(jb_hover_bg)",
        "layer0.opacity": 0.0,
    })
    add({"class": "status_button", "attributes": ["hover"], "layer0.opacity": 1.0})
    add({
        "class": "label_control",
        "parents": [{"class": "status_button", "attributes": ["hover"]}],
        "fg": "var(jb_text)",
    })
    add({
        "class": "sidebar_button_control",
        "layer0.texture": "Theme - Default/common/sidebar_button.png",
        "layer0.tint": "var(jb_text_dim)",
        "layer0.opacity": "var(sidebar_button_opacity)",
        "content_margin": [10, 8],
    })
    add({"class": "sidebar_button_control", "attributes": ["hover"], "layer0.opacity": "var(sidebar_button_hover_opacity)"})
    add({
        "class": "vcs_status",
        "spacing": 4,
        "content_margin": [4, 0, 4, 0],
    })
    add({
        "class": "vcs_branch_icon",
        "layer0.texture": "Theme - Default/common/branch.png",
        "layer0.tint": "var(jb_text_dim)",
        "layer0.opacity": 1.0,
        "content_margin": [8, 8],
    })
    add({
        "class": "vcs_changes_annotation",
        "font.face": "var(font_face)",
        "font.size": 11,
        "color": "var(jb_text_dim)",
        "border_color": "var(jb_text_dim)",
        "content_margin": [4, 0],
    })

    # ----------------------------------------------------------------- panels
    add({
        "class": "panel_control",
        "layer0.tint": "var(jb_panel_bg)",
        "layer0.opacity": 1.0,
        "content_margin": [6, 4, 6, 4],
    })
    add({
        "class": "panel_grid_control",
        "inside_spacing": 6,
        "outside_hspacing": 6,
        "outside_vspacing": 6,
    })
    add({
        "class": "panel_close_button",
        "layer0.texture": "Theme - Default/common/panel_close.png",
        "layer0.tint": "var(jb_text_dim)",
        "layer0.opacity": {"target": 0.7, "speed": 4.0, "interpolation": "smoothstep"},
        "content_margin": 8,
    })
    add({"class": "panel_close_button", "attributes": ["hover"], "layer0.opacity": 1.0})

    # Text inputs (quick panel, find, replace, input panels)
    add({
        "class": "text_line_control",
        "layer0.texture": theme_path("input_pill"),
        "layer0.inner_margin": [8, 8, 8, 8],
        "layer0.tint": "var(jb_input_bg)",
        "layer0.opacity": 1.0,
        "layer1.texture": theme_path("input_pill_border"),
        "layer1.inner_margin": [8, 8, 8, 8],
        "layer1.tint": "var(jb_input_border)",
        "layer1.opacity": 1.0,
        "content_margin": [8, 5, 8, 5],
        # Default inherits tint_index: 0, which re-tints layer0 with the
        # color-scheme background and crushes the input fill toward black.
        "tint_index": -1,
    })
    add({
        "class": "text_line_control",
        "parents": [{"class": "overlay_control"}],
        "font.face": "system",
        "font.size": 13,
    })

    # Find panel icon buttons: pill on hover / toggled (Islands toggles are filled).
    add({
        "class": "icon_button_control",
        "layer0.texture": theme_path("icon_button_pill"),
        "layer0.inner_margin": [6, 6, 6, 6],
        "layer0.tint": "var(jb_hover_bg)",
        "layer0.opacity": 0.0,
        "content_margin": 3,
    })
    add({"class": "icon_button_control", "attributes": ["hover"], "layer0.opacity": 1.0})
    add({
        "class": "icon_button_control",
        "attributes": ["selected"],
        "layer0.tint": "var(jb_accent_soft)",
        "layer0.opacity": 1.0,
    })
    add({
        "class": "label_control",
        "parents": [{"class": "panel_control"}],
        "fg": "var(jb_text)",
    })

    # ---------------------------------------------------------------- buttons
    add({
        "class": "button_control",
        "layer0.texture": theme_path("button_pill"),
        "layer0.inner_margin": [8, 8, 8, 8],
        "layer0.tint": "transparent",
        "layer0.opacity": 1.0,
        "layer1.texture": theme_path("button_pill_border"),
        "layer1.inner_margin": [8, 8, 8, 8],
        "layer1.tint": "var(jb_input_border)",
        "layer1.opacity": 1.0,
        "min_size": [72, 26],
        "content_margin": [12, 5, 12, 5],
    })
    add({"class": "button_control", "attributes": ["hover"], "layer0.tint": "var(jb_hover_bg)"})
    add({"class": "button_control", "attributes": ["pressed"], "layer0.tint": "var(jb_accent_soft)", "layer1.tint": "var(jb_accent)"})
    add({"class": "button_control", "attributes": ["disabled"], "layer0.opacity": 0.5, "layer1.tint": "var(jb_border_strong)"})
    add({
        "class": "button_control",
        "parents": [{"class": "dialog"}],
        "layer0.tint": "transparent",
        "layer1.tint": "var(jb_input_border)",
    })
    add({
        "class": "label_control",
        "parents": [{"class": "button_control"}],
        "fg": "var(jb_text)",
        "shadow_color": "transparent",
    })

    # ------------------------------------------------------------ popup panels
    add({
        "class": "overlay_control",
        "layer0.tint": "var(jb_popup_bg)",
        "layer0.opacity": 1.0,
        "layer1.texture": theme_path("input_pill_border"),
        "layer1.inner_margin": [8, 8, 8, 8],
        "layer1.tint": "var(jb_popup_border)",
        "layer1.opacity": 1.0,
        "content_margin": 4,
    })
    add({
        "class": "quick_panel",
        "layer0.tint": "var(jb_popup_bg)",
        "layer0.opacity": 1.0,
        "row_padding": [8, 5, 8, 5],
        "dark_content": dark,
    })
    for cls in ("mini_quick_panel_row", "quick_panel_row"):
        add({
            "class": cls,
            "layer0.texture": theme_path("row_pill"),
            "layer0.inner_margin": [8, 6, 8, 6],
            "layer0.tint": "var(jb_row_selected)",
            "layer0.opacity": 0.0,
        })
        add({"class": cls, "attributes": ["selected"], "layer0.opacity": 1.0})
    add({
        "class": "quick_panel_label",
        "font.face": "var(font_face)",
        "font.size": 13,
        "fg": "var(jb_text)",
        "match_fg": "var(jb_link)",
        "selected_fg": "var(jb_text)",
        "selected_match_fg": "var(jb_link)",
    })
    add({
        "class": "quick_panel_path_label",
        "font.size": 11,
        "fg": "var(jb_text_faint)",
        "match_fg": "var(jb_link)",
        "selected_fg": "var(jb_text_dim)",
        "selected_match_fg": "var(jb_link)",
    })
    add({
        "class": "quick_panel_label key_binding",
        "fg": "var(jb_text_faint)",
        "selected_fg": "var(jb_text_dim)",
    })
    add({
        "class": "quick_panel_label hint",
        "fg": "var(jb_text_faint)",
        "selected_fg": "var(jb_text_dim)",
    })
    add({
        "class": "popup_control",
        "layer0.tint": "var(jb_popup_bg)",
        "layer0.opacity": 1.0,
    })
    add({
        "class": "auto_complete",
        "row_padding": 0,
        "layer0.tint": "var(jb_popup_bg)",
        "layer0.opacity": 1.0,
        # Default sets tint_index: 0, re-tinting the popup with the scheme
        # background; the Islands popup must stay on jb_popup_bg.
        "tint_index": -1,
    })
    add({
        "class": "table_row",
        "layer0.tint": "var(jb_row_selected)",
        "layer0.opacity": 0.0,
    })
    add({"class": "table_row", "attributes": ["selected"], "layer0.opacity": 1.0})
    add({"class": "tool_tip_control", "layer0.texture": theme_path("button_pill"),
         "layer0.inner_margin": [8, 8, 8, 8], "layer0.tint": "var(jb_popup_bg)", "layer0.opacity": 1.0,
         "layer1.texture": theme_path("button_pill_border"), "layer1.inner_margin": [8, 8, 8, 8],
         "layer1.tint": "var(jb_popup_border)", "content_margin": [8, 5]})
    add({"class": "tool_tip_label_control", "font.face": "var(font_face)", "font.size": 12, "fg": "var(jb_text)"})

    # ---------------------------------------------------------------- editor
    add({"class": "fold_button_control", "layer0.tint": "var(jb_text_faint)",
         "layer0.opacity": {"target": 0.7, "speed": 4.0, "interpolation": "smoothstep"}, "content_margin": 8})
    add({"class": "fold_button_control", "attributes": ["hover"], "layer0.opacity": 1.0})
    add({"class": "minimap_control", "settings": ["always_show_minimap_viewport"],
         "viewport_color": "var(viewport_always_visible_color)", "viewport_opacity": 1.0})
    add({"class": "minimap_control", "settings": ["!always_show_minimap_viewport"],
         "viewport_color": "var(viewport_hide_show_color)",
         "viewport_opacity": {"target": 0.0, "speed": 4.0, "interpolation": "smoothstep"}})
    add({"class": "minimap_control", "attributes": ["hover"], "settings": ["!always_show_minimap_viewport"],
         "viewport_opacity": {"target": 1.0, "speed": 20.0, "interpolation": "smoothstep"}})

    # ------------------------------------------------------------ scroll bars
    add({"class": "scroll_area_control", "settings": ["overlay_scroll_bars"], "overlay": True})
    # Default tints the scroll bar host with the scheme background; keep the
    # puck tint as authored.
    add({"class": "scroll_bar_control", "tint_index": -1})
    add({"class": "scroll_corner_control", "tint_index": -1, "layer0.opacity": 1.0})
    add({"class": "puck_control", "layer0.tint": "var(jb_scroll_thumb)",
         "layer0.opacity": {"target": 0.30, "speed": 5.0, "interpolation": "smoothstep"}})
    add({"class": "puck_control",
         "parents": [{"class": "scroll_bar_control", "attributes": ["hover"]}, {"class": "scroll_track_control"}],
         "layer0.opacity": {"target": 0.55, "speed": 5.0, "interpolation": "smoothstep"}})

    return rules


def write_theme(p):
    data = {
        "extends": "Default.sublime-theme",
        "variables": variables(p),
        "rules": build_rules(p),
    }
    path = os.path.join(ROOT, f"{p['name']}.sublime-theme")
    with open(path, "w") as f:
        f.write("// JetBrains Islands — generated by scripts/build_themes.py\n")
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
        f.write("\n")
    return path


def icon_names(prefix):
    """Resolve icon names for one flavour, honouring per-theme variants."""
    manifest = json.load(open(os.path.join(ROOT, "scripts", "icon-map.json")))
    variants = json.load(open(os.path.join(ROOT, "scripts", "icon-variants.json")))
    flavour = "dark" if prefix.startswith("dark") else "light"

    def resolve(icon):
        v = variants.get(icon, {}).get(flavour)
        return v or f"file_type_{icon}"

    mapping = {k: resolve(v) for k, v in manifest["mapping"].items()}
    mapping.update({k: resolve(v) for k, v in manifest["nameMapping"].items()})
    mapping.setdefault("txt", "file_type_console")
    mapping.setdefault("log", "file_type_console")
    mapping.setdefault("md", resolve("markdown"))
    return mapping


def write_file_icons():
    out = {}
    for name, prefix in (("JetBrains Islands Dark", "dark"), ("JetBrains Islands Light", "light")):
        mapping = icon_names(prefix)
        payload = json.dumps({"icons": mapping}, indent=4, ensure_ascii=False)
        path = os.path.join(ROOT, f"{name}.sublime-file-icons")
        with open(path, "w") as f:
            f.write("// JetBrains Islands file icons — generated by scripts/build_themes.py\n")
            f.write(payload)
            f.write("\n")
        out[name] = len(mapping)
    return out


if __name__ == "__main__":
    for p in (DARK, LIGHT):
        print("theme:", write_theme(p))
    print("icon mappings:", write_file_icons())
