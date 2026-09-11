#!/usr/bin/env python3
"""SLOW fallback: fuzzy GitHub search for portal programs that guess_repos_by_slug.py
could not resolve. Rate-limited to 30 req/min by GitHub's search endpoint, so this
runs as a resumable queue: each invocation processes a capped batch and exits,
respecting X-RateLimit-Reset on 403s. Scheduled every 15min across a 2am-6am EST
window by cron -- NOT run inline in the main daily pipeline."""
import json
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path.home() / "work" / "dsx-portal.db"
GH_TOKEN_FILE = Path.home() / ".config" / "dsx-watch" / "gh_token"
QUEUE_STATE = Path.home() / "work" / "dsx-discover-queue.json"

MAX_CALLS_PER_RUN = 15
CALL_INTERVAL_S = 2.1  # GitHub search: 30 req/min authenticated

PRIORITY_ORGS = ["dsx-ai-factory", "NVIDIA", "Mellanox", "ai-dynamo", "run-ai", "leptonai",
                  "kai-scheduler", "kubernetes-sigs", "NVIDIA-Omniverse", "NVIDIA-Omniverse-blueprints",
                  "SlinkyProject"]

STOPWORDS = {"dsx", "os", "the", "nvidia", "project", "of", "for", "a", "an", "and", "oss",
             "labs", "platform", "framework", "service", "tool", "layer", "api"}


def gh_token():
    return GH_TOKEN_FILE.read_text(encoding="utf-8").strip()


def name_tokens(name):
    base = re.sub(r"\([^)]*\)", " ", name)
    tokens = re.findall(r"[a-zA-Z0-9]+", base.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def gh_search(query, org, token):
    q = f"{query} org:{org}" if org else query
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": q, "per_page": 5})
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return [{"fullName": i["full_name"], "url": i["html_url"], "description": i.get("description") or ""}
                for i in data.get("items", [])]
    except urllib.error.HTTPError as e:
        if e.code == 403:
            reset = e.headers.get("X-RateLimit-Reset")
            if reset:
                wait = max(0, int(reset) - int(time.time())) + 1
                print(f"  rate-limited, sleeping {wait}s until reset", file=sys.stderr)
                time.sleep(min(wait, 120))  # never sleep more than 2min in one call; queue picks up next run
            return []
        print(f"  search failed for {q!r}: HTTP {e.code}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  search failed for {q!r}: {e}", file=sys.stderr)
        return []


def score_candidate(tokens, repo_full_name):
    repo_name = repo_full_name.split("/")[-1].lower()
    repo_tokens = set(re.findall(r"[a-z0-9]+", repo_name))
    overlap = len(set(tokens) & repo_tokens)
    if overlap == 0:
        return "low"
    if overlap >= len(tokens):
        return "high"
    return "medium"


def load_queue(conn):
    """Programs still missing a github_url AND not already resolved by the
    slug-guess pass (no repo_candidates row yet)."""
    if QUEUE_STATE.exists():
        state = json.loads(QUEUE_STATE.read_text())
    else:
        state = {"pending": None}

    if not state.get("pending"):
        rows = conn.execute("""
            SELECT p.program_id, p.name FROM programs p
            WHERE (p.github_url = '' OR p.github_url IS NULL)
              AND p.program_id NOT IN (SELECT DISTINCT program_id FROM repo_candidates)
        """).fetchall()
        state["pending"] = [{"program_id": r[0], "name": r[1], "org_idx": 0} for r in rows]
        print(f"Rebuilt queue: {len(state['pending'])} programs need the slow search fallback.")
    return state


def save_queue(state):
    QUEUE_STATE.write_text(json.dumps(state, indent=2))


def main():
    token = gh_token()
    conn = sqlite3.connect(DB_PATH)
    state = load_queue(conn)
    queue = state["pending"]

    if not queue:
        print("Queue empty -- nothing left for the slow search fallback.")
        return 0

    calls_made = 0
    now = datetime.now(timezone.utc).isoformat()

    while queue and calls_made < MAX_CALLS_PER_RUN:
        item = queue[0]
        tokens = name_tokens(item["name"])
        query = " ".join(tokens[:4])
        org_idx = item["org_idx"]

        if org_idx >= len(PRIORITY_ORGS):
            # exhausted all orgs for this program with nothing found -- drop it
            print(f"  no candidates for {item['name']!r} after checking all orgs")
            queue.pop(0)
            continue

        org = PRIORITY_ORGS[org_idx]
        results = gh_search(query, org, token)
        calls_made += 1
        time.sleep(CALL_INTERVAL_S)

        found_high = False
        for r in results:
            conf = score_candidate(tokens, r["fullName"])
            conn.execute(
                "INSERT INTO repo_candidates (program_id, candidate_url, confidence, source, discovered_at) VALUES (?,?,?,?,?)",
                (item["program_id"], r["url"], conf, f"github search, org:{org}", now),
            )
            if conf == "high":
                found_high = True
        if results:
            print(f"  {item['name']!r} org:{org} -> {len(results)} candidate(s)")

        if found_high or org_idx == len(PRIORITY_ORGS) - 1:
            queue.pop(0)
        else:
            item["org_idx"] += 1

    conn.commit()
    conn.close()
    state["pending"] = queue
    save_queue(state)
    print(f"Batch done: {calls_made} calls made, {len(queue)} programs remain in queue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
