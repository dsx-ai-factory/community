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

Record fields: `name`, `description`, `status`, `url`. A section with no confirmed
entries yet carries a `# TODO(...)` comment line instead of records — the renderer
prints that section as "to be added" rather than inventing a placeholder link. See
`repos.txt` for what is still open.
