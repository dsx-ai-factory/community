#!/usr/bin/env python3
"""Check data/repos.txt against live GitHub state. Read-only, no dependency
on any external scoring tool - pure GitHub REST API via `gh api`.

Detects:
  - a tracked repo that was RENAMED (same org, new repo name)
  - a tracked repo that MOVED to a different org - split into "moved INTO
    dsx-ai-factory" (the migration event this whole index exists to catch)
    vs "moved to some other org" (rarer, still worth a human look)
  - a tracked repo whose archived/visibility status no longer matches what
    data/repos.txt records
  - new repos in dsx-ai-factory not yet tracked in data/repos.txt

Prints a plain-text report. Exit 0 = no drift, 1 = drift found (for cron
alerting), 2 = error.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path.home() / "work" / "community"
DATA_FILE = REPO_ROOT / "data" / "repos.txt"


def gh_api(path):
    result = subprocess.run(
        ["gh", "api", path], capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return None, result.stderr.strip()
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError:
        return None, f"bad JSON from {path}"


def parse_records(text):
    """Minimal parse: section -> list of {name, url, status, ...} dicts."""
    sections = {}
    current = None
    records = []
    lines_buf = []

    def flush():
        if not lines_buf:
            return
        rec = {}
        for line in lines_buf:
            if ":" in line:
                k, _, v = line.partition(":")
                rec[k.strip()] = v.strip()
        if rec:
            records.append(rec)
        lines_buf.clear()

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("## "):
            if current is not None:
                flush()
                sections[current] = records
            current = stripped[3:].strip()
            records = []
            continue
        if current is None:
            continue
        if stripped == "---":
            flush()
            continue
        if not stripped or stripped.startswith("#"):
            continue
        lines_buf.append(stripped)
    if current is not None:
        flush()
        sections[current] = records
    return sections


def owner_repo_from_url(url):
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/?$", url)
    return (m.group(1), m.group(2)) if m else (None, None)


def check_tracked_repos(sections):
    findings = []
    for section in ("dsx-ai-factory", "nvidia-org", "upstream"):
        for rec in sections.get(section) or []:
            owner, repo = owner_repo_from_url(rec.get("url", ""))
            if not owner:
                continue
            data, err = gh_api(f"repos/{owner}/{repo}")
            if err:
                findings.append(f"[{section}] {rec['name']}: API error - {err}")
                continue

            live_owner, live_repo = data["full_name"].split("/", 1)
            expected_full = f"{owner}/{repo}"

            if live_owner.lower() != owner.lower():
                # Org changed - the case this index exists to catch.
                if live_owner.lower() == "dsx-ai-factory" and section != "dsx-ai-factory":
                    findings.append(
                        f"[{section}] {rec['name']}: MOVED INTO dsx-ai-factory - "
                        f"{expected_full} -> {data['full_name']} (belongs in the dsx-ai-factory section now)"
                    )
                else:
                    findings.append(
                        f"[{section}] {rec['name']}: MOVED to a different org - "
                        f"{expected_full} -> {data['full_name']}"
                    )
            elif live_repo.lower() != repo.lower():
                # Same org, name changed - a rename, not a migration.
                findings.append(
                    f"[{section}] {rec['name']}: RENAMED (same org) - "
                    f"{expected_full} -> {data['full_name']}"
                )

            live_archived = data.get("archived", False)
            recorded_archived = "archived" in rec.get("status", "").lower()
            if live_archived != recorded_archived:
                findings.append(
                    f"[{section}] {rec['name']}: archived status changed - "
                    f"live={live_archived}, recorded={recorded_archived}"
                )
            live_vis = data.get("visibility", "unknown")
            recorded_status = rec.get("status", "")
            recorded_internal = "internal" in recorded_status.lower() or "not yet public" in recorded_status.lower()
            if live_vis == "public" and recorded_internal:
                findings.append(
                    f"[{section}] {rec['name']}: now PUBLIC (was recorded as {recorded_status!r}) - {data['full_name']}"
                )
    return findings


def check_new_dsx_ai_factory_repos(sections):
    tracked_urls = {
        rec.get("url", "").lower()
        for rec in (sections.get("dsx-ai-factory") or [])
    }
    data, err = gh_api("orgs/dsx-ai-factory/repos?per_page=100")
    if err:
        return [f"[dsx-ai-factory] could not list org repos - {err}"]
    findings = []
    for repo in data or []:
        url = repo["html_url"].lower()
        name = repo["name"]
        if name.startswith("zz-forkpilot"):
            continue  # known scratch/pilot noise, deliberately excluded
        if url not in tracked_urls:
            findings.append(
                f"[dsx-ai-factory] NEW REPO not tracked: {repo['full_name']} "
                f"(visibility={repo['visibility']}, archived={repo['archived']})"
            )
    return findings


def main():
    if not DATA_FILE.exists():
        print(f"error: {DATA_FILE} not found", file=sys.stderr)
        return 2

    sections = parse_records(DATA_FILE.read_text(encoding="utf-8"))
    findings = check_tracked_repos(sections) + check_new_dsx_ai_factory_repos(sections)

    if findings:
        print(f"DRIFT FOUND ({len(findings)}):")
        for f in findings:
            print(f"  - {f}")
        return 1
    print("OK: no drift detected against data/repos.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
