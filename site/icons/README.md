# Icon sources

Original SVG exports from NVIDIA's "AI Developer Icon Library" Figma file
(`figma.com/design/A5plgNKROGORaJSveJmUrx`), supplied by the operator 2026-09-08.
`site/render_index.py` reads these as the canonical source and generates two kinds of
output from them:

- **Materials-index diagram bands** (`content/posts/assets/dsx-stack.svg`): a
  background/badge path is stripped and the remaining glyph is recolored to match the
  band it sits on, since it composites onto a solid color rect. See
  `strip_icon_paths()` and `BAND_ICON` in `site/render_index.py`.
- **Category headings** in the materials index listing
  (`content/posts/assets/icons/<slug>.svg`): copied through unmodified — full NVIDIA
  green coloring, since these sit on the page background, not a colored band. See
  `CATEGORY_ICON` in `site/render_index.py`.

These are NVIDIA's own brand assets (first-party, not a third-party dependency in the
OSRB sense), but redistributing them under this repository's CC-BY-4.0 license is a
real change from "zero external assets" — confirm with NVIDIA brand/OSRB before this
repository goes public if that has not already happened.

Do not add more icons here directly; ask the person maintaining this repo for a fresh
export from the source library, so provenance stays traceable to a specific library
version.
