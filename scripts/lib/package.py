"""Build a reproducible release from an explicit runtime/documentation allowlist."""
import hashlib
import json
import posixpath
import re
import struct
import zipfile

from . import ROOT, SRC, icons, schemes, settings, themes

PACKAGE = ROOT / "dist" / "JetBrains Islands.sublime-package"


def package_readme():
    """Use the same installation text, omitting repository-only developer links."""
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    start = text.index("## Documentation and development\n")
    end = text.index("## Credits and license\n", start)
    return text[:start] + text[end:]


def release_files():
    files = {
        name: (ROOT / name).read_bytes()
        for name in (
            "LICENSE", "NOTICE", "README.md", "VERSION",
            "docs/SETTINGS.zh-CN.md", "docs/LICENSING.md",
        )
    }
    for pattern in ("LICENSES/*.txt",):
        for path in ROOT.glob(pattern):
            files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    for pattern in (
        "themes/*.sublime-theme", "themes/*.sublime-file-icons",
        "schemes/*.sublime-color-scheme", "schemes/*.hidden-color-scheme",
        "icons/*.png", "textures/*.png", "settings/*.sublime-settings",
        "settings/*.sublime-commands",
        "styles/mdpopups.css", "styles/popup-dark.css", "styles/popup-light.css",
        "icons/upstream/manifest.json",
        "icons/upstream/licenses/*.txt",
    ):
        for path in SRC.glob(pattern):
            files[path.relative_to(SRC).as_posix()] = path.read_bytes()
    files["README.md"] = package_readme().encode("utf-8")
    return files


def repository_files():
    """Add development docs and SVG evidence for source-only validation."""
    files = release_files()
    for pattern in ("README.md", "docs/*.md"):
        for path in ROOT.glob(pattern):
            files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    for pattern in ("icons/upstream/svg/*.svg",):
        for path in SRC.glob(pattern):
            files[path.relative_to(SRC).as_posix()] = path.read_bytes()
    if (SRC / "styles/popup.css").exists():
        files["styles/popup.css"] = (SRC / "styles/popup.css").read_bytes()
    return files


def release_manifest(files):
    return {
        "version": (ROOT / "VERSION").read_text().strip(),
        "sublime_text": ">=4170",
        "files": {name: hashlib.sha256(content).hexdigest() for name, content in sorted(files.items())},
    }


def build(release_ready=False):
    # Texture rendering needs Pillow; checking an existing tree does not.
    from . import textures

    textures.build()
    themes.build()
    schemes.build_all()
    settings.build()
    check(source_only=True, release_ready=release_ready)
    files = release_files()
    files["release.json"] = (json.dumps(release_manifest(files), indent=2) + "\n").encode()
    PACKAGE.parent.mkdir(exist_ok=True)
    temporary = PACKAGE.with_suffix(".tmp")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, content)
    temporary.replace(PACKAGE)
    check(release_ready=release_ready)
    digest = hashlib.sha256(PACKAGE.read_bytes()).hexdigest()
    PACKAGE.with_suffix(".sublime-package.sha256").write_text(f"{digest}  {PACKAGE.name}\n")
    print(f"Release {release_manifest(files)['version']}: {PACKAGE}")
    print(f"SHA256: {digest}")
    if not release_ready:
        print("Development archive only. Run build --release-ready before public distribution.")


