#!/usr/bin/env python3
"""Content-signal triage: watch public tracked repos for activity that might
be post-worthy (a release, a version tag without a formal release, a burst of
commits, or a new non-NVIDIA contributor -- a strong external-interest
signal) and draft a short triage note as a GitHub issue for an editor to
accept or decline.

Never publishes an article itself - this only ever produces a triage issue.
State (what's already been seen) persists in a local JSON file on this
instance, NOT in the community repo - it's operational bookkeeping, not
content. Losing the instance loses the state, not any real data (worst case:
a repeat scan re-reports something already seen once).

Usage:
    python3 check_activity.py            # dry-run: print what would be filed
    python3 check_activity.py --apply    # actually file triage issues
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_drift as cd  # noqa: E402

REPO_ROOT = cd.REPO_ROOT
DATA_FILE = cd.DATA_FILE
STATE_FILE = Path.home() / "work" / "dsx-watch-activity-state.json"
BOT_MARKER = "<!-- filed automatically by DSX Repo Watch -->"
ISSUE_TITLE_PREFIX = "Content signal:"
MAX_ISSUES_PER_RUN = 5

NVIDIA_API_KEY_FILE = Path.home() / ".config" / "dsx-watch" / "nvidia_api_key"
MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

# Known bot/automation logins to never treat as a "new external contributor" --
# these commit from outside nvidia.com but aren't a community-interest signal.
BOT_LOGIN_PATTERNS = re.compile(r"(bot|dependabot|renovate|github-actions|automation)$", re.I)


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, **kw)


def gh_api(path):
    result = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def public_tracked_repos(sections):
    """Only repos actually released as open source - internal/roadmapped
    ones have no public activity to watch yet."""
    repos = []
    for section in ("dsx-ai-factory", "nvidia-org", "upstream"):
        for rec in sections.get(section) or []:
            status = rec.get("status", "").lower()
            if "internal" in status or "to be released" in status:
                continue
            owner, repo = cd.owner_repo_from_url(rec.get("url", ""))
            if owner:
                repos.append((rec["name"], owner, repo))
    return repos


def is_nvidia_email(email):
    return bool(email) and email.lower().endswith("@nvidia.com")


def is_bot_author(login, email):
    if login and BOT_LOGIN_PATTERNS.search(login):
        return True
    if email and "noreply.github.com" in email and login and "[bot]" in login:
        return True
    return False


def collect_events(name, owner, repo, state):
    """Return a list of (event_type, summary_dict) for this repo since the
    last time it was checked."""
    key = f"{owner}/{repo}"
    prev = state.get(key, {})
    events = []

    releases = gh_api(f"repos/{owner}/{repo}/releases?per_page=1")
    if releases:
        latest = releases[0]
        if latest["tag_name"] != prev.get("last_release"):
            events.append(("release", {
                "tag": latest["tag_name"],
                "name": latest.get("name") or latest["tag_name"],
                "body": (latest.get("body") or "")[:1500],
                "url": latest["html_url"],
            }))
        state.setdefault(key, {})["last_release"] = latest["tag_name"]

    # Fallback: some repos cut version tags without ever creating a formal
    # GitHub Release object. Catch those too, as a distinct "code milestone".
    tags = gh_api(f"repos/{owner}/{repo}/tags?per_page=1")
    if tags:
        latest_tag = tags[0]["name"]
        release_tags = {r["tag_name"] for r in (releases or [])}
        if latest_tag != prev.get("last_tag") and latest_tag not in release_tags:
            events.append(("tag", {
                "tag": latest_tag,
                "commit_sha": tags[0].get("commit", {}).get("sha", ""),
                "url": f"https://github.com/{owner}/{repo}/releases/tag/{latest_tag}",
            }))
        state.setdefault(key, {})["last_tag"] = latest_tag

    commits = gh_api(f"repos/{owner}/{repo}/commits?per_page=30")
    if commits:
        last_seen_sha = prev.get("last_commit_sha")
        new_commits = []
        for c in commits:
            if c["sha"] == last_seen_sha:
                break
            new_commits.append(c["commit"]["message"].splitlines()[0])
        if last_seen_sha and 5 <= len(new_commits) < 30:
            events.append(("commit_burst", {
                "count": len(new_commits),
                "messages": new_commits[:10],
            }))

        # Non-NVIDIA committers on new commits since the last check -- a new
        # (not-previously-seen) external author is a strong external-interest
        # signal, distinct from just "some commits happened".
        known_external = set(prev.get("known_external_authors", []))
        newly_seen = {}
        for c in commits:
            if c["sha"] == last_seen_sha:
                break
            commit_author = c.get("commit", {}).get("author", {}) or {}
            email = commit_author.get("email", "")
            gh_user = c.get("author") or {}
            login = gh_user.get("login", "")
            if is_nvidia_email(email) or is_bot_author(login, email):
                continue
            author_key = login or email
            if not author_key or author_key in known_external:
                continue
            newly_seen[author_key] = {
                "login": login, "email": email,
                "commit_message": commit_author and c["commit"]["message"].splitlines()[0],
                "commit_url": c.get("html_url", ""),
            }
        if newly_seen and last_seen_sha:  # skip on first-ever baseline pass
            events.append(("external_contributor", {"authors": list(newly_seen.values())}))
        state.setdefault(key, {})["known_external_authors"] = list(known_external | set(newly_seen.keys()))

        state.setdefault(key, {})["last_commit_sha"] = commits[0]["sha"]

    return events, state


def judge_post_worthy(name, owner, repo, event_type, summary):
    """Ask the model: is this worth a triage note, and if so, draft it."""
    if event_type == "release":
        prompt = (
            f"Repo: {owner}/{repo} ({name}), part of NVIDIA's DSX AI Factory.\n"
            f"New release: {summary['tag']} - {summary['name']}\n"
            f"Release notes:\n{summary['body']}\n\n"
            "Is this release notable enough to suggest as a DSX community blog post "
            "(release post, deep-dive, or spotlight)? Reply with exactly one line: "
            "either 'NO' or 'YES: <one sentence on why, and which post type fits>'."
        )
    elif event_type == "tag":
        prompt = (
            f"Repo: {owner}/{repo} ({name}), part of NVIDIA's DSX AI Factory.\n"
            f"New version tag cut: {summary['tag']} (no formal GitHub Release notes were written for it).\n\n"
            "Is a new version tag on its own worth flagging to an editor as a possible "
            "code-milestone/blog topic (e.g. a major/minor version bump)? Reply with exactly "
            "one line: either 'NO' or 'YES: <one sentence on why>'."
        )
    elif event_type == "external_contributor":
        authors = "\n".join(f"- {a['login'] or a['email']}: {a['commit_message']}" for a in summary["authors"])
        prompt = (
            f"Repo: {owner}/{repo} ({name}), part of NVIDIA's DSX AI Factory.\n"
            f"New non-NVIDIA contributor(s) just committed for the first time:\n{authors}\n\n"
            "External contributions to an NVIDIA open source project are a real community-interest "
            "signal. Is this worth flagging to an editor as a possible 'community spotlight' or "
            "'growing adoption' post angle? Reply with exactly one line: either 'NO' or "
            "'YES: <one sentence on why>'."
        )
    else:
        msgs = "\n".join(f"- {m}" for m in summary["messages"])
        prompt = (
            f"Repo: {owner}/{repo} ({name}), part of NVIDIA's DSX AI Factory.\n"
            f"{summary['count']} commits since the last check. Recent commit messages:\n{msgs}\n\n"
            "Does this look like a notable development burst worth flagging to an editor "
            "as a possible blog post topic? Reply with exactly one line: either 'NO' or "
            "'YES: <one sentence on why>'."
        )

    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "chat_template_kwargs": {"enable_thinking": False},
    })
    api_key = NVIDIA_API_KEY_FILE.read_text().strip()
    result = subprocess.run(
        ["curl", "-s", "https://integrate.api.nvidia.com/v1/chat/completions",
         "-H", f"Authorization: Bearer {api_key}",
         "-H", "Content-Type: application/json",
         "-d", payload],
        capture_output=True, text=True, timeout=30,
    )
    try:
        content = json.loads(result.stdout)["choices"][0]["message"]["content"].strip()
    except (json.JSONDecodeError, KeyError, IndexError):
        return None
    if content.upper().startswith("YES"):
        return content
    return None


def open_issue_titles():
    res = run(["gh", "issue", "list", "--state", "open", "--json", "title", "--limit", "100"])
    if res.returncode != 0:
        return set()
    try:
        return {i["title"] for i in json.loads(res.stdout)}
    except json.JSONDecodeError:
        return set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    sections = cd.parse_records(DATA_FILE.read_text(encoding="utf-8"))
    repos = public_tracked_repos(sections)
    state = load_state()
    first_run = not STATE_FILE.exists()

    to_file = []
    for name, owner, repo in repos:
        events, state = collect_events(name, owner, repo, state)
        if first_run:
            continue  # first run just baselines state, nothing to judge yet
        for event_type, summary in events:
            verdict = judge_post_worthy(name, owner, repo, event_type, summary)
            if verdict:
                to_file.append((name, owner, repo, event_type, summary, verdict))
            if len(to_file) >= MAX_ISSUES_PER_RUN:
                break
        if len(to_file) >= MAX_ISSUES_PER_RUN:
            break

    save_state(state)

    if first_run:
        print(f"First run: baselined state for {len(repos)} repos. Nothing to triage yet.")
        return 0

    if not to_file:
        print(f"Checked {len(repos)} repos, no post-worthy signals.")
        return 0

    print(f"{len(to_file)} post-worthy signal(s) found.")
    if not args.apply:
        for name, owner, repo, event_type, summary, verdict in to_file:
            print(f"\n[{event_type}] {owner}/{repo}: {verdict}")
        return 0

    existing = open_issue_titles()
    for name, owner, repo, event_type, summary, verdict in to_file:
        title = f"{ISSUE_TITLE_PREFIX} {owner}/{repo} ({event_type})"
        if title in existing:
            print(f"SKIP: issue already open for {owner}/{repo} {event_type}")
            continue
        body = (
            f"**{name}** ({owner}/{repo}) - {event_type}\n\n"
            f"{verdict}\n\n"
            f"Evidence: {json.dumps(summary, indent=2)}\n\n"
            f"{BOT_MARKER}"
        )
        res = run(["gh", "issue", "create", "--title", title, "--body", body])
        print(res.stdout, res.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
