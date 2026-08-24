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
author: Jane Doe
type: how-to
last_reviewed: 2026-11-09
---

Article body starts here.
```

| Field | Required | Notes |
| --- | --- | --- |
| `title` | yes | Shown as the page heading and in the index |
| `date` | yes | `YYYY-MM-DD`. Publication date |
| `author` | yes | Byline as it should appear |
| `type` | yes | One of the seven content types below |
| `last_reviewed` | yes | `YYYY-MM-DD`. Bump this whenever you verify the article still holds |
| `status` | no | `outdated` or `archived` — see below |
| `superseded_by` | no | URL of current material, shown in the outdated banner |

Valid `type` values: `release-post`, `deep-dive`, `how-to`, `success-story`, `event`,
`exploratory`, `spotlight`.

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

Output lands in `docs/`, which is what GitHub Pages serves. Commit the rendered output
along with the article.
