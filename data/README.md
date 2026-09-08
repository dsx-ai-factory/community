# Materials index data

`repos.txt` is the single source of truth for the DSX repo and materials index (90-day
plan, s.4 "Post 2, the Pinned Index" and s.6 "Index generation"). `site/render_index.py`
renders it into two places:

- the pinned article, `content/posts/dsx-repo-and-materials-index.md`
- the `<!-- BEGIN REPO INDEX -->` / `<!-- END REPO INDEX -->` block in `README.md`

Edit `repos.txt`, then run the renderer — never hand-edit the generated block in either
output, it will be overwritten and the two will drift apart.

```
python3 site/render_index.py
```

## Format

Not YAML, for the same reason the rest of this repo avoids it: parsing YAML would mean
adding a dependency, and this repository's OSRB approval records zero. The format
mirrors article front matter — `key: value`, one per line — with records separated by a
line containing only `---`, grouped under `## section` headers.

Sections, matching the POR's index scope (90-day plan, s.4):

| Section | What it lists |
| --- | --- |
| `dsx-ai-factory` | Every repo in the `dsx-ai-factory` GitHub org |
| `nvidia-org` | DSX-relevant repos staying outside `dsx-ai-factory` |
| `upstream` | Upstream and third-party projects (Linux Foundation, etc.) |
| `video` | NVIDIA YouTube channel and the DSX playlist |
| `documentation` | DSX-DOCS and other reference documentation |

Record fields: `name`, `description`, `license`, `status`, `url`, plus `category` for
records in `dsx-ai-factory`, `nvidia-org`, and `upstream` (not required in `video` or
`documentation`, which don't have components to categorize). `license` is the SPDX
identifier reported by the GitHub API (e.g. `Apache-2.0`, `MIT`) — use `unknown` rather
than guessing if a repo has no detected license. A section with no confirmed entries
yet carries a `# TODO(...)` comment line instead of records — the renderer prints that
section as "to be added" rather than inventing a placeholder link. See `repos.txt` for
what is still open.

## Functional grouping (`category`)

The pinned index post groups `dsx-ai-factory`/`nvidia-org`/`upstream` components by
function, not by which GitHub org holds the repo — see "DSX Stack (1).pptx" (DSX Stack
Framework deck, reviewed Jul 29 2026), which breaks the Software - Infrastructure and
Software - Platform layers into named functional categories. `category` must be one of
the values in `CATEGORY_ORDER` in `site/render_index.py`:

Cluster Orchestration and Provisioning, Infrastructure Management, Monitoring and
Observability, Resiliency and Remediation, Security and Confidential Computing, Core
Operations, Scheduling and Workload Management, Optimized Inference, Validation and
Testing, Simulation, Developer Tooling, Documentation.

The last three (Validation and Testing, Developer Tooling, Documentation) are not in the
deck's own taxonomy — they exist here for repos that don't map onto a DSX Stack layer
(test harnesses, CI/IaC tooling, docs repos). Assigning a repo's category is a judgment
call recorded on the record itself; if a repo plausibly fits two categories, pick the
one that describes what the repo does for DSX OS, not how it is implemented.
