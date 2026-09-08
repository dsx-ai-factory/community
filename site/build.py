#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: CC-BY-4.0
"""Build the community site from Markdown articles.

Deliberately dependency-free. This script uses only the Python standard library.
Output lands in ``docs/`` (``.gitignore``d, not committed) with ``.nojekyll`` set,
and ``.github/workflows/pages.yml`` uploads it as a Pages artifact and deploys it
on every merge to main — no Jekyll, no theme, no gems, no static site generator,
no package manifest.

That is not an aesthetic choice. The repository's Open Source Review Board
approval records this project as having **no third-party dependencies**. Adding a
theme or a site generator would contradict that record and require re-opening the
approval before the site could ship. See THIRD_PARTY_NOTICES.md.

Markdown is rendered by GitHub's own ``/markdown`` API, so articles get real
GitHub Flavored Markdown without vendoring a Markdown library. That is a service
call, not a bundled component.

Usage:
    GH_TOKEN=<token> python3 site/build.py
    python3 site/build.py --check      # validate front matter only, render nothing

A token is needed only for the rendering API. Any token with public read scope
works; ``gh auth token`` supplies one.
"""

import argparse
import datetime
import html
import json
import os
import pathlib
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "posts"
OUT = ROOT / "docs"
TEMPLATE = ROOT / "site" / "template.html"

REQUIRED_FIELDS = ("title", "date", "authors", "type", "last_reviewed")
OPTIONAL_FIELDS = ("component", "tier", "pillar", "draft", "status", "superseded_by")
VALID_TYPES = {
    "release-post",
    "deep-dive",
    "how-to",
    "success-story",
    "event",
    "exploratory",
    "spotlight",
    # Not one of the POR's seven content types. It points at other repos rather
    # than narrating, and the POR has not ruled on whether it gets a type of its
    # own or is "furniture that happens to have a post URL" (90-day plan, s.3).
    # Treated as its own type until that ruling lands — see GOVERNANCE.md.
    "index",
}
VALID_TIERS = {"1", "2", "3"}
STALE_AFTER_DAYS = 365


class BuildError(Exception):
    """A problem the author must fix. Never rendered into the site."""


def parse_front_matter(text, path):
    """Pull the ``---`` delimited header off an article.

    Intentionally not YAML: the format is ``key: value``, one per line, so that
    no YAML parser has to be added as a dependency.
    """
    if not text.startswith("---\n"):
        raise BuildError(f"{path}: missing front matter (file must start with '---')")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise BuildError(f"{path}: front matter is not closed with '---'")

    meta = {}
    for lineno, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise BuildError(f"{path}:{lineno}: front matter line is not 'key: value': {line!r}")
        key, _, value = line.partition(":")
        key = key.strip()
        if key in meta:
            # A silent overwrite here could let e.g. a duplicate `draft:` line
            # mask the intended value and publish something meant to stay
            # draft (CodeRabbit finding, 2026-09-08).
            raise BuildError(f"{path}:{lineno}: front matter has {key!r} more than once")
        meta[key] = value.strip()

    body = text[end + len("\n---\n"):]
    return meta, body


def validate(meta, path):
    missing = [f for f in REQUIRED_FIELDS if f not in meta or not meta[f]]
    if missing:
        raise BuildError(f"{path}: front matter missing required field(s): {', '.join(missing)}")

    unknown = [k for k in meta if k not in REQUIRED_FIELDS and k not in OPTIONAL_FIELDS]
    if unknown:
        raise BuildError(f"{path}: unrecognized front matter field(s): {', '.join(unknown)}")

    if meta["type"] not in VALID_TYPES:
        raise BuildError(
            f"{path}: type {meta['type']!r} is not one of: {', '.join(sorted(VALID_TYPES))}"
        )

    for field in ("date", "last_reviewed"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta[field]):
            raise BuildError(f"{path}: {field} must be YYYY-MM-DD, got {meta[field]!r}")
        try:
            datetime.date.fromisoformat(meta[field])
        except ValueError as exc:
            raise BuildError(f"{path}: {field} is not a real date: {exc}") from exc

    if "tier" in meta and meta["tier"] not in VALID_TIERS:
        raise BuildError(f"{path}: tier must be one of {sorted(VALID_TIERS)}, got {meta['tier']!r}")

    if "draft" in meta and meta["draft"].lower() not in ("true", "false"):
        raise BuildError(f"{path}: draft must be 'true' or 'false', got {meta['draft']!r}")

    if "status" in meta and meta["status"] not in ("outdated", "archived"):
        # A typo here (e.g. "outdate") previously passed silently and just
        # never rendered the staleness banner the author intended
        # (CodeRabbit finding, 2026-09-08).
        raise BuildError(
            f"{path}: status must be 'outdated' or 'archived' if set, got {meta['status']!r}"
        )

    return meta


