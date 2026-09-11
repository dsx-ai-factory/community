#!/usr/bin/env python3
"""Daily job: pick up the latest DSX OS Programs portal CSV from the Drive drop
folder, rebuild the SQLite database (build_portal_db.py), search GitHub for
programs with no known repo (discover_missing_github.py), and refresh the
live Google Sheet editorial dashboard (build_editorial_sheet.py). Never
touches the public community repo -- output stays in Drive."""
import json
import subprocess
import sys
from pathlib import Path

DRIVE_FOLDER = "nvidia-gdrive:DSX OS Programs Exports"
STATE_FILE = Path.home() / "work" / "dsx-watch-portal-state.json"
LOCAL_CSV_DIR = Path.home() / "work" / "portal-csv-drops"
SCRIPT_DIR = Path(__file__).parent


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def latest_drive_csv():
    r = run(["rclone", "lsjson", DRIVE_FOLDER])
    if r.returncode != 0:
        print("rclone lsjson failed:", r.stderr, file=sys.stderr)
        sys.exit(1)
    files = [f for f in json.loads(r.stdout) if f["Name"].lower().endswith(".csv")]
    if not files:
        return None
    files.sort(key=lambda f: f["ModTime"])
    return files[-1]


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_name": None, "last_modtime": None}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def main():
    latest = latest_drive_csv()
    if latest is None:
        print("No CSV found in drop folder.")
        return 0

    state = load_state()
    if latest["Name"] == state.get("last_name") and latest["ModTime"] == state.get("last_modtime"):
        print(f"OK: no new CSV since last run ({latest['Name']}).")
        return 0

    LOCAL_CSV_DIR.mkdir(parents=True, exist_ok=True)
    local_path = LOCAL_CSV_DIR / latest["Name"]
    r = run(["rclone", "copyto", f"{DRIVE_FOLDER}/{latest['Name']}", str(local_path)])
    if r.returncode != 0:
        print("rclone copyto failed:", r.stderr, file=sys.stderr)
        return 1

    print(f"New CSV: {latest['Name']} (modified {latest['ModTime']}) -- rebuilding database.")
    r = run(["python3", str(SCRIPT_DIR / "build_portal_db.py"), str(local_path)])
    print(r.stdout)
    if r.returncode != 0:
        print("build_portal_db.py failed:", r.stderr, file=sys.stderr)
        return 1

    print("Trying fast slug-guess existence checks for programs with no known repo...")
    r = run(["python3", str(SCRIPT_DIR / "guess_repos_by_slug.py")])
    print(r.stdout)
    if r.returncode != 0:
        print("guess_repos_by_slug.py failed:", r.stderr, file=sys.stderr)
    # Anything still unresolved falls to discover_missing_github.py, which runs
    # separately via cron (slow, rate-limited search, 2am-6am EST queue) -- not here.

    print("Refreshing the editorial dashboard Google Sheet...")
    r = run(["python3", str(SCRIPT_DIR / "build_editorial_sheet.py")])
    print(r.stdout)
    if r.returncode != 0:
        print("build_editorial_sheet.py failed:", r.stderr, file=sys.stderr)
        return 1

    state = {"last_name": latest["Name"], "last_modtime": latest["ModTime"]}
    save_state(state)
    print("Done -- editorial dashboard refreshed in Drive.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
