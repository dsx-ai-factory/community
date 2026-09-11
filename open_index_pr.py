#!/usr/bin/env python3
"""Turn drift findings into action. Two tracks, matching the original
proposal: mechanical fixes become a PR (never auto-merged); anything needing
editorial judgment becomes an issue for a human to triage.

Auto-fixable via a single-line edit to data/repos.txt (url: and/or status:):
  RENAMED, MOVED (any org), archived status changed, now-public.
  "MOVED INTO dsx-ai-factory" still only gets its url/status line-edited in
  place - relocating the record's text block to the dsx-ai-factory section
  is left for the human reviewer, on purpose: that's a structural edit this
  script has no business making unattended.

NOT auto-fixed, becomes a triage issue instead:
  NEW REPO - category/license/description need a human's judgment, not a
  guess.

Dedup: this runs nightly via cron. Before opening anything, checks for an
already-open PR/issue from a prior run and skips re-filing - a finding that
persists because yesterday's PR hasn't been merged yet should not spawn a
second PR tonight.

Usage:
    python3 open_index_pr.py            # dry-run: show what would happen
    python3 open_index_pr.py --apply    # actually branch/commit/push/open
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_drift as cd  # noqa: E402

REPO_ROOT = cd.REPO_ROOT
DATA_FILE = cd.DATA_FILE
BOT_MARKER = "<!-- filed automatically by DSX Repo Watch -->"
PR_TITLE_PREFIX = "chore: automated index update"
ISSUE_TITLE_PREFIX = "New untracked repo:"


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, **kw)


def has_open_pr_from_bot():
    res = run(["gh", "pr", "list", "--state", "open", "--json", "title,body", "--limit", "50"])
    if res.returncode != 0:
        return False  # can't tell - fail open rather than silently never running
    try:
        prs = json.loads(res.stdout)
    except json.JSONDecodeError:
        return False
    return any(
        p["title"].startswith(PR_TITLE_PREFIX) and BOT_MARKER in (p.get("body") or "")
        for p in prs
    )


def open_issue_titles():
    res = run(["gh", "issue", "list", "--state", "open", "--json", "title", "--limit", "100"])
    if res.returncode != 0:
        return set()
    try:
        return {i["title"] for i in json.loads(res.stdout)}
    except json.JSONDecodeError:
        return set()


def classify(findings):
    line_edits, new_repos = [], []
    for f in findings:
        if "NEW REPO" in f:
            new_repos.append(f)
        else:
            line_edits.append(f)
    return line_edits, new_repos


def apply_line_edit(text, name, new_url=None, new_status=None):
    """Find the record whose `name:` line matches, and rewrite its url:/status:
    line within that record's block only (bounded by the next `---` or `## `).
    """
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"name: {name}":
            start = i
            break
    if start is None:
        return text, False
    end = len(lines)
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if s == "---" or s.startswith("## "):
            end = i
            break
    changed = False
    for i in range(start, end):
        if new_url and lines[i].startswith("url:"):
            lines[i] = f"url: {new_url}"
            changed = True
        if new_status and lines[i].startswith("status:"):
            lines[i] = f"status: {new_status}"
            changed = True
    return "\n".join(lines), changed


def finding_to_edit(finding_line):
    """Parse one finding string back into (name, new_url, new_status)."""
    m = re.match(r"\[(\S+)\] ([^:]+): (.+)", finding_line.strip("- ").strip())
    if not m:
        return None
    _, name, rest = m.groups()
    name = name.strip()
    if " -> " in rest:
        new_full = rest.split(" -> ")[-1].split(" (")[0].strip()
        return name, f"https://github.com/{new_full}", None
    if "now PUBLIC" in rest:
        return name, None, "open source"
    if "archived status changed" in rest and "live=True" in rest:
        return name, None, "archived"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually branch/commit/push/open (default: dry-run)")
    args = ap.parse_args()

    sections = cd.parse_records(DATA_FILE.read_text(encoding="utf-8"))
    findings = cd.check_tracked_repos(sections) + cd.check_new_dsx_ai_factory_repos(sections)
    if not findings:
        print("OK: no drift, nothing to do.")
        return 0

    line_edits, new_repos = classify(findings)
    print(f"{len(line_edits)} mechanical finding(s) -> PR, {len(new_repos)} new-repo finding(s) -> issue")

    text = DATA_FILE.read_text(encoding="utf-8")
    applied = []
    for f in line_edits:
        parsed = finding_to_edit(f)
        if not parsed:
            print(f"  SKIP (could not parse): {f}")
            continue
        name, new_url, new_status = parsed
        text, changed = apply_line_edit(text, name, new_url, new_status)
        if changed:
            applied.append(f)
        else:
            print(f"  SKIP (record not found or no matching field): {f}")

    if not args.apply:
        print("\n--- DRY RUN: would write this data/repos.txt and open a PR with body: ---")
        print(f"## Index drift detected {date.today().isoformat()}\n")
        for f in applied:
            print(f"- {f}")
        if new_repos:
            print(f"\n{len(new_repos)} new untracked repo(s) would get a separate triage issue instead.")
        print(f"\n{BOT_MARKER}")
        return 0

    if not applied:
        print("Nothing applicable to auto-fix.")
    elif has_open_pr_from_bot():
        print("SKIP: an open PR from a prior run already exists - not filing a duplicate.")
    else:
        DATA_FILE.write_text(text, encoding="utf-8")
        branch = f"dsx-watch/index-update-{date.today().isoformat()}"
        run(["git", "checkout", "-b", branch])
        run(["python3", "site/render_index.py"])
        run(["git", "add", "-A"])
        body = "## Index drift detected\n\n" + "\n".join(f"- {f}" for f in applied) + f"\n\n{BOT_MARKER}"
        commit_msg = f"{PR_TITLE_PREFIX} ({date.today().isoformat()})\n\n{body}"
        run(["git", "commit", "-s", "-m", commit_msg])
        push = run(["git", "push", "-u", "origin", branch])
        if push.returncode != 0:
            print("push failed:", push.stderr)
            return 1
        pr = run([
            "gh", "pr", "create", "--draft",
            "--title", f"{PR_TITLE_PREFIX} ({date.today().isoformat()})",
            "--body", body,
            "--base", "chore/osrb-compliance-and-governance",
        ])
        print(pr.stdout, pr.stderr)

    if new_repos:
        existing_titles = open_issue_titles()
        for f in new_repos:
            m = re.search(r"NEW REPO not tracked: (\S+)", f)
            repo = m.group(1) if m else "unknown"
            title = f"{ISSUE_TITLE_PREFIX} {repo}"
            if title in existing_titles:
                print(f"SKIP: issue already open for {repo}")
                continue
            issue_body = f"A new repo was found in dsx-ai-factory that isn't in `data/repos.txt` yet:\n\n{f}\n\nNeeds a human to assign category/license/description before adding.\n\n{BOT_MARKER}"
            res = run(["gh", "issue", "create", "--title", title, "--body", issue_body])
            print(res.stdout, res.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
