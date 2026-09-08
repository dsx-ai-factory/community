#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: CC-BY-4.0
"""Lightweight house-style check for published articles. Dependency-free.

Not a substitute for editorial review — this catches mechanical tells cheaply
so a reviewer's attention goes to content, not punctuation. Findings are
warnings unless noted BLOCKING; a clean run does not mean an article is ready.

Usage:
    python3 site/stylecheck.py
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "posts"

# (pattern, message, blocking)
CHECKS = [
    (re.compile(r"—"), "em dash — use a comma, period, or parenthetical instead", False),
    (re.compile(r"\bit's worth noting\b", re.I), '"it\'s worth noting" — cut it, say the thing', False),
    (re.compile(r"\bin conclusion\b", re.I), '"in conclusion" — articles do not need a summary paragraph', False),
    (re.compile(r"\bdive (?:deep |right )?in\b", re.I), '"dive in" — cliché opener', False),
    (re.compile(r"\bunleash\b", re.I), '"unleash" — marketing tell', False),
    (re.compile(r"\bsupercharge\b", re.I), '"supercharge" — marketing tell', False),
    (re.compile(r"\bgame[- ]changing\b", re.I), '"game-changing" — unearned superlative', False),
    (re.compile(r"[ \t]+$", re.M), "trailing whitespace", False),
    (re.compile(r"\n{3,}"), "more than one blank line in a row", False),
    (re.compile(r"  +"), "double space", False),
]

FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)


def strip_front_matter(text):
    return FRONT_MATTER_RE.sub("", text, count=1)


def strip_code_blocks(text):
    """Do not flag style issues inside fenced or inline code.

    Replaces with a same-width placeholder word rather than deleting or
    inserting a space, so stripping a code span does not manufacture a double
    space out of the spacing already around it (e.g. "the `x` thing" must not
    become "the  thing" or "the   thing").
    """
    text = re.sub(r"```.*?```", "codeblock", text, flags=re.S)
    return re.sub(r"`[^`]*`", "code", text)


def main():
    if not CONTENT.is_dir():
        print("No articles yet: nothing to check.")
        return 0

    findings = 0
    for path in sorted(CONTENT.rglob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        raw = path.read_text(encoding="utf-8")
        body = strip_code_blocks(strip_front_matter(raw))
        for pattern, message, blocking in CHECKS:
            if pattern.search(body):
                marker = "error" if blocking else "warning"
                print(f"{marker}: {path.relative_to(ROOT)}: {message}")
                findings += 1

    if findings:
        print(f"\n{findings} style finding(s). None are build-blocking; review before merge.")
    else:
        print("OK: no style findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