def load_json(content):
    text = content.decode("utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return json.loads(re.sub(r"^\s*//.*$", "", text, flags=re.M))


def validate(files, release_ready=False, verify_sources=True):
    errors = icons.validate(files, release_ready=release_ready, verify_sources=verify_sources)

    def check(condition, message):
        if not condition:
            errors.append(message)

    configs = {}
    for name, content in files.items():
        if name.endswith((".sublime-theme", ".sublime-color-scheme", ".hidden-color-scheme",
                          ".sublime-file-icons", ".sublime-commands", ".sublime-settings")):
            try:
                configs[name] = load_json(content)
            except (ValueError, UnicodeError) as error:
                errors.append(f"{name}: {error}")
        if name.endswith(".py"):
            try:
                compile(content, name, "exec")
            except SyntaxError as error:
                errors.append(f"{name}: {error}")
        if name.endswith(".md"):
            for target in re.findall(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)", content.decode("utf-8")):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith(("#", "//")):
                    continue
                target = target.split("#", 1)[0]
                linked = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                check(linked in files, f"{name}: missing linked resource: {linked}")

    referenced_textures = set()
    for flavor in ("Dark", "Light"):
        theme_name = f"themes/JetBrains Islands {flavor}.sublime-theme"
        scheme_name = f"schemes/JetBrains Islands {flavor}.sublime-color-scheme"
        icons_name = f"themes/JetBrains Islands {flavor}.sublime-file-icons"
        widget_name = f"Widget - JetBrains Islands {flavor}"
        widget_scheme_name = "schemes/" + widget_name + ".hidden-color-scheme"
        widget_settings_name = "settings/" + widget_name + ".sublime-settings"
        for name in (theme_name, scheme_name, icons_name, widget_scheme_name, widget_settings_name):
            check(name in configs, f"missing or invalid {name}")
        widget_settings = configs.get(widget_settings_name, {})
        check(widget_settings.get("color_scheme") == posixpath.basename(widget_scheme_name),
              f"{widget_settings_name}: incorrect widget color-scheme binding")
        theme = configs.get(theme_name, {})
        for rule in theme.get("rules", []):
            for key, value in rule.items():
                if key.endswith(".texture") and isinstance(value, str) and value.startswith("JetBrains Islands/"):
                    resource = value.split("/", 1)[1]
                    referenced_textures.add(resource)
                    check(resource in files, f"{theme_name}: missing {value}")
        for extension, icon in configs.get(icons_name, {}).get("icons", {}).items():
            check(f"icons/{icon}.png" in files, f"{icons_name}: missing icon for {extension}")
        scheme = configs.get(scheme_name, {})
        css = scheme.get("globals", {}).get("popup_css", "")
        check("@@" not in css, f"{scheme_name}: unexpanded CSS tokens")
        check("#ff0000" not in css.lower(), f"{scheme_name}: debug red in popup CSS")
        check(":hover" not in css and "!important" not in css,
              f"{scheme_name}: unsupported minihtml selector/declaration")
        check("phantom_css" in scheme.get("globals", {}), f"{scheme_name}: phantom CSS falls back to popup CSS")
    for name in ("styles/mdpopups.css", "styles/popup-dark.css", "styles/popup-light.css"):
        check(name in files, f"missing popup adapter resource: {name}")

    # Check dimensions in both the source tree and the actual archive.
    for name, content in files.items():
        if not name.startswith(("textures/", "icons/")) or not name.endswith(".png"):
            continue
        check(content[:8] == b"\x89PNG\r\n\x1a\n", f"invalid PNG: {name}")
        if "@" in name or len(content) < 24:
            continue
        if name.startswith("textures/"):
            check(name in referenced_textures, f"unused theme texture: {name}")
        width, height = struct.unpack(">II", content[16:24])
        for scale in (2, 3):
            variant = name[:-4] + f"@{scale}x.png"
            data = files.get(variant, b"")
            check(len(data) >= 24, f"missing PNG variant: {variant}")
            if len(data) >= 24:
                check(struct.unpack(">II", data[16:24]) == (width * scale, height * scale),
                      f"incorrect PNG dimensions: {variant}")
    return errors


def generator_errors(files):
    errors = []
    if files.get("docs/SETTINGS.zh-CN.md") != settings.documentation().encode("utf-8"):
        errors.append("Chinese settings documentation differs from generator")
    for tp, cp in ((themes.DARK, schemes.DARK), (themes.LIGHT, schemes.LIGHT)):
        name = tp["name"]
        expected = {"extends": "Default.sublime-theme",
                    "variables": themes.variables(tp), "rules": themes.build_rules(tp)}
        if load_json(files[f"themes/{name}.sublime-theme"]) != expected:
            errors.append(f"{name}: theme differs from generator")
        expected = {"name": cp["name"], "author": "JetBrains Islands for Sublime Text 4",
                    "variables": schemes.variables_for(cp), "globals": schemes.globals_for(cp),
                    "rules": schemes.rules_for(cp)}
        if load_json(files[f"schemes/{name}.sublime-color-scheme"]) != expected:
            errors.append(f"{name}: scheme differs from generator")
        flavor = "dark" if tp["dark"] else "light"
        if files.get(f"styles/popup-{flavor}.css") != (schemes.popup_css_for(cp) + "\n").encode():
            errors.append(f"{name}: mdpopups CSS differs from generator")
        if files.get(f"settings/{name}.sublime-settings") != settings.template(flavor.title()).encode():
            errors.append(f"{name}: Chinese settings template differs from generator")
        widget = f"Widget - {name}"
        if load_json(files.get("schemes/" + widget + ".hidden-color-scheme", b"{}")) != schemes.widget_data(cp):
            errors.append(f"{name}: widget scheme differs from generator")
        if load_json(files.get("settings/" + widget + ".sublime-settings", b"{}")) != {"color_scheme": widget + ".hidden-color-scheme"}:
            errors.append(f"{name}: widget binding differs from generator")
        expected = {"icons": themes.icon_names("dark" if tp["dark"] else "light")}
        if load_json(files[f"themes/{name}.sublime-file-icons"]) != expected:
            errors.append(f"{name}: icon mapping differs from generator")
    return errors


def check(source_only=False, release_ready=False):
    sources = repository_files()
    files = release_files()
    errors = validate(sources, release_ready=release_ready) + generator_errors(sources)
    errors += validate(files, release_ready=release_ready, verify_sources=False)
    if not source_only:
        if not PACKAGE.exists():
            errors.append("release package not built")
        else:
            with zipfile.ZipFile(PACKAGE) as archive:
                if archive.testzip():
                    errors.append("archive CRC verification failed")
                names = archive.namelist()
                if len(names) != len(set(names)):
                    errors.append("duplicate archive entries")
                packaged = {name: archive.read(name) for name in names}
            errors += ["archive: " + error for error in
                       validate(packaged, release_ready=release_ready, verify_sources=False)]
            expected_names = set(files) | {"release.json"}
            if set(packaged) != expected_names:
                errors.append(f"archive inventory differs: {sorted(set(packaged) ^ expected_names)}")
            for name, content in files.items():
                if packaged.get(name) != content:
                    errors.append(f"archive differs from source: {name}")
            try:
                manifest = json.loads(packaged.get("release.json", b"{}"))
                if manifest != release_manifest(files):
                    errors.append("release manifest differs from current source")
                for name, digest in manifest.get("files", {}).items():
                    if hashlib.sha256(packaged.get(name, b"")).hexdigest() != digest:
                        errors.append(f"archive checksum mismatch: {name}")
            except ValueError:
                errors.append("invalid release manifest")
    if errors:
        print("\n".join("FAIL " + error for error in errors))
        raise SystemExit(1)
    print("all checks passed: JSON, generators, runtime assets, attribution inventory, 1x/2x/3x" +
          ("" if source_only else ", archive contents and SHA256 manifest"))
    if not release_ready:
        print("This checks recorded evidence and integrity, not publication clearance; use --release-ready for that gate.")

