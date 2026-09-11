#!/usr/bin/env python3
"""Build/refresh a live Google Sheet editorial calendar + alerting dashboard
from dsx-portal.db. Two tabs: 'Editorial Calendar' (every upcoming milestone
with a computed recommended-post-start date) and 'Alerts' (filtered to what
needs attention now, sorted soonest-first). Creates the Sheet once, then
updates the SAME file in place on every subsequent run (stable URL). Internal
use only -- never linked from the public community repo."""
import json
import re
import sqlite3
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

DB_PATH = Path.home() / "work" / "dsx-portal.db"
XLSX_PATH = Path.home() / "work" / "portal-csv-drops" / "dsx-editorial-dashboard.xlsx"
STATE_FILE = Path.home() / "work" / "dsx-editorial-sheet-state.json"
DRIVE_FOLDER_ID_CACHE = Path.home() / "work" / "dsx-drive-folder-id.json"
RCLONE_CONF = Path.home() / ".config" / "rclone" / "rclone.conf"
DRIVE_FOLDER_NAME = "DSX OS Programs Exports"

# Lead time (weeks of run-up before the milestone) by marketing tier.
LEAD_WEEKS = {
    "T1 (Keynote/PR)": 6,
    "T2 (Momentum Announcement)": 4,
    "T3 (Ongoing Beats)": 2,
}
DEFAULT_LEAD_WEEKS = 3

HEADER_FILL = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
ALERT_COLORS = {
    "OVERDUE": "DC2626",       # red
    "START NOW": "EA580C",     # orange
    "START THIS WEEK": "F59E0B",  # amber
    "START SOON": "FDE68A",    # pale yellow
    "ON TRACK": "86EFAC",      # green
}


def due_date_from_month(due_month):
    try:
        y, m = due_month.split("-")
        return date(int(y), int(m), 1)
    except (ValueError, AttributeError):
        return None


def compute_row(name, layer, oss_phase, tier, pulse, pm, pm_email, tracked_repo, due_month, milestone_text):
    due = due_date_from_month(due_month)
    today = date.today()
    lead_weeks = LEAD_WEEKS.get(tier, DEFAULT_LEAD_WEEKS)
    if due is None:
        return None
    recommended_start = due - timedelta(weeks=lead_weeks)
    days_until_due = (due - today).days
    days_until_start = (recommended_start - today).days

    if due < today:
        alert = "OVERDUE"
    elif days_until_start <= 0:
        alert = "START NOW"
    elif days_until_start <= 7:
        alert = "START THIS WEEK"
    elif days_until_start <= 14:
        alert = "START SOON"
    else:
        alert = "ON TRACK"

    return {
        "name": name, "layer": layer, "oss_phase": oss_phase, "tier": tier or "(none)",
        "pulse": pulse, "pm": pm, "pm_email": pm_email, "tracked_repo": tracked_repo or "NOT TRACKED",
        "due_month": due_month, "milestone_text": milestone_text,
        "due_date": due.isoformat(), "lead_weeks": lead_weeks,
        "recommended_start": recommended_start.isoformat(),
        "days_until_due": days_until_due, "days_until_start": days_until_start,
        "alert": alert,
    }


def load_rows():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    today = date.today().isoformat()[:7]
    q = conn.execute("""
        SELECT p.name, p.layer, p.oss_phase, p.marketing_tier, p.pulse_status,
               p.pm_pic, p.pm_pic_email, p.tracked_repo_name,
               m.due_month, m.text
        FROM milestones m JOIN programs p ON p.program_id = m.program_id
        WHERE m.due_month >= ?
        ORDER BY m.due_month ASC
    """, (today,)).fetchall()
    conn.close()
    rows = []
    for r in q:
        computed = compute_row(r["name"], r["layer"], r["oss_phase"], r["marketing_tier"],
                                r["pulse_status"], r["pm_pic"], r["pm_pic_email"],
                                r["tracked_repo_name"], r["due_month"], r["text"])
        if computed:
            rows.append(computed)
    return rows


COLUMNS = [
    ("alert", "Alert"), ("name", "Program"), ("layer", "Layer"), ("milestone_text", "Milestone"),
    ("due_month", "Due (month)"), ("due_date", "Due (est.)"), ("days_until_due", "Days Until Due"),
    ("recommended_start", "Recommended Post Start"), ("days_until_start", "Days Until Start"),
    ("lead_weeks", "Lead Time (wk)"), ("tier", "Marketing Tier"), ("oss_phase", "OSS Phase"),
    ("pulse", "Pulse"), ("tracked_repo", "Tracked Repo"), ("pm", "PM PIC"), ("pm_email", "PM Email"),
]


def write_sheet(ws, rows, title):
    ws.title = title
    for col_idx, (_, header) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center")
    for row_idx, row in enumerate(rows, start=2):
        for col_idx, (key, _) in enumerate(COLUMNS, start=1):
            ws.cell(row=row_idx, column=col_idx, value=row[key])
        alert_cell = ws.cell(row=row_idx, column=1)
        color = ALERT_COLORS.get(row["alert"])
        if color:
            alert_cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    for col_idx, (key, header) in enumerate(COLUMNS, start=1):
        width = max(len(header), max((len(str(r[key])) for r in rows), default=10) if rows else 10)
        ws.column_dimensions[get_column_letter(col_idx)].width = min(width + 2, 50)
    ws.freeze_panes = "A2"
    if rows:
        ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{len(rows) + 1}"


