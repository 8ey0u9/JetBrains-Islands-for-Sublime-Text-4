"""Icon regeneration and attribution must remain independent of local IDEs."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from lib import icons, SRC
from lib.package import repository_files


class IconTooling(unittest.TestCase):
    def test_finds_repo_local_renderer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'node_modules/@resvg/resvg-js').mkdir(parents=True)
            with patch.object(icons, 'ROOT', root), \
                    patch.dict(icons.os.environ, {'RESVG_DIR': ''}):
                self.assertEqual(Path(icons.find_resvg()), root.resolve())

    def test_explicit_renderer_location_takes_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            override = Path(directory)
            (override / 'node_modules/@resvg/resvg-js').mkdir(parents=True)
            with patch.dict(icons.os.environ, {'RESVG_DIR': directory}):
                self.assertEqual(Path(icons.find_resvg()), override.resolve())

    def test_renderer_failure_cleans_temporary_files_and_preserves_outputs(self):
        task_files = []
        manifest = SRC / icons.MANIFEST
        original = manifest.read_bytes()

        def fail(command, **kwargs):
            task_files.append(Path(command[-1]))
            self.assertTrue(task_files[-1].exists())
            raise subprocess.CalledProcessError(1, command)

        with tempfile.TemporaryDirectory() as directory:
            module = Path(directory) / 'node_modules/@resvg/resvg-js'
            module.mkdir(parents=True)
            module.joinpath('package.json').write_text('{"version":"2.6.2"}')
            with patch.object(icons, 'find_resvg', return_value=directory), \
                    patch.object(icons.subprocess, 'run', side_effect=fail) as run:
                with self.assertRaises(subprocess.CalledProcessError):
                    icons.build()
                self.assertEqual(run.call_args.args[0][:2], ['node', '-e'])
                self.assertEqual(run.call_args.kwargs['cwd'], directory)
            self.assertFalse(task_files[0].parent.exists())
            self.assertEqual(manifest.read_bytes(), original)


class IconAttribution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = repository_files()
        cls.manifest = json.loads(cls.files[icons.MANIFEST])

    def test_inventory_and_recorded_evidence_validate(self):
        self.assertEqual(icons.validate(self.files), [])

    def test_missing_license_or_notice_is_rejected(self):
        for resource in ('NOTICE', 'docs/LICENSING.md', icons.APACHE_LICENSE):
            with self.subTest(resource=resource):
                files = dict(self.files)
                del files[resource]
                self.assertIn(f'missing licensing resource: {resource}', icons.validate(files))

    def test_missing_upstream_license_evidence_is_rejected(self):
        asset = next(a for a in self.manifest['assets'].values()
                     if a.get('license_evidence', {}).get('type') == 'upstream_repository')
        files = dict(self.files)
        del files[asset['license_evidence']['license']['file']]
        self.assertTrue(any('upstream license evidence missing' in e for e in icons.validate(files)))

    def test_modified_source_is_rejected(self):
        source = next(iter(self.manifest['assets'].values()))['source']
        files = dict(self.files)
        files[source] += b'\n'
        self.assertIn(f'icon source missing or changed: {source}', icons.validate(files))

    def test_png_attribution_is_required_even_when_checksum_matches(self):
        name = next(iter(self.manifest['assets']))
        files = dict(self.files)
        output = f'icons/{name}.png'
        # A non-icon PNG has no source/license metadata.
        files[output] = files['textures/row_pill.png']
        manifest = json.loads(files[icons.MANIFEST])
        manifest['assets'][name]['outputs'][output] = hashlib.sha256(files[output]).hexdigest()
        files[icons.MANIFEST] = json.dumps(manifest).encode()
        self.assertIn(f'{output}: missing or incorrect License metadata', icons.validate(files))

    def test_release_review_rejects_unresolved_licenses_and_name(self):
        errors = icons.validate(self.files, release_ready=True)
        self.assertTrue(any('icon variants need license review' in e for e in errors))
        self.assertTrue(any('independent project/package name' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
