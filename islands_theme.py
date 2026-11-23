"""JetBrains Islands — one-command Dark/Light switching.

The package ships both flavours; this plugin flips the theme, the color scheme
and the handful of tab-layout settings that define the Islands look. Nothing
else in the user's preferences is touched.

File icons need no setting: Sublime Text loads the `.sublime-file-icons` file
whose name matches the active `.sublime-theme`, so the Dark theme picks the
dark icon variants and the Light theme the light ones.
"""
import sublime
import sublime_plugin

PREFS = "Preferences.sublime-settings"
FLAVORS = {
    "dark": ("JetBrains Islands Dark.sublime-theme",
             "JetBrains Islands Dark.sublime-color-scheme"),
    "light": ("JetBrains Islands Light.sublime-theme",
              "JetBrains Islands Light.sublime-color-scheme"),
}
LAYOUT = {
    "file_tab_style": "rounded",
    "themed_title_bar": True,
    "highlight_modified_tabs": True,
    "bold_folder_labels": True,
    "overlay_scroll_bars": "enabled",
    # Islands draws no edge shadow between the editor and the minimap.
    "draw_shadows": False,
    # "show_minimap" is not a documented setting (only draw_minimap_border /
    # always_show_minimap_viewport / minimap_horizontal_scrolling are), so it
    # cannot be set from here. Use View > Hide Minimap.
    "show_sidebar_button": False,
    # IntelliJ's status bar carries encoding, line endings and indentation.
    "show_encoding": True,
    "show_line_endings": True,
    "show_indentation": True,
    "hide_tab_scrolling_buttons": True,
    "hide_new_tab_button": True,
    "show_tab_close_buttons_on_left": False,
}


def apply(flavor):
    """Apply the Islands flavour's theme, scheme and tab layout."""
    settings = sublime.load_settings(PREFS)
    settings.set("theme", FLAVORS[flavor][0])
    settings.set("color_scheme", FLAVORS[flavor][1])
    for key, value in LAYOUT.items():
        settings.set(key, value)
    # Pair the variants so "theme": "auto" follows the OS appearance into the
    # matching Islands flavour.
    settings.set("dark_theme", FLAVORS["dark"][0])
    settings.set("light_theme", FLAVORS["light"][0])
    settings.set("dark_color_scheme", FLAVORS["dark"][1])
    settings.set("light_color_scheme", FLAVORS["light"][1])
    # A pinned icon theme would keep the Dark variants alive in Light mode.
    if settings.get("file_icon_theme"):
        settings.erase("file_icon_theme")
    sublime.save_settings(PREFS)


class IslandsSwitchDarkCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        apply("dark")


class IslandsSwitchLightCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        apply("light")


class IslandsSwitchAutoCommand(sublime_plugin.ApplicationCommand):
    """Follow the OS appearance, with both flavours paired to Islands."""

    def run(self):
        settings = sublime.load_settings(PREFS)
        settings.set("dark_theme", FLAVORS["dark"][0])
        settings.set("light_theme", FLAVORS["light"][0])
        settings.set("dark_color_scheme", FLAVORS["dark"][1])
        settings.set("light_color_scheme", FLAVORS["light"][1])
        for key, value in LAYOUT.items():
            settings.set(key, value)
        if settings.get("file_icon_theme"):
            settings.erase("file_icon_theme")
        settings.set("theme", "auto")
        settings.set("color_scheme", "auto")
        sublime.save_settings(PREFS)
