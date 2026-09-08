#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: CC-BY-4.0
"""Render the DSX repo and materials index from data/repos.txt.

Dependency-free, same rationale as site/build.py: no YAML library, no template
engine. Produces two outputs from one source so they cannot drift apart
(90-day plan, s.6 "Index generation"):

  - content/posts/dsx-repo-and-materials-index.md  (the pinned article)
  - the <!-- BEGIN REPO INDEX --> block in README.md (dsx-ai-factory table only)

Usage:
    python3 site/render_index.py             # write both outputs
    python3 site/render_index.py --check     # validate data/repos.txt only
"""

import argparse
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "repos.txt"
INDEX_POST = ROOT / "content" / "posts" / "dsx-repo-and-materials-index.md"
README = ROOT / "README.md"

SECTIONS = {
    "dsx-ai-factory": "dsx-ai-factory repos",
    "nvidia-org": "NVIDIA org repos",
    "upstream": "Upstream and third party",
    "video": "Video",
    "documentation": "Documentation",
}
REQUIRED_RECORD_FIELDS = ("name", "description", "license", "status", "url")
# Sections whose records get grouped by function in the pinned index post
# (90-day plan's DSX Stack functional grouping, added 2026-09-08) rather than
# left in the trailing "video" section. `video` stays ungrouped/TODO until it
# has real entries, at which point it likely wants a category of its own.
CATEGORIZED_SECTIONS = ("dsx-ai-factory", "nvidia-org", "upstream", "documentation")

# Rendering order for the functional grouping, following the DSX Stack's own
# rough layer flow (facilities/hardware infra -> software infra -> software
# platform -> simulation), with two pragmatic buckets tacked on at the end for
# repos that don't map onto a stack layer.
CATEGORY_ORDER = [
    "Cluster Orchestration & Provisioning",
    "Infrastructure Management",
    "Monitoring & Observability",
    "Resiliency & Remediation",
    "Security & Confidential Computing",
    "Core Operations",
    "Scheduling & Workload Management",
    "Optimized Inference",
    "Validation & Testing",
    "Simulation",
    "Developer Tooling",
    "Documentation",
]


class DataError(Exception):
    """A problem in data/repos.txt the author must fix."""


def parse(text):
    """Return {section_key: [record, ...] | None}. None means 'not yet populated'."""
    sections = {key: None for key in SECTIONS}
    current = None
    record_lines = []
    records = []

    def flush_record():
        if not record_lines:
            return
        rec = {}
        for line in record_lines:
            if ":" not in line:
                raise DataError(f"malformed record line (not 'key: value'): {line!r}")
            key, _, value = line.partition(":")
            rec[key.strip()] = value.strip()
        required = REQUIRED_RECORD_FIELDS + (("category",) if current in CATEGORIZED_SECTIONS else ())
        missing = [f for f in required if f not in rec or not rec[f]]
        if missing:
            raise DataError(f"record missing field(s) {missing}: {rec}")
        if "category" in rec and rec["category"] not in CATEGORY_ORDER:
            raise DataError(f"record has unknown category {rec['category']!r}: {rec}")
        records.append(rec)
        record_lines.clear()

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("## "):
            if current is not None:
                flush_record()
                sections[current] = records
            key = stripped[3:].strip()
            if key not in SECTIONS:
                raise DataError(f"unknown section '## {key}'")
            current = key
            records = []
            continue
        if current is None:
            continue  # header comment block before the first section
        if stripped == "---":
            flush_record()
            continue
        if not stripped or stripped.startswith("#"):
            continue
        record_lines.append(stripped)

    if current is not None:
        flush_record()
        sections[current] = records

    return sections


def render_section_md(title, records):
    if not records:
        return f"### {title}\n\nTo be added.\n"
    rows = "\n".join(
        f"- **[{r['name']}]({r['url']})**: {r['description']} ({r['license']}, {r['status']})"
        for r in records
    )
    return f"### {title}\n\n{rows}\n"


# Where a record came from, shown alongside each functionally-grouped entry so
# "which layer is this" and "who owns the repo" stay visible together.
HOME_LABEL = {
    "dsx-ai-factory": "dsx-ai-factory",
    "nvidia-org": "NVIDIA org",
    "upstream": "upstream",
}


