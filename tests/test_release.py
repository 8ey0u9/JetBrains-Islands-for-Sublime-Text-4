"""Regression checks for release integrity and provider preference preservation."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from lib import package, settings, themes
from lib.package import release_files, repository_files


class ReleaseIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = repository_files()

    def test_current_source_validates(self):
        self.assertEqual(package.validate(self.files), [])
        self.assertEqual(package.generator_errors(self.files), [])

    def test_missing_retina_resource_is_rejected(self):
        files = dict(self.files)
        del files['textures/chevron_right@2x.png']
        self.assertTrue(any('chevron_right@2x' in e for e in package.validate(files)))

    def test_missing_packaged_base_texture_is_rejected(self):
        files = dict(self.files)
        del files['textures/popup_pill.png']
        self.assertTrue(any('missing JetBrains Islands/textures/popup_pill.png' in e
                            for e in package.validate(files)))

    def test_manual_colour_edit_is_rejected(self):
        files = dict(self.files)
        name = 'schemes/JetBrains Islands Dark.sublime-color-scheme'
        files[name] = files[name].replace(b'#26282C', b'#FF0000')
        self.assertTrue(any('debug red' in e for e in package.validate(files)))
        self.assertTrue(any('scheme differs' in e for e in package.generator_errors(files)))

    def test_runtime_css_is_in_release(self):
        files = release_files()
        self.assertIn('styles/mdpopups.css', files)
        self.assertIn('styles/popup-dark.css', files)
        self.assertNotIn('styles/popup.css', files)
        self.assertFalse(any(n.startswith(('tests/', 'scripts/', '__pycache__/')) for n in files))

    def test_config_layout_keeps_existing_preference_names_resolvable(self):
        files = release_files()
        configurations = [name for name in files
                          if '.sublime-' in name or name.endswith('.hidden-color-scheme')]
        self.assertEqual(len(configurations), 13)
        self.assertTrue(all('/' in name for name in configurations))
        self.assertFalse(any(ROOT.glob('*.sublime-*')))
        self.assertFalse(any(ROOT.glob('*.hidden-color-scheme')))
        self.assertNotIn('islands_theme.py', files)
        self.assertIn('settings/JetBrains Islands.sublime-commands', files)
        for flavor in ('Dark', 'Light'):
            template = package.load_json(files[f'settings/JetBrains Islands {flavor}.sublime-settings'])
            for key in ('theme', 'color_scheme', 'dark_theme', 'light_theme',
                        'dark_color_scheme', 'light_color_scheme'):
                basename = template[key]
                matches = [name for name in files if Path(name).name == basename]
                self.assertEqual(len(matches), 1, (key, basename, matches))
            theme = Path('themes') / template['theme']
            self.assertIn(theme.with_suffix('.sublime-file-icons').as_posix(), files)

    def test_development_sources_stay_out_of_install_archive(self):
        files = release_files()
        for name in ('docs/DESIGN.md',):
            self.assertIn(name, self.files)
            self.assertNotIn(name, files)
        self.assertTrue(any(n.endswith('.svg') for n in self.files))
        self.assertFalse(any(n.endswith('.svg') for n in files))
        self.assertEqual(package.validate(files, verify_sources=False), [])

    def test_packaged_icons_still_require_attribution(self):
        files = release_files()
        del files['NOTICE']
        self.assertIn('missing licensing resource: NOTICE',
                      package.validate(files, verify_sources=False))

    def test_unused_texture_is_rejected(self):
        files = dict(self.files)
        for suffix in ('', '@2x', '@3x'):
            files[f'textures/unused{suffix}.png'] = files[f'textures/row_pill{suffix}.png']
        self.assertIn('unused theme texture: textures/unused.png', package.validate(files))

    def test_broken_documentation_link_is_rejected(self):
        files = dict(self.files)
        del files['docs/DESIGN.md']
        self.assertIn('README.md: missing linked resource: docs/DESIGN.md',
                      package.validate(files))

    def test_stale_settings_documentation_is_rejected(self):
        files = dict(self.files)
        files['docs/SETTINGS.zh-CN.md'] += b'\nStale documentation\n'
        self.assertIn('Chinese settings documentation differs from generator',
                      package.generator_errors(files))

    def test_missing_widget_resource_is_rejected(self):
        for flavor in ('Dark', 'Light'):
            for directory, extension in (('schemes', '.hidden-color-scheme'),
                                         ('settings', '.sublime-settings')):
                name = f'{directory}/Widget - JetBrains Islands {flavor}{extension}'
                with self.subTest(resource=name):
                    files = dict(self.files)
                    del files[name]
                    self.assertIn(f'missing or invalid {name}', package.validate(files))

    def test_widget_binding_preserves_user_typography_and_native_syntax(self):
        for flavor in ('Dark', 'Light'):
            with self.subTest(flavor=flavor):
                name = f'Widget - JetBrains Islands {flavor}'
                settings = package.load_json(self.files['settings/' + name + '.sublime-settings'])
                # A theme-specific binding must not override font_size, font_face,
                # syntax, or the settings used by other themes' input widgets.
                self.assertEqual(set(settings), {'color_scheme'})
                self.assertEqual(settings['color_scheme'], name + '.hidden-color-scheme')
                self.assertIn('schemes/' + settings['color_scheme'], self.files)
        self.assertNotIn('Widget.sublime-settings', self.files)
        self.assertNotIn('Regex Widget.sublime-settings', self.files)
        self.assertNotIn('Regex Replace Widget.sublime-settings', self.files)

    def test_widget_placeholder_contrast_is_independent_of_editor_rulers(self):
        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
                      for v in channels]
            return sum(v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722)))

        for flavor in ('Dark', 'Light'):
            with self.subTest(flavor=flavor):
                name = f'JetBrains Islands {flavor}'
                widget = package.load_json(self.files[f'schemes/Widget - {name}.hidden-color-scheme'])
                editor = package.load_json(self.files['schemes/' + name + '.sublime-color-scheme'])
                globals_ = widget['globals']
                light, dark = sorted((luminance(globals_['rulers']),
                                      luminance(globals_['background'])), reverse=True)
                self.assertGreaterEqual((light + 0.05) / (dark + 0.05), 4.5)
                self.assertEqual(editor['globals']['rulers'], 'var(guide)')
                self.assertNotEqual(globals_['rulers'], editor['variables']['guide'])


class PopupTemplate(unittest.TestCase):
    def test_standard_user_file_is_composed(self):
        template = (ROOT / 'src/styles/mdpopups.css').read_text()
        self.assertTrue(template.rstrip().endswith("{{ 'Packages/User/mdpopups.css' | getcss }}"))
        self.assertIn('var.is_popup', template)


class SettingsAndStates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = themes.build_rules(themes.DARK)
        cls.defaults = {'highlight_modified_tabs': True, 'show_tab_close_buttons': True,
                        'show_tab_close_buttons_on_left': False, 'file_tab_style': 'rounded'}

    def resolved(self, control_class, attrs=(), parents=(), values=None):
        values = dict(self.defaults, **(values or {}))
        result = {}

        def attributes(required, actual):
            return all((a[1:] not in actual) if a.startswith('!') else a in actual for a in required)

        for rule in self.rules:
            if not set(rule['class'].split()) <= set(control_class.split()):
                continue
            if not attributes(rule.get('attributes', []), attrs):
                continue
            conditions = rule.get('settings', {})
            if isinstance(conditions, list):
                if not all((not values.get(k[1:], False)) if k.startswith('!') else values.get(k, False)
                           for k in conditions):
                    continue
            else:
                if not all(values.get(k, '') in (v if isinstance(v, list) else [v])
                           for k, v in conditions.items()):
                    continue
            if rule.get('parents'):
                if not all(any(p['class'] == actual_cls and attributes(p.get('attributes', []), actual_attrs)
                               for actual_cls, actual_attrs in parents) for p in rule['parents']):
                    continue
            result.update(rule)
        return result

    def test_dirty_selected_label_obeys_highlight_toggle(self):
        parents=[('tab_control', ['dirty', 'selected'])]
        self.assertEqual(self.resolved('tab_label', parents=parents)['fg'], 'var(jb_link)')
        self.assertEqual(self.resolved('tab_label', parents=parents, values={'highlight_modified_tabs':False})['fg'], 'var(jb_text)')

    def test_dirty_dot_survives_inactive_tab(self):
        self.assertTrue(self.resolved('tab_close_button', parents=[('tab_control',['dirty'])])['layer0.texture'].endswith('tab_dirty.png'))
        self.assertEqual(self.resolved('tab_close_button', values={'show_tab_close_buttons':False})['content_margin'], 0)

    def test_square_has_actual_square_texture(self):
        self.assertTrue(self.resolved('tab_control', attrs=['selected','left_overhang'], values={'file_tab_style':'square'})['layer0.texture'].endswith('tab_square.png'))

    def test_hidden_dropdown_stays_hidden_on_hover(self):
        self.assertEqual(self.resolved('show_tabs_dropdown_button', attrs=['hover'], values={'islands_hide_tab_dropdown':True})['content_margin'], 0)

    def test_disabled_label_and_dialog_press(self):
        self.assertEqual(self.resolved('label_control', parents=[('button_control',['disabled'])])['fg'],'var(jb_text_faint)')
        self.assertEqual(self.resolved('button_control', attrs=['pressed'],parents=[('dialog',[])])['layer0.tint'],'var(jb_accent_soft)')

    def test_every_template_setting_has_chinese_description(self):
        for flavor in ('Dark','Light'):
            text=settings.template(flavor)
            for key in package.load_json(text.encode()):
                self.assertIn(key,settings.SETTINGS)
                self.assertIn('// '+settings.SETTINGS[key][0],text)


if __name__ == '__main__':
    unittest.main()