def is_draft(meta):
    """Draft Mode (90-day plan, s.6): draft: true excludes a post from the build.

    A review queue, not a staging area — the article still ships in the pull
    request and still passes front matter validation, it just does not render
    until someone flips the flag.
    """
    return meta.get("draft", "false").lower() == "true"


# Excludes any URI scheme (not just http(s)/mailto — ftp:, tel:, etc.) and
# protocol-relative URLs (//host/...), not just http(s)/mailto specifically
# (CodeRabbit finding, 2026-09-08).
MD_LINK_RE = re.compile(r"\]\((?![A-Za-z][A-Za-z0-9+.\-]*:|//)([^)\s#]+)\.md(#[^)\s]*)?\)")


def rewrite_md_links(body, article_path, draft_targets):
    """Relative links between articles are written as ``other-post.md`` in the
    source, so they resolve correctly when viewed on GitHub directly — but the
    published site only has the rendered ``.html``. Rewrite them at build time
    rather than asking authors to write two different link forms.

    Also warns (does not fail the build) when a published article links to
    another article that is still ``draft: true`` — that link will 404 on the
    live site, since the draft target is never rendered (CodeRabbit finding,
    2026-09-08: this repo's own materials-index post is linked from other
    articles while itself in draft).
    """

    def replace(match):
        target, anchor = match.group(1), match.group(2) or ""
        resolved = (article_path.parent / f"{target}.md").resolve()
        if resolved in draft_targets:
            print(
                f"warning: {article_path.relative_to(ROOT)} links to {target}.md, "
                "which is still draft: true and will not be published (this link will 404)",
                file=sys.stderr,
            )
        return f"]({target}.html{anchor})"

    return MD_LINK_RE.sub(replace, body)


def staleness(meta):
    """Return a banner for content the governance policy says to mark, or None.

    Outdated articles are marked, never deleted — published URLs stay resolvable.
    See GOVERNANCE.md.
    """
    if meta.get("status") == "archived":
        return "This article describes a component that has been retired. It is kept for reference."
    if meta.get("status") == "outdated":
        note = meta.get("superseded_by")
        tail = ""
        if note:
            # html.escape() alone does not stop a javascript:/data: URI from
            # being a live href — only an absolute https:// URL is safe to
            # render as a link here (CodeRabbit finding, 2026-09-08, XSS).
            if urllib.parse.urlparse(note).scheme == "https":
                tail = f' Current material: <a href="{html.escape(note)}">{html.escape(note)}</a>.'
            else:
                tail = f" Current material: {html.escape(note)}."
        return "The commands, versions, or prerequisites in this article are no longer accurate." + tail

    reviewed = datetime.date.fromisoformat(meta["last_reviewed"])
    age = (datetime.date.today() - reviewed).days
    if age > STALE_AFTER_DAYS:
        return (
            f"This article has not been reviewed in {age} days. "
            "It may no longer reflect current versions or behaviour."
        )
    return None