def render_functional_groups(sections):
    """Group dsx-ai-factory/nvidia-org/upstream records by DSX Stack function.

    Added 2026-09-08 per "DSX Stack (1).pptx" (Jason Perlow / DSX Stack Framework
    deck, reviewed Jul 29 2026): the deck breaks Software - Infrastructure and
    Software - Platform into named functional categories (s.18-19) rather than
    by which GitHub org happens to hold the repo. CATEGORY_ORDER in this module
    is that taxonomy, condensed to fit the repos actually in data/repos.txt, plus
    Validation & Testing, Developer Tooling, and Documentation for repos the
    deck does not cover. The category assignment for each repo is a judgment
    call recorded as the record's own `category` field in data/repos.txt, not
    re-derived here — change it there, not in this function.
    """
    by_category = {c: [] for c in CATEGORY_ORDER}
    for section in CATEGORIZED_SECTIONS:
        for r in sections[section] or []:
            by_category[r["category"]].append((r, section))

    parts = []
    for category in CATEGORY_ORDER:
        entries = by_category[category]
        if not entries:
            continue
        def row(r, section):
            # dsx-ai-factory status is bare ("open source") with no org context,
            # so tag it explicitly. nvidia-org/upstream status already names the
            # org/governance model (e.g. "open source, NVIDIA org"); appending
            # HOME_LABEL there would just repeat it.
            tag = f", {HOME_LABEL[section]}" if section == "dsx-ai-factory" else ""
            return f"- **[{r['name']}]({r['url']})**: {r['description']} ({r['license']}, {r['status']}{tag})"

        rows = "\n".join(row(r, section) for r, section in entries)
        parts.append(f"### {category}\n\n{rows}\n")
    return "\n".join(parts)


# Which functional categories (CATEGORY_ORDER) roll up into which DSX brand,
# per "DSX Stack (1).pptx" slide 21 ("DSX Portfolio... layers and
# functionalities grouped by DSX brands"). Documentation isn't a brand with
# open-source components of its own (it's this repo plus a pointer to
# docs.nvidia.com/dsx) so it is deliberately left out of every bucket below.
BRAND_CATEGORIES = {
    "DSX OS": [
        "Cluster Orchestration & Provisioning",
        "Infrastructure Management",
        "Monitoring & Observability",
        "Resiliency & Remediation",
        "Security & Confidential Computing",
        "Scheduling & Workload Management",
        "Optimized Inference",
        "Validation & Testing",
        "Developer Tooling",
    ],
    "DSX Exchange": ["Core Operations"],
    "DSX Sim": ["Simulation"],
    # No category currently rolls up to these two — no dsx-ai-factory/nvidia-org/
    # upstream repo in data/repos.txt is a DSX Flex or DSX MaxLPS component yet.
    # Left in the diagram (both are named on slide 21) rather than dropped, so
    # the diagram doesn't quietly imply they don't exist.
    "DSX Flex": [],
    "DSX MaxLPS": [],
}
# Diagram order, top to bottom: Simulation on top (models everything below),
# then DSX OS (by far the most open-source components, so drawn tallest and
# highlighted), then Exchange (also highlighted, per operator direction, even
# though its count is currently small), then Flex/MaxLPS at the bottom nearest
# the physical/power layer they represent.
BRAND_ORDER = ["DSX Sim", "DSX OS", "DSX Exchange", "DSX Flex", "DSX MaxLPS"]
BRAND_HEIGHT = {"DSX OS": 90}  # all others default to 50, set below

# What each brand covers, independent of open-source status — every band
# explains itself even when its component count is zero (operator direction
# 2026-09-08: describe the layer, don't just say "no open-source components").
BRAND_DESCRIPTION = {
    "DSX Sim": "Models the stack, so a factory can be validated before it is built",
    "DSX OS": "Orchestration, monitoring, scheduling, and inference software",
    "DSX Exchange": "IT/OT communication: event bus and agent gateway",
    "DSX Flex": "Dynamic power orchestration with grid and energy providers",
    "DSX MaxLPS": "Power architecture, cooling efficiency, and grid integration",
}

DSX_STACK_SVG_PATH = ROOT / "content" / "posts" / "assets" / "dsx-stack.svg"


