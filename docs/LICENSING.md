# Licensing, third-party resources and publication

## License scope

Original code, documentation, theme rules and textures use the [MIT license](../LICENSE).
Third-party icons retain their own rights. [NOTICE](../NOTICE) preserves upstream
attribution and modification statements; [Apache-2.0](../LICENSES/Apache-2.0.txt)
is included for icons with established Apache licensing evidence.

## JetBrains file icons

The 42 file-icon types have 84 Dark/Light variant records and 252 PNGs.
The [asset manifest](../icons/upstream/manifest.json) records each
source location, IDE build/archive entry, source and PNG SHA256, copyright
notice, license evidence and any verified public source URL.

The recorded sources come from IntelliJ IDEA 2026.3 build 263.7307.200's platform
icon archive and JavaScript plugin resources. Origin in an IDE archive is not
itself a redistribution grant.

| Variants | Evidence | Treatment |
|---|---|---|
| 62 | Original SVGs contain explicit Apache declarations | Apache-2.0; retain the individual copyright notices |
| 10 | Go, PHP, Ruby, Rust and Scala sources match a pinned Apache-licensed upstream revision byte-for-byte | Apache-2.0; retain its LICENSE and NOTICE |
| 12 | Bazel, C, C++, C#, Swift and Vue, each in Dark/Light, lack sufficient recorded license evidence | Pending review; `license: null` in the manifest and `NOASSERTION` in PNG metadata |

The ten repository-licensed variants match upstream revision
`73d2a5cb3bf446179262dc40e47cd20f307a410b`. Its
[LICENSE](../icons/upstream/licenses/intellij-community-LICENSE.txt)
and [NOTICE](../icons/upstream/licenses/intellij-community-NOTICE.txt)
are retained verbatim. Explicit source notices identify JetBrains s.r.o. and
contributors with their original year ranges, preserved individually.

### Conversion and attribution

Source SVGs were rasterized into 16×16, 32×32 and 48×48 PNGs, without intentional
colour or geometry edits. PNG text metadata identifies the source, license
status, available copyright notice and rasterization modification. Dark variants
use the recorded dark artwork where available; shared sources are identified in
the manifest.

Original SVGs and development tools stay in the source repository. The install
archive includes PNGs, this document, `LICENSE`, `NOTICE`, `LICENSES/`, the
attribution manifest and relevant upstream license/NOTICE texts. Source evidence
is checked before packaging; PNG attribution and hashes are checked in the archive.

Apache-2.0 section 4 addresses license copies, retained notices and modification
statements; section 6 does not grant general trademark rights. For new assets,
record the stable source, original file and hash, exact license/copyright/NOTICE
evidence, transformations and output hashes. A public URL or an IDE installation
alone does not establish permission. `NOASSERTION` is a review marker, not a license.

## Other referenced components

| Component | Relationship |
|---|---|
| Sublime Text `Theme - Default` | Theme inheritance and runtime texture paths; application assets are not bundled |
| LSP and mdpopups | Optional integrations; their code is not bundled or patched |
| Pillow and `@resvg/resvg-js` | Separately installed development tools; libraries are not bundled |
| IntelliJ Islands appearance | Visual reference for independently authored rules and textures |

Review any additional copied code or artwork separately before adding it.

## Project identity and publication status

**The source repository and development archive are not yet cleared for public
distribution.** Two items remain:

1. Confirm the applicable license/permission for the 12 pending icon variants
   (36 PNGs), or replace them with appropriately licensed artwork. A missing
   header does not prove reuse is forbidden; the evidence remains incomplete.
2. Choose an independent project/package name and update resource paths, or
   obtain appropriate written permission for the current name containing
   `JetBrains`. The [JetBrains Brand Guidelines](https://www.jetbrains.com/company/brand/)
   restrict use of brand assets in names of third-party offerings. An affiliation
   disclaimer alone does not resolve naming permission.

The manifest's `publication_review.branding_clearance` stays `null` until the
name is reviewed. Record the independent name or permission reference only after
that review; do not set the field just to bypass validation.

JetBrains, IntelliJ IDEA and other JetBrains product names are trademarks of
[JetBrains s.r.o.](https://www.jetbrains.com/). Other names and file-type symbols
remain the property of their owners. This project is independent of JetBrains
and Sublime HQ, with no affiliation, sponsorship or endorsement. No JetBrains
IDE product logos, splash screens or company logo files are intentionally
bundled as standalone assets; file-type symbols may still represent third-party marks.

## Release checks

From the source repository:

```bash
python scripts/manage.py build
python scripts/manage.py test
python scripts/manage.py build --release-ready
```

The default build creates a development archive. The final command checks the
outstanding rights/name review before packaging and must pass before public
distribution. Automated checks verify recorded evidence and integrity; they do
not replace the maintainer's rights review or legal advice on unresolved cases.

## Primary sources

- [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- [JetBrains Brand Guidelines](https://www.jetbrains.com/company/brand/)
- [IntelliJ upstream NOTICE](https://github.com/JetBrains/intellij-community/blob/b131167ab6e123d544b9bc1e53688eb5a9e27c62/NOTICE.txt)
- [Apache license at the matching upstream revision](https://github.com/JetBrains/intellij-community/blob/73d2a5cb3bf446179262dc40e47cd20f307a410b/LICENSE.txt)
- [Platform icon implementation guide](https://plugins.jetbrains.com/docs/intellij/icons.html) — technical guidance, not a blanket redistribution grant.
