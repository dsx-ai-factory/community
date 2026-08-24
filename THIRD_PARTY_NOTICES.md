# Third-Party Notices

This repository publishes NVIDIA-authored and community-contributed articles and hosts
discussions. It contains no product source code.

## Third-party components

**None.** As of the initial release, this repository declares no third-party
dependencies, vendors no third-party code, and includes no copied third-party source.
The site published from this repository is built without a third-party theme, static
site generator, or package manager, so there is no dependency manifest to enumerate.

`site/build.py` uses only the Python standard library. The page shell in
`site/template.html` is hand-written: no framework, no webfont, no analytics, no
third-party stylesheet or script is loaded by the published pages.

## Services used at build time

These are network services called during the build, not components distributed with
the content and not code vendored into this repository. They are recorded here for
completeness rather than as license obligations.

| Service | Used for |
| --- | --- |
| GitHub Markdown API (`api.github.com/markdown`) | Rendering GitHub Flavored Markdown to HTML, so that no Markdown library has to be added as a dependency |
| GitHub Pages | Serving the contents of `docs/` |

## When this file must be updated

Add an entry here whenever any of the following enters the repository:

- A declared dependency — anything that would appear in a `Gemfile`, `package.json`,
  `requirements.txt`, or equivalent manifest.
- Third-party code copied into the repository, in whole or in part, including a
  template, theme, stylesheet, or script obtained from another project.
- A vendored component.
- Third-party text, figures, or images reproduced in an article beyond what plain
  attribution covers.

Each entry must record the component name, version, license, and a link to its
license text. Preserve upstream copyright notices exactly as they appear — do not
edit their wording, formatting, or dates.

Adding any of the above is also a trigger to re-open the repository's Open Source
Review Board approval, since the approved request records this project as having no
third-party dependencies.

## Attribution of quoted material

Articles that quote or adapt third-party material must attribute it inline, at the
point of use, and link to the source. Contributors are responsible for confirming
the source's license permits the use.
