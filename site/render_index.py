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


# A standalone SVG file, referenced from the article as an <img> (see
# render_index_post). NOT embedded inline in the article's Markdown: GitHub's
# markdown renderer (both github.com and the api.github.com/markdown endpoint
# site/build.py itself calls) sanitizes raw <svg>/<style>/<title>/<desc> tags
# out of rendered Markdown but leaves their TEXT CONTENT behind — verified by
# rendering this exact content through the API on 2026-09-08 and finding the
# tags stripped, the CSS and title/desc text left as garbled visible text, and
# no image. An <img src="..."> tag from Markdown image syntax is on GitHub's
# sanitizer allowlist and is not affected.
DSX_STACK_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 640 300" width="640" height="300" role="img"
     aria-labelledby="dsx-stack-title dsx-stack-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="dsx-stack-title">The DSX Stack</title>
  <desc id="dsx-stack-desc">
    Five layers, foundation to top: Facilities Infrastructure, Hardware, Software -
    Infrastructure, Software - Platform, and Simulation, which models the other four.
  </desc>
  <style>
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .band { stroke: #ffffff; stroke-width: 2; }
    .label { font-size: 15px; font-weight: 600; fill: #ffffff; }
    .sub { font-size: 12px; fill: #f0f0f0; }
  </style>
  <rect class="band" x="20" y="10"  width="600" height="50" rx="6" fill="#a8d977"/>
  <text class="label" x="36" y="32">Simulation</text>
  <text class="sub"   x="36" y="49">DSX Air, Omniverse Blueprints, SimReady assets</text>

  <rect class="band" x="20" y="64"  width="600" height="50" rx="6" fill="#76b900"/>
  <text class="label" x="36" y="86">Software &#8212; Platform</text>
  <text class="sub"   x="36" y="103">Scheduling, workload management, optimized inference</text>

  <rect class="band" x="20" y="118" width="600" height="50" rx="6" fill="#2e6b1f"/>
  <text class="label" x="36" y="140">Software &#8212; Infrastructure</text>
  <text class="sub"   x="36" y="157">Orchestration, provisioning, monitoring, resiliency, security</text>

  <rect class="band" x="20" y="172" width="600" height="50" rx="6" fill="#6a6a6a"/>
  <text class="label" x="36" y="194">Hardware</text>
  <text class="sub"   x="36" y="211">Compute, network, storage</text>

  <rect class="band" x="20" y="226" width="600" height="50" rx="6" fill="#4a4a4a"/>
  <text class="label" x="36" y="248">Facilities Infrastructure</text>
  <text class="sub"   x="36" y="265">Land, connectivity, power, shell</text>
</svg>
"""

DSX_STACK_SVG_PATH = ROOT / "content" / "posts" / "assets" / "dsx-stack.svg"


def render_index_post(sections):
    today = datetime.date.today().isoformat()
    functional_body = render_functional_groups(sections).strip()
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

## What is DSX OS

DSX OS is the open-source IaaS and PaaS layer of the DSX AI Factory platform: the
components that provision, orchestrate, monitor, and serve inference across a
GPU-accelerated cluster. It sits inside the wider DSX Stack, which runs from the
physical facility up through simulation:

![The DSX Stack: five layers, Facilities Infrastructure and Hardware at the foundation, Software - Infrastructure and Software - Platform above them, Simulation on top modeling the other four.](assets/dsx-stack.svg)

- **Facilities Infrastructure** covers the physical site: land, connectivity, power, and shell.
- **Hardware** is compute, network, and storage.
- **Software - Infrastructure** is the layer most of the repos below live in: cluster orchestration and provisioning, infrastructure management, monitoring and observability, resiliency and remediation, security, and core operations.
- **Software - Platform** is scheduling, workload management, and optimized inference, the layer that turns a provisioned cluster into one that serves workloads.
- **Simulation** models the other four layers, so an AI factory can be validated before it is built.

Every open-source `dsx-ai-factory` component, and the NVIDIA-org and upstream
projects DSX OS depends on, are grouped below by which of these functions they
serve, not by which GitHub org happens to hold the repo.

## DSX OS components, by function

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
    DSX_STACK_SVG_PATH.write_text(DSX_STACK_SVG, encoding="utf-8")
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
