#!/usr/bin/env python3
"""Load the latest DSX OS Programs portal CSV into a SQLite database the agent
can query: every program, its PICs, dates, milestones, and best-known repo
location. Idempotent (upsert by program id). Internal only -- do not commit to
the public community repo (PM/TPM/EM/DevRel names+emails inside)."""
import csv
import json
import re
import sqlite3
import sys
from pathlib import Path

csv.field_size_limit(sys.maxsize)

CSV_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "work" / "portal-csv-drops"
DB_PATH = Path.home() / "work" / "dsx-portal.db"


def latest_csv(path):
    if path.is_file():
        return path
    candidates = sorted(path.glob("*.csv"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        print("No CSV found.", file=sys.stderr)
        sys.exit(1)
    return candidates[-1]


SCHEMA = """
CREATE TABLE IF NOT EXISTS programs (
    program_id TEXT PRIMARY KEY,
    slug TEXT,
    name TEXT,
    layer_code TEXT,
    layer TEXT,
    short_description TEXT,
    pm_pic TEXT,
    pm_pic_email TEXT,
    tpm_pic TEXT,
    em_pic TEXT,
    devrel_pic TEXT,
    devrel_pic_email TEXT,
    priority TEXT,
    oss_phase_code TEXT,
    oss_phase TEXT,
    marketing_tier TEXT,
    pulse_status_code TEXT,
    pulse_status TEXT,
    status_note TEXT,
    concept_submitted_at TEXT,
    concept_approved_at TEXT,
    last_confirmed TEXT,
    github_url TEXT,
    gitlab_url TEXT,
    other_links_json TEXT,
    milestones_json TEXT,
    tracked_repo_name TEXT,
    updated_at TEXT
);
CREATE TABLE IF NOT EXISTS milestones (
    program_id TEXT,
    due_month TEXT,
    text TEXT,
    FOREIGN KEY(program_id) REFERENCES programs(program_id)
);
CREATE TABLE IF NOT EXISTS repo_candidates (
    program_id TEXT,
    candidate_url TEXT,
    confidence TEXT,
    source TEXT,
    discovered_at TEXT,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY(program_id) REFERENCES programs(program_id)
);
"""


def extract_links(row):
    try:
        links = json.loads(row.get("Links JSON") or "[]")
    except json.JSONDecodeError:
        links = []
    github_url = ""
    gitlab_url = ""
    other = []
    for l in links:
        url = l.get("url", "")
        kind = l.get("kind", "")
        if kind == "github" and not github_url:
            github_url = url
        elif "gitlab" in url.lower() and not gitlab_url:
            gitlab_url = url
        else:
            other.append(l)
    return github_url, gitlab_url, other


def normalize_repo_url(url):
    """owner/repo, lowercased, ignoring scheme/www/trailing bits -- so renames
    within the same repo (org move aside) still don't false-match, but
    http(s)/www/trailing-slash noise does not cause false negatives."""
    if not url:
        return None
    u = url.strip().lower()
    u = re.sub(r"^https?://(www\.)?github\.com/", "", u)
    u = u.rstrip("/")
    u = re.sub(r"\.git$", "", u)
    parts = u.split("/")
    if len(parts) < 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def tracked_urls():
    """owner/repo -> display name, from data/repos.txt's url: fields."""
    repos_txt = Path.home() / "work" / "community" / "data" / "repos.txt"
    if not repos_txt.exists():
        return {}
    urls = {}
    current_name = None
    for line in repos_txt.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("name:"):
            current_name = stripped.split("name:", 1)[1].strip()
        elif stripped.startswith("url:"):
            norm = normalize_repo_url(stripped.split("url:", 1)[1].strip())
            if norm:
                urls[norm] = current_name
    return urls


def main():
    csv_path = latest_csv(CSV_PATH)
    print(f"Loading {csv_path}")
    with open(csv_path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    tracked = tracked_urls()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)

    for row in rows:
        pid = row.get("Program ID", "").strip()
        if not pid:
            continue
        github_url, gitlab_url, other_links = extract_links(row)
        name = row.get("Project / Program", "").strip()
        conn.execute("DELETE FROM milestones WHERE program_id = ?", (pid,))
        conn.execute("""
            INSERT INTO programs (program_id, slug, name, layer_code, layer, short_description,
                pm_pic, pm_pic_email, tpm_pic, em_pic, devrel_pic, devrel_pic_email, priority,
                oss_phase_code, oss_phase, marketing_tier, pulse_status_code, pulse_status,
                status_note, concept_submitted_at, concept_approved_at, last_confirmed,
                github_url, gitlab_url, other_links_json, milestones_json, tracked_repo_name, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(program_id) DO UPDATE SET
                slug=excluded.slug, name=excluded.name, layer_code=excluded.layer_code,
                layer=excluded.layer, short_description=excluded.short_description,
                pm_pic=excluded.pm_pic, pm_pic_email=excluded.pm_pic_email,
                tpm_pic=excluded.tpm_pic, em_pic=excluded.em_pic, devrel_pic=excluded.devrel_pic,
                devrel_pic_email=excluded.devrel_pic_email, priority=excluded.priority,
                oss_phase_code=excluded.oss_phase_code, oss_phase=excluded.oss_phase,
                marketing_tier=excluded.marketing_tier, pulse_status_code=excluded.pulse_status_code,
                pulse_status=excluded.pulse_status, status_note=excluded.status_note,
                concept_submitted_at=excluded.concept_submitted_at,
                concept_approved_at=excluded.concept_approved_at, last_confirmed=excluded.last_confirmed,
                github_url=excluded.github_url, gitlab_url=excluded.gitlab_url,
                other_links_json=excluded.other_links_json, milestones_json=excluded.milestones_json,
                tracked_repo_name=excluded.tracked_repo_name, updated_at=excluded.updated_at
        """, (
            pid, row.get("Slug", ""), name, row.get("Layer code", ""), row.get("Layer", ""),
            row.get("Short description", ""), row.get("PM PIC", ""), row.get("PM PIC email", ""),
            row.get("TPM PIC", ""), row.get("EM PIC", ""), row.get("Devrel PIC", ""),
            row.get("Devrel PIC email", ""), row.get("Priority", ""), row.get("OSS phase code", ""),
            row.get("OSS Phase", ""), row.get("Marketing tier", ""), row.get("Pulse status code", ""),
            row.get("Pulse status", ""), row.get("Status note", ""), row.get("Concept submitted at", ""),
            row.get("Concept approved at", ""), row.get("Last confirmed", ""), github_url, gitlab_url,
            json.dumps(other_links), row.get("Milestones JSON", "[]"),
            tracked.get(normalize_repo_url(github_url)) or tracked.get(normalize_repo_url(gitlab_url)),
            row.get("Updated at", ""),
        ))
        try:
            ms = json.loads(row.get("Milestones JSON") or "[]")
        except json.JSONDecodeError:
            ms = []
        for m in ms:
            conn.execute("INSERT INTO milestones (program_id, due_month, text) VALUES (?,?,?)",
                         (pid, m.get("dueMonth", ""), m.get("text", "")))

    conn.commit()

    total = conn.execute("SELECT COUNT(*) FROM programs").fetchone()[0]
    missing_github = conn.execute("SELECT COUNT(*) FROM programs WHERE github_url = '' OR github_url IS NULL").fetchone()[0]
    print(f"Loaded {total} programs, {missing_github} missing a known GitHub URL.")
    conn.close()


if __name__ == "__main__":
    main()