def render_markdown(md, token):
    """Render GFM through GitHub's API. No Markdown library is vendored."""
    payload = json.dumps({"text": md, "mode": "gfm"}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/markdown",
        data=payload,
        headers={
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "dsx-ai-factory-community-site-build",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:200]
        raise BuildError(f"GitHub markdown API returned {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise BuildError(f"could not reach the GitHub markdown API: {exc.reason}") from exc


def page(template, *, title, body, banner=None, meta=None, is_index=False):
    banner_html = ""
    if banner:
        banner_html = f'<div class="banner" role="note">{banner}</div>'

    byline = ""
    if meta and not is_index:
        byline = (
            f'<p class="byline">{html.escape(meta["authors"])} &middot; '
            f'<time datetime="{meta["date"]}">{meta["date"]}</time> &middot; '
            f'{html.escape(meta["type"])}</p>'
        )

    return (
        template.replace("{{TITLE}}", html.escape(title))
        .replace("{{BANNER}}", banner_html)
        .replace("{{BYLINE}}", byline)
        .replace("{{BODY}}", body)
        .replace("{{YEAR}}", str(datetime.date.today().year))
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--check",
        action="store_true",
        help="validate front matter and exit without rendering (needs no token)",
    )
    args = ap.parse_args()

    if not CONTENT.is_dir():
        print(f"No articles yet: {CONTENT} does not exist.", file=sys.stderr)
        return 0

    articles = sorted(CONTENT.rglob("*.md"))
    articles = [a for a in articles if a.name.upper() != "README.MD"]

    parsed, errors = [], []
    for path in articles:
        try:
            meta, body = parse_front_matter(path.read_text(encoding="utf-8"), path.relative_to(ROOT))
            validate(meta, path.relative_to(ROOT))
            parsed.append((path, meta, body))
        except BuildError as exc:
            errors.append(str(exc))

    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    if args.check:
        drafts = sum(1 for _, meta, _ in parsed if is_draft(meta))
        print(f"OK: {len(parsed)} article(s) have valid front matter ({drafts} in draft).")
        return 0

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    template = TEMPLATE.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    draft_count = sum(1 for _, meta, _ in parsed if is_draft(meta))
    published = [p for p in parsed if not is_draft(p[1])]
    draft_targets = {p.resolve() for p, meta, _ in parsed if is_draft(meta)}

    pinned_rows, index_rows = [], []
    for path, meta, body in sorted(published, key=lambda p: p[1]["date"], reverse=True):
        slug = path.relative_to(CONTENT).with_suffix(".html")
        dest = OUT / slug
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            page(
                template,
                title=meta["title"],
                body=render_markdown(rewrite_md_links(body, path, draft_targets), token),
                banner=staleness(meta),
                meta=meta,
            ),
            encoding="utf-8",
        )
        # URL-encode before HTML-escaping: the slug comes from the article's own
        # filename, and an unescaped quote there could break out of the href
        # attribute (CodeRabbit finding, 2026-09-08, XSS).
        href = html.escape(urllib.parse.quote(slug.as_posix()))
        row = (
            f'<li><a href="{href}">{html.escape(meta["title"])}</a>'
            f'<span class="meta">{meta["date"]} &middot; {html.escape(meta["type"])}</span></li>'
        )
        # The "index" type (90-day plan, s.4: "Post 2, the Pinned Index") is
        # pinned above the chronological feed rather than sorted into it by
        # date, so it stays the first thing a homepage visitor sees.
        (pinned_rows if meta["type"] == "index" else index_rows).append(row)
        print(f"built {slug.as_posix()}")

        # Copy an article's own assets/ directory (images referenced by relative
        # path, e.g. ![...](assets/foo.svg)) alongside its rendered HTML. Draft
        # articles are skipped entirely above, so a draft's assets are not
        # published early either.
        assets_dir = path.parent / "assets"
        if assets_dir.is_dir():
            shutil.copytree(assets_dir, dest.parent / "assets", dirs_exist_ok=True)
            print(f"copied {assets_dir.relative_to(ROOT)} -> {(dest.parent / 'assets').relative_to(OUT)}")

    body_parts = [
        "<p>Articles and discussion about the open-source components of the "
        "NVIDIA DSX AI Factory.</p>"
    ]
    if pinned_rows:
        body_parts.append('<ul class="index index-pinned">\n' + "\n".join(pinned_rows) + "\n</ul>")
    if index_rows:
        body_parts.append('<ul class="index">\n' + "\n".join(index_rows) + "\n</ul>")
    elif not pinned_rows:
        body_parts.append(
            "<p>No articles have been published yet. "
            '<a href="https://github.com/dsx-ai-factory/community/discussions">'
            "Join the discussion</a> in the meantime.</p>"
        )

    (OUT / "index.html").write_text(
        page(
            template,
            title="DSX AI Factory Community",
            body="\n".join(body_parts),
            is_index=True,
        ),
        encoding="utf-8",
    )
    print(
        f"built index.html ({len(index_rows)} article(s), {len(pinned_rows)} pinned, "
        f"{draft_count} draft(s) excluded)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
