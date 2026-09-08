# Articles

One Markdown file per article. The path becomes the published URL, so choose it once
and do not move it afterwards — moving an article breaks every inbound link to it.

```
content/posts/<slug>.md                        -> /<slug>.html
content/posts/components/<slug>.md             -> /components/<slug>.html
content/posts/partners/<slug>.md               -> /partners/<slug>.html
```

The `components/` and `partners/` subdirectories are not cosmetic: `.github/CODEOWNERS`
routes them to the product delegate and the partner delegate respectively, so putting an
article in the right place is what pulls in the right reviewer.

## Front matter

Every article starts with a `---` delimited header. It is `key: value`, one per line —
not YAML, because parsing YAML would mean adding a dependency this repository does not
have.

```markdown
---
title: Scaling inference across a multi-tenant DSX cluster
date: 2026-11-09
authors: Jane Doe
type: how-to
tier: 1
component: nv-rms
pillar: infrastructure
last_reviewed: 2026-11-09
draft: false
---

Article body starts here.
```

| Field | Required | Notes |
| --- | --- | --- |
| `title` | yes | Shown as the page heading and in the index |
| `date` | yes | `YYYY-MM-DD`. Publication date |
| `authors` | yes | Byline as it should appear. Multiple authors: `Jane Doe, John Smith` |
| `type` | yes | One of the eight values below. `type` is what lets a single layout serve all seven POR content types, per the 90-day plan, s.6 |
| `last_reviewed` | yes | `YYYY-MM-DD`. Bump this whenever you verify the article still holds |
| `component` | no | The `dsx-ai-factory` repo this article is about, if any. Matches the CODEOWNERS product-delegate routing |
| `tier` | no | `1`, `2`, or `3`. Content tier from the 90-day plan, s.3 |
| `pillar` | no | Free text. Used for the "browse by pillar" navigation |
| `draft` | no | `true` or `false` (default `false`). `true` excludes the article from the build — a review queue, not a staging area. Front matter still has to be valid |
| `status` | no | `outdated` or `archived` — see below |
| `superseded_by` | no | URL of current material, shown in the outdated banner |

An unrecognized front matter field fails the build — this is deliberate, so a typo'd
field name does not silently do nothing.

Valid `type` values: `release-post`, `deep-dive`, `how-to`, `success-story`, `event`,
`exploratory`, `spotlight`, and `index` (the pinned repo-and-materials index; see
`data/README.md`).

## Starting from a template

Four skeletons cover the seven content types (90-day plan, s.6 Post Templates). Copy the
one for your type into `content/posts/` and fill it in:

| Skeleton | Serves | Spine |
| --- | --- | --- |
| [`content/templates/component-post.md`](../templates/component-post.md) | Component release post, Component/Technology deep-dive | What shipped, the problem it solves, how it works, what is next |
| [`content/templates/narrative.md`](../templates/narrative.md) | Exploratory post, Event announcement/recap | Prose led, light headings, links out. No fixed section list |
| [`content/templates/how-to.md`](../templates/how-to.md) | How-to | Prerequisites and versions, numbered steps, commands, verification, troubleshooting |
| [`content/templates/profile.md`](../templates/profile.md) | Success story, Contributor spotlight | Who they are, what they built, outcomes, quotes, what they would tell someone starting |

## Marking content outdated

Articles are **marked, never deleted** — published URLs stay resolvable. Set
`status: outdated` and the page renders a banner at the top. Add `superseded_by` with a
link when current material exists. Use `status: archived` when the component itself has
been retired.

An article whose `last_reviewed` date is more than a year old gets a staleness banner
automatically, without anyone having to remember. See
[GOVERNANCE.md](../../GOVERNANCE.md).

## Building locally

```
python3 site/build.py --check     # validate front matter, no token needed
GH_TOKEN=$(gh auth token) python3 site/build.py
```

Output lands in `docs/`, which is `.gitignore`d — do not commit it. On every merge to
`main`, `.github/workflows/pages.yml` builds it fresh and deploys it to GitHub Pages.
Build locally only to preview.