def count_by_brand(sections):
    counts = {brand: 0 for brand in BRAND_ORDER}
    for section in CATEGORIZED_SECTIONS:
        for r in sections[section] or []:
            for brand, categories in BRAND_CATEGORIES.items():
                if r["category"] in categories:
                    counts[brand] += 1
    return counts


def render_stack_svg(sections):
    """A standalone SVG file, referenced from the article as an <img> (see
    render_index_post). NOT embedded inline in the article's Markdown: GitHub's
    markdown renderer (both github.com and the api.github.com/markdown endpoint
    site/build.py itself calls) sanitizes raw <svg>/<style>/<title>/<desc> tags
    out of rendered Markdown but leaves their TEXT CONTENT behind — verified by
    rendering this exact content through the API on 2026-09-08 and finding the
    tags stripped, the CSS and title/desc text left as garbled visible text, and
    no image. An <img src="..."> tag from Markdown image syntax is on GitHub's
    sanitizer allowlist and is not affected.

    Grouped by DSX brand (slide 21), not by generic stack layer, per operator
    direction 2026-09-08. DSX OS and DSX Exchange are highlighted because they
    are where a large number of components have already been open sourced;
    counts are computed live from data/repos.txt so the diagram cannot drift
    from the listing below it.
    """
    counts = count_by_brand(sections)
    x, width, gap, pad = 20, 600, 4, 10
    y = pad
    rects = []
    for brand in BRAND_ORDER:
        h = BRAND_HEIGHT.get(brand, 50)
        n = counts[brand]
        highlighted = brand in ("DSX OS", "DSX Exchange")
        if highlighted:
            fill, stroke, text_fill = "#76b900", "#ffffff", "#ffffff"
        elif n > 0:
            fill, stroke, text_fill = "#a8d977", "#ffffff", "#1b1b1b"
        else:
            fill, stroke, text_fill = "#e2e2e2", "#9a9a9a", "#4a4a4a"
        # Every band explains what it does; the highlighted ones additionally
        # name their open-source count, since that's what's being highlighted.
        sub_text = BRAND_DESCRIPTION[brand]
        if highlighted:
            sub_text += f" &#8212; {n} open source"
        label_y, sub_y = y + h / 2 - 4, y + h / 2 + 16
        rects.append(
            f'  <rect class="band" x="{x}" y="{y}" width="{width}" height="{h}" rx="6" '
            f'fill="{fill}" stroke="{stroke}"/>\n'
            f'  <text class="label" x="{x + 16}" y="{label_y:.0f}" fill="{text_fill}">{brand}</text>\n'
            f'  <text class="sub" x="{x + 16}" y="{sub_y:.0f}" fill="{text_fill}">{sub_text}</text>'
        )
        y += h + gap
    total_height = y - gap + pad
    bands = "\n\n".join(rects)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 640 {total_height}" width="640" height="{total_height}" role="img"
     aria-labelledby="dsx-stack-title dsx-stack-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="dsx-stack-title">The DSX Portfolio, by Brand</title>
  <desc id="dsx-stack-desc">
    DSX Sim, DSX OS, DSX Exchange, DSX Flex, and DSX MaxLPS, each shown with what it
    covers. DSX OS and DSX Exchange are highlighted and labeled with an open-source
    component count: that is where the open-source components are concentrated.
  </desc>
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    .band {{ stroke-width: 2; }}
    .label {{ font-size: 15px; font-weight: 600; }}
    .sub {{ font-size: 12px; }}
  </style>
{bands}
</svg>
"""


def render_index_post(sections):
    today = datetime.date.today().isoformat()
    functional_body = render_functional_groups(sections).strip()
    brand_counts = count_by_brand(sections)
    video_records = sections["video"] or []
    video_body = (
        "\n".join(
            f"- **[{r['name']}]({r['url']})**: {r['description']} ({r['license']}, {r['status']})"
            for r in video_records
        )
        if video_records
        else "To be added."
    )
    return f"""---
title: DSX Repo and Materials Index
date: {today}
authors: DSX AI Factory Community
type: index
tier: 1
pillar: index
last_reviewed: {today}
draft: true
---

<!-- Generated by site/render_index.py from data/repos.txt. Do not edit by hand. -->

## What is DSX

