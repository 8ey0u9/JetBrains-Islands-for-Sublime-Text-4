"""Render recorded icon sources and validate their attribution and integrity."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import re
import struct

from . import ROOT, SRC

MANIFEST = "icons/upstream/manifest.json"
APACHE_LICENSE = "LICENSES/Apache-2.0.txt"
APACHE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"


def png_metadata(asset, size):
    origin = asset["origin"]
    source = origin.get("verified_public_source") or (
        f'{origin["product"]} {origin["version"]} ({origin["build"]}); '
        f'{origin["archive"]}!/{origin["entry"]}'
    )
    metadata = {
        "License": asset["license"] or "NOASSERTION",
        "Source": source,
        "Comment": (
            f"Modified by this project's build tools: rasterized from SVG to {size}x{size} PNG. "
            "No intentional color or shape edits. See NOTICE and docs/LICENSING.md."
        ),
    }
    if asset["copyright_notice"]:
        metadata["Copyright"] = asset["copyright_notice"]
    return metadata


def read_png_text(data):
    """Read the uncompressed text chunks written by the icon generator."""
    result = {}
    offset = 8
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 8 + length
        if end + 4 > len(data):
            break
        if kind == b"tEXt" and b"\0" in data[offset + 8:end]:
            key, value = data[offset + 8:end].split(b"\0", 1)
            result[key.decode("latin-1")] = value.decode("latin-1")
        offset = end + 4
    return result


def validate(files, release_ready=False, verify_sources=True):
    errors = []
    for name in ("LICENSE", "NOTICE", "docs/LICENSING.md", APACHE_LICENSE, MANIFEST):
        if not files.get(name):
            errors.append(f"missing licensing resource: {name}")
    if hashlib.sha256(files.get(APACHE_LICENSE, b"")).hexdigest() != APACHE_SHA256:
        errors.append("Apache-2.0 license text differs from the official copy")
    try:
        manifest = json.loads(files.get(MANIFEST, b"{}"))
    except (ValueError, UnicodeError):
        return errors + ["invalid icon provenance manifest"]
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("assets"), dict):
        return errors + ["unsupported icon provenance manifest"]

    outputs = set()
    sources = set()
    pending = []
    for name, asset in manifest["assets"].items():
        if not re.fullmatch(r"file_type_(dark|light)_[a-z0-9]+", name):
            errors.append(f"invalid icon identifier: {name}")
            continue
        source = asset.get("source", "")
        sources.add(source)
        content = files.get(source, b"")
        if verify_sources and (
            not content or hashlib.sha256(content).hexdigest() != asset.get("source_sha256")
        ):
            errors.append(f"icon source missing or changed: {source}")
        license_id = asset.get("license")
        if license_id is None:
            pending.append(name)
        elif license_id != "Apache-2.0":
            errors.append(f"{name}: unreviewed license identifier: {license_id}")
        else:
            notice = asset.get("copyright_notice")
            evidence = asset.get("license_evidence", {})
            if evidence.get("type") == "source_header":
                if not notice or "Apache 2.0" not in notice or (
                    verify_sources and notice.encode("utf-8") not in content
                ):
                    errors.append(f"{name}: Apache declaration is not backed by the source SVG")
            elif evidence.get("type") == "upstream_repository":
                source_url = evidence.get("source_url", "")
                match = re.fullmatch(
                    r"https://github.com/JetBrains/intellij-community/blob/([a-f0-9]{40})/(.+)",
                    source_url,
                )
                if not match or evidence.get("source_sha256") != asset.get("source_sha256"):
                    errors.append(f"{name}: missing pinned upstream source evidence")
                for kind, upstream_name in (("license", "LICENSE.txt"), ("notice", "NOTICE.txt")):
                    record = evidence.get(kind, {})
                    text = files.get(record.get("file"), b"")
                    if not text or hashlib.sha256(text).hexdigest() != record.get("sha256"):
                        errors.append(f"{name}: upstream {kind} evidence missing or changed")
                    if match and record.get("url") != (
                        f"https://github.com/JetBrains/intellij-community/blob/{match[1]}/{upstream_name}"
                    ):
                        errors.append(f"{name}: upstream {kind} does not match the source revision")
                    if kind == "license" and hashlib.sha256(text).hexdigest() != APACHE_SHA256:
                        errors.append(f"{name}: upstream license is not the recorded Apache-2.0 text")
                    if kind == "notice" and (not notice or notice.encode("utf-8") not in text):
                        errors.append(f"{name}: attribution is not backed by the upstream NOTICE")
            else:
                errors.append(f"{name}: missing license evidence")

        expected = {f"icons/{name}{suffix}.png" for suffix in ("", "@2x", "@3x")}
        if set(asset.get("outputs", {})) != expected:
            errors.append(f"{name}: incomplete PNG provenance")
        for path, digest in asset.get("outputs", {}).items():
            if path in outputs:
                errors.append(f"duplicate icon provenance: {path}")
            outputs.add(path)
            data = files.get(path, b"")
            if not data or hashlib.sha256(data).hexdigest() != digest:
                errors.append(f"icon PNG missing or changed: {path}")
            size = 48 if "@3x" in path else 32 if "@2x" in path else 16
            metadata = read_png_text(data)
            for key, value in png_metadata(asset, size).items():
                if metadata.get(key) != value:
                    errors.append(f"{path}: missing or incorrect {key} metadata")

    actual = {name for name in files if name.startswith("icons/") and name.endswith(".png")}
    if outputs != actual:
        errors.append(f"icon provenance inventory differs: {sorted(outputs ^ actual)}")
    actual_sources = {name for name in files
                      if name.startswith("icons/upstream/svg/") and name.endswith(".svg")}
    if verify_sources and sources != actual_sources:
        errors.append(f"icon source inventory differs: {sorted(sources ^ actual_sources)}")
    if release_ready:
        if pending:
            icons = sorted({name.split("_", 3)[-1] for name in pending})
            errors.append(f"publication blocked: {len(pending)} icon variants need license review: {', '.join(icons)}")
        if manifest.get("publication_review", {}).get("branding_clearance") is None:
            errors.append("publication blocked: choose an independent project/package name or record JetBrains naming permission")
    return errors


RENDERER = r"""
const fs = require('fs');
const { Resvg } = require('@resvg/resvg-js');
for (const task of JSON.parse(fs.readFileSync(process.argv[1], 'utf8'))) {
  const svg = fs.readFileSync(task.source, 'utf8');
  for (const [size, suffix] of [[16, ''], [32, '@2x'], [48, '@3x']]) {
    fs.writeFileSync(task.output + suffix + '.png',
      new Resvg(svg, { fitTo: { mode: 'width', value: size } }).render().asPng());
  }
}
"""


def find_resvg():
    for candidate in (os.environ.get("RESVG_DIR"), ROOT):
        if candidate and (Path(candidate) / "node_modules/@resvg/resvg-js").is_dir():
            return str(Path(candidate).resolve())
    return None


def build(check=False):
    from PIL import Image, PngImagePlugin

    module_root = find_resvg()
    if not module_root:
        raise SystemExit("Install @resvg/resvg-js@2.6.2 locally, or set RESVG_DIR to its module root.")
    version = json.loads((Path(module_root) / "node_modules/@resvg/resvg-js/package.json").read_text())["version"]
    manifest_path = SRC / MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if version != manifest["renderer"]["version"]:
        raise SystemExit(f"Renderer version differs from the manifest: {version}")

    with tempfile.TemporaryDirectory(prefix="islands-icons-") as directory:
        temporary = Path(directory)
        tasks = []
        for name, asset in manifest["assets"].items():
            source = SRC / asset["source"]
            if hashlib.sha256(source.read_bytes()).hexdigest() != asset["source_sha256"]:
                raise SystemExit(f"Review the changed SVG and its license before rendering: {source}")
            tasks.append({"source": str(source), "output": str(temporary / name)})
        task_file = temporary / "tasks.json"
        task_file.write_text(json.dumps(tasks), encoding="utf-8")
        subprocess.run(["node", "-e", RENDERER, str(task_file)], cwd=module_root, check=True)

        generated = {}
        for name, asset in manifest["assets"].items():
            for size, suffix in ((16, ""), (32, "@2x"), (48, "@3x")):
                path = temporary / f"{name}{suffix}.png"
                info = PngImagePlugin.PngInfo()
                for key, value in png_metadata(asset, size).items():
                    info.add_text(key, value)
                with Image.open(path) as image:
                    image.load()
                    image.save(path, pnginfo=info)
                relative = f"icons/{path.name}"
                generated[relative] = path.read_bytes()
                if check:
                    if generated[relative] != (SRC / relative).read_bytes():
                        raise SystemExit(f"Generated icon differs: {relative}")
                else:
                    asset["outputs"][relative] = hashlib.sha256(generated[relative]).hexdigest()
        if not check:
            for relative, content in generated.items():
                (SRC / relative).write_bytes(content)
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{'Checked' if check else 'Rendered'} {len(generated)} attributed PNGs; license review status is unchanged.")

