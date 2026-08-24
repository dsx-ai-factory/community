# Governance

How content gets proposed, reviewed, published, and retired in this repository, and
who decides. This implements the governance model called for in the DSX Community
Repo POR.

## Roles

| Role | GitHub team | Responsibility |
| --- | --- | --- |
| Editor | `dsx-community-editors` | Overall PIC. Owns the content roadmap, accepts or declines proposals, assigns publishing slots, works with contributors and delegates. |
| Maintainer | `dsx-community-maintainers` | Owns the publishing pipeline and repository configuration. Reviews, approves, merges, publishes. |
| Product delegate | `dsx-community-product` | One person per component team. Reviews articles that describe their component. |
| Partner delegate | `dsx-community-partners` | One person per partner program area. Reviews partner and customer mentions, and interfaces with partner marketing and account teams. |
| Community representative | `dsx-community-moderators` | Moderates Discussions, enforces the Code of Conduct. |

Role holders are named in the POR staffing table. Team membership is the operative
record — CODEOWNERS resolves against teams, not individuals.

## Teams to request from an organization owner

None of these teams exist yet. `.github/CODEOWNERS` names them, and **GitHub silently
ignores CODEOWNERS entries that reference a non-existent team**, so review enforcement
does nothing until they are created. Request the following from a `dsx-ai-factory`
organization owner:

| Team slug | Repository permission | Notes |
| --- | --- | --- |
| `dsx-community-editors` | Write | Default owner of all content paths. |
| `dsx-community-maintainers` | Maintain | Owns `.github/`, the site build, and the compliance files. |
| `dsx-community-product` | Write | Component reviewers. |
| `dsx-community-partners` | Write | Partner and customer mention reviewers. |
| `dsx-community-moderators` | Triage | Discussion moderation; does not need merge rights. |

Keep these separate from the existing `dsx-sw-*` engineering teams. Content review and
code review are different jobs with different membership, and merging them means every
engineer is a content approver by accident.

## Content approval

1. **Proposal.** A contributor opens an Article Proposal issue. Editors triage it,
   confirm the topic is not already covered, assign a content type, and set a target
   publishing window. An unaccepted proposal is not a commitment to publish.
2. **Draft.** The contributor forks and opens a pull request against `main`. External
   contributors always work from a fork.
3. **Review.** The pull request requires:
   - approval from an editor for the content itself;
   - approval from the relevant **product delegate** if it describes a component;
   - approval from the relevant **partner delegate** if it names a partner or customer.
   CODEOWNERS routes these automatically based on the paths touched.
4. **Merge and publish.** A maintainer merges. Publishing follows from the merge —
   the site builds from `main`. No separate publish step, and no publishing from a
   branch.

Small corrections — typos, broken links, stale version numbers — skip step 1 and need
only a single approval.

## Publishing schedule

Articles are published against the content roadmap in the POR rather than on merge-when-ready.
The editor owns the calendar and holds merged-but-unpublished work in the target window
where a launch date depends on it.

## Marking outdated content

Articles are dated and go stale. Every article carries a last-reviewed date in its front
matter.

- An article untouched for **12 months** is flagged for review by the editor.
- An article whose commands, versions, or prerequisites no longer work is marked
  **outdated** at the top of the page, with a pointer to current material where one
  exists.
- Outdated articles are **not deleted**. Published URLs stay resolvable — removing them
  breaks inbound links and reads as revising history. Mark, do not delete.
- An article describing a component that has been retired is marked **archived**.

## Discussions

Discussions are for questions, ideas, and conversation about DSX open-source components
and about the articles published here. They are moderated by the community
representative under the Code of Conduct.

Out of scope, and redirected rather than answered in place:

- Bug reports against a component — belong in that component's repository.
- Support requests and account or entitlement questions — belong in NVIDIA support channels.
- Security vulnerabilities — belong with NVIDIA PSIRT. See [SECURITY.md](SECURITY.md).

The POR names discussion drift as a risk. The redirect list above is the boundary; keep
it current as the org grows.

## Ownership of contributed content

Contributors keep the copyright in what they write. Sign-off under the Developer
Certificate of Origin certifies the right to submit — it does not transfer ownership to
NVIDIA. Everything merged is available to everyone under CC-BY-4.0 with attribution.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changes that require re-opening OSRB approval

This repository's public release is covered by an Open Source Review Board approval that
records it as CC-BY-4.0, source-only, with **no third-party dependencies**. Re-open that
approval before doing any of the following:

- changing the repository license;
- adding a third-party dependency, theme, static site generator, or package manifest;
- vendoring or copying third-party code;
- changing the distribution location, channel, or project name;
- changing how an approved dependency is used.

Adding articles, features, or documentation within the existing scope does **not**
require a new approval, provided the team's IP review process is followed.
