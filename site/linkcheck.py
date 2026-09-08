#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: CC-BY-4.0
"""Check links in published articles. Dependency-free — see site/build.py.

Internal links (relative paths and links into this repo's own docs/ output) must
resolve, or the build fails. External links are checked too, but a failure or
timeout there is a warning, not a build failure — this repo does not control
upstream availability and should not go red because someone else's site is down.

Usage:
    python3 site/linkcheck.py               # internal links only, exit non-zero on break
    python3 site/linkcheck.py --external     # also probe external links (slower, network)
"""

import argparse
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "posts"

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
MD_LINK_TARGET = re.compile(r"^(?P<path>[^#]*)(?:#(?P<anchor>.*))?$")


def internal_target_exists(path, target):
    """Resolve a relative Markdown link from the file that contains it."""
    clean = MD_LINK_TARGET.match(target).group("path")
    if not clean:
        return True  # pure in-page anchor, e.g. "#section"
    resolved = (path.parent / clean).resolve()
    return resolved.exists()


def probe_external(url, timeout=10):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "dsx-community-linkcheck"})
    try:
        with urllib.request.urlopen(req, timeout=timeout):
            return True, None
    except urllib.error.HTTPError as exc:
        # Some hosts reject HEAD but serve GET fine (e.g. 405/403 from a WAF).
        if exc.code in (403, 405):
            return True, None
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 - network is inherently varied
        return False, str(exc)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--external", action="store_true", help="also probe external links (network required)")
    args = ap.parse_args()

    if not CONTENT.is_dir():
        print("No articles yet: nothing to check.")
        return 0

    broken_internal = []
    external_warnings = []
    checked_external = set()

    for path in sorted(CONTENT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        # Skip fenced/inline code so a doc's illustrative link syntax (e.g. this
        # very script's own README explaining Markdown image syntax) is not
        # itself resolved as a real link.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`]*`", "", text)
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://")):
                if args.external and target not in checked_external:
                    checked_external.add(target)
                    ok, detail = probe_external(target)
                    if not ok:
                        external_warnings.append(f"{path.relative_to(ROOT)}: {target} ({detail})")
                continue
            if target.startswith(("mailto:", "#")):
                continue
            if not internal_target_exists(path, target):
                broken_internal.append(f"{path.relative_to(ROOT)}: {target}")

    if external_warnings:
        print("warning: external link(s) did not respond cleanly (not build-blocking):")
        for w in external_warnings:
            print(f"  {w}")

    if broken_internal:
        print("error: broken internal link(s):", file=sys.stderr)
        for b in broken_internal:
            print(f"  {b}", file=sys.stderr)
        return 1

    print("OK: no broken internal links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
