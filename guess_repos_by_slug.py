#!/usr/bin/env python3
"""Cheap first pass at finding repos for portal programs with no known GitHub
link: try the portal's own 'slug' field (+ a few variants) as a literal repo
name across known DSX-adjacent orgs, using GET /repos/{org}/{repo} existence
checks (fast REST quota, 5000/hr -- NOT the 30/min search endpoint). Only
programs still unresolved after this pass need the slow search fallback."""
import csv
import json
import re
import sqlite3
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(sys.maxsize)

DB_PATH = Path.home() / "work" / "dsx-portal.db"
GH_TOKEN_FILE = Path.home() / ".config" / "dsx-watch" / "gh_token"
CSV_DIR = Path.home() / "work" / "portal-csv-drops"

PRIORITY_ORGS = ["dsx-ai-factory", "NVIDIA", "Mellanox", "ai-dynamo", "run-ai", "leptonai",
                  "kai-scheduler", "kubernetes-sigs", "NVIDIA-Omniverse", "NVIDIA-Omniverse-blueprints",
                  "SlinkyProject"]

# Common portal-slug noise that real repo names usually drop.
STRIP_PREFIXES = ["dsx-os-", "dsx-oss-", "dsx-", "nvidia-", "ncx-"]


def gh_token():
    return GH_TOKEN_FILE.read_text(encoding="utf-8").strip()


def slug_variants(slug):
    variants = {slug}
    for prefix in STRIP_PREFIXES:
        if slug.startswith(prefix):
            variants.add(slug[len(prefix):])
    # collapse doubled dashes, trailing "-api"/"-service" style suffixes left bare
    variants.add(re.sub(r"-+", "-", slug))
    return [v for v in variants if v]


def repo_exists(org, repo, token):
    url = f"https://api.github.com/repos/{org}/{repo}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("html_url")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"  unexpected {e.code} for {org}/{repo}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  error checking {org}/{repo}: {e}", file=sys.stderr)
        return None


def latest_slugs():
    """program_id -> slug, straight from the newest CSV drop (DB doesn't store
    the raw slug column, only the derived fields build_portal_db.py keeps)."""
    candidates = sorted(CSV_DIR.glob("*.csv"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        return {}
    with open(candidates[-1], encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return {r["Program ID"]: r.get("Slug", "") for r in rows if r.get("Program ID")}


def main():
    token = gh_token()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    missing = conn.execute(
        "SELECT program_id, name FROM programs WHERE github_url = '' OR github_url IS NULL"
    ).fetchall()
    slugs = latest_slugs()
    print(f"{len(missing)} programs with no known GitHub URL. Trying slug-guess pass (fast REST, no search quota)...")

    now = datetime.now(timezone.utc).isoformat()
    resolved = 0
    checked = 0
    for row in missing:
        slug = slugs.get(row["program_id"])
        if not slug:
            continue
        found_url = None
        for org in PRIORITY_ORGS:
            for variant in slug_variants(slug):
                checked += 1
                url = repo_exists(org, variant, token)
                if url:
                    found_url = url
                    break
            if found_url:
                break
        if found_url:
            resolved += 1
            print(f"  FOUND {row['name']!r} -> {found_url}")
            conn.execute(
                "INSERT INTO repo_candidates (program_id, candidate_url, confidence, source, discovered_at) "
                "VALUES (?,?,?,?,?)",
                (row["program_id"], found_url, "high", "slug-guess (existence-confirmed)", now),
            )

    conn.commit()
    conn.close()
    print(f"\nSlug-guess pass: {checked} existence checks, {resolved}/{len(missing)} programs resolved.")
    print(f"{len(missing) - resolved} programs remain for the slow search fallback.")


if __name__ == "__main__":
    main()