UNTRACKED_COLUMNS = [("name", "Program"), ("layer", "Layer"), ("known_url", "Known Repo URL (portal)"),
                     ("pm", "PM PIC"), ("pm_email", "PM Email")]
CANDIDATE_COLUMNS = [("name", "Program"), ("candidate_url", "Candidate Repo URL"),
                     ("confidence", "Confidence"), ("source", "Source")]


def load_untracked_graduated():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    q = conn.execute("""
        SELECT name, layer, pm_pic, pm_pic_email, github_url, gitlab_url
        FROM programs
        WHERE oss_phase = 'Graduated' AND tracked_repo_name IS NULL
    """).fetchall()
    conn.close()
    return [{"name": r["name"], "layer": r["layer"], "pm": r["pm_pic"], "pm_email": r["pm_pic_email"],
             "known_url": r["github_url"] or r["gitlab_url"] or "(no repo link in portal)"} for r in q]


def load_candidates():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    q = conn.execute("""
        SELECT p.name, c.candidate_url, c.confidence, c.source
        FROM repo_candidates c JOIN programs p ON p.program_id = c.program_id
        ORDER BY p.name, CASE c.confidence WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END
    """).fetchall()
    conn.close()
    return [dict(r) for r in q]


def write_simple_sheet(ws, rows, columns, title):
    ws.title = title
    for col_idx, (_, header) in enumerate(columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
    for row_idx, row in enumerate(rows, start=2):
        for col_idx, (key, _) in enumerate(columns, start=1):
            ws.cell(row=row_idx, column=col_idx, value=row[key])
    for col_idx, (key, header) in enumerate(columns, start=1):
        width = max(len(header), max((len(str(r[key])) for r in rows), default=10) if rows else 10)
        ws.column_dimensions[get_column_letter(col_idx)].width = min(width + 2, 60)
    ws.freeze_panes = "A2"
    if rows:
        ws.auto_filter.ref = f"A1:{get_column_letter(len(columns))}{len(rows) + 1}"


def build_xlsx(rows):
    alert_order = {"OVERDUE": 0, "START NOW": 1, "START THIS WEEK": 2, "START SOON": 3, "ON TRACK": 4}
    alerts_rows = sorted([r for r in rows if r["alert"] != "ON TRACK"],
                         key=lambda r: (alert_order[r["alert"]], r["days_until_start"]))
    untracked = load_untracked_graduated()
    candidates = load_candidates()

    wb = openpyxl.Workbook()
    write_sheet(wb.active, alerts_rows, "Alerts")
    write_sheet(wb.create_sheet(), rows, "Editorial Calendar")
    write_simple_sheet(wb.create_sheet(), untracked, UNTRACKED_COLUMNS, "Untracked (Graduated)")
    write_simple_sheet(wb.create_sheet(), candidates, CANDIDATE_COLUMNS, "Repo Candidates")
    XLSX_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb.save(XLSX_PATH)
    return len(rows), len(alerts_rows)


def rclone_access_token():
    subprocess.run(["rclone", "lsf", "nvidia-gdrive:"], capture_output=True, text=True, timeout=30)
    conf = RCLONE_CONF.read_text()
    m = re.search(r'token = ({.*?})\n', conf)
    if not m:
        raise RuntimeError("could not find rclone token in config")
    return json.loads(m.group(1))["access_token"]


def drive_folder_id(token):
    if DRIVE_FOLDER_ID_CACHE.exists():
        return json.loads(DRIVE_FOLDER_ID_CACHE.read_text())["id"]
    q = f"name='{DRIVE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    url = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode({"q": q})
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    files = data.get("files", [])
    if not files:
        raise RuntimeError(f"Drive folder {DRIVE_FOLDER_NAME!r} not found")
    fid = files[0]["id"]
    DRIVE_FOLDER_ID_CACHE.write_text(json.dumps({"id": fid}))
    return fid


def create_sheet(token, folder_id):
    boundary = "dsxdash" + str(int(datetime.now().timestamp()))
    metadata = {
        "name": "DSX Editorial Dashboard",
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "parents": [folder_id],
    }
    media = XLSX_PATH.read_bytes()
    body = (
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\nContent-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\r\n\r\n"
    ).encode() + media + f"\r\n--{boundary}--".encode()

    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,webViewLink",
        data=body, method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def update_sheet(token, file_id):
    media = XLSX_PATH.read_bytes()
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media",
        data=media, method="PATCH",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def main():
    rows = load_rows()
    total, alert_count = build_xlsx(rows)
    print(f"Built dashboard: {total} milestones, {alert_count} need attention.")

    token = rclone_access_token()
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}

    if "file_id" in state:
        result = update_sheet(token, state["file_id"])
        print(f"Updated existing sheet: https://docs.google.com/spreadsheets/d/{state['file_id']}/edit")
    else:
        folder_id = drive_folder_id(token)
        result = create_sheet(token, folder_id)
        state["file_id"] = result["id"]
        STATE_FILE.write_text(json.dumps(state, indent=2))
        print(f"Created new sheet: {result.get('webViewLink', result['id'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