DSX is NVIDIA's overarching brand for AI Factories: it spans hardware, data center
power and cooling infrastructure, and software, everything needed to plan, build, and
run a GPU-accelerated data center. It is organized into a handful of named brands,
each covering part of that scope:

![The DSX portfolio by brand: DSX Sim on top, DSX OS (highlighted, the largest concentration of open-source components) below it, then DSX Exchange (also highlighted), DSX Flex, and DSX MaxLPS.](assets/dsx-stack.svg)

- **DSX OS** is the open-source IaaS/PaaS software that provisions, orchestrates, monitors, and serves inference across a cluster: cluster orchestration, infrastructure management, monitoring, resiliency, security, scheduling, workload management, and optimized inference.
- **DSX Exchange** is IT/OT infrastructure communication: the event bus and agent gateway that connect DSX clusters to building management and grid systems.
- **DSX Flex** and **DSX MaxLPS** cover power: grid integration, cooling efficiency, and dynamic power orchestration.
- **DSX Sim** models the other four, so an AI factory can be validated before it is built.

Some of DSX is open source, alongside domains such as hardware and facilities that are
not released as source code by their nature. DSX OS and DSX Exchange are where the
open-source components are concentrated: as of this page's last render, DSX OS
accounts for {brand_counts['DSX OS']} open-source components and DSX Exchange
{brand_counts['DSX Exchange']}, which is why they are highlighted above. DSX Flex and
DSX MaxLPS do not have open-source components in this index yet. The full list, each
shown against the DSX layer it occupies, is below.

## DSX components released as open source, by layer

{functional_body}

## Video

{video_body}
"""


def render_readme_block(sections):
    rows = "\n".join(
        f"| [{r['name']}]({r['url']}) | {r['description']} | {r['license']} | {r['status']} |"
        for r in (sections["dsx-ai-factory"] or [])
    )
    if not rows:
        rows = "| _to be added_ | | | |"
    return (
        "<!-- BEGIN REPO INDEX (generated by site/render_index.py from data/repos.txt — do not edit by hand) -->\n"
        "| Repository | Description | License | Status |\n"
        "| --- | --- | --- | --- |\n"
        f"{rows}\n"
        "\n"
        "Full index, including NVIDIA org repos, upstream projects, video, and "
        "documentation: [DSX Repo and Materials Index]"
        "(content/posts/dsx-repo-and-materials-index.md).\n"
        "<!-- END REPO INDEX -->"
    )


def splice_readme(readme_text, block):
    start_marker = "<!-- BEGIN REPO INDEX"
    end_marker = "<!-- END REPO INDEX -->"
    start = readme_text.find(start_marker)
    end = readme_text.find(end_marker)
    if start == -1 or end == -1:
        raise DataError(
            "README.md has no <!-- BEGIN REPO INDEX --> / <!-- END REPO INDEX --> markers to splice into"
        )
    return readme_text[:start] + block + readme_text[end + len(end_marker):]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="validate data/repos.txt only, write nothing")
    args = ap.parse_args()

    if not DATA.exists():
        print(f"error: {DATA} does not exist", file=sys.stderr)
        return 1

    try:
        sections = parse(DATA.read_text(encoding="utf-8"))
    except DataError as exc:
        print(f"error: {DATA}: {exc}", file=sys.stderr)
        return 1

    populated = [key for key, records in sections.items() if records]
    empty = [key for key, records in sections.items() if not records]
    print(f"OK: parsed {DATA.relative_to(ROOT)} — populated: {populated or 'none'}; open: {empty or 'none'}")

    if args.check:
        return 0

    INDEX_POST.parent.mkdir(parents=True, exist_ok=True)
    INDEX_POST.write_text(render_index_post(sections), encoding="utf-8")
    print(f"wrote {INDEX_POST.relative_to(ROOT)}")

    DSX_STACK_SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DSX_STACK_SVG_PATH.write_text(render_stack_svg(sections), encoding="utf-8")
    print(f"wrote {DSX_STACK_SVG_PATH.relative_to(ROOT)}")

    if not README.exists():
        print(f"error: {README} does not exist", file=sys.stderr)
        return 1
    try:
        updated = splice_readme(README.read_text(encoding="utf-8"), render_readme_block(sections))
    except DataError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    README.write_text(updated, encoding="utf-8")
    print(f"updated {README.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
