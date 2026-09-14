# Security

## Reporting a vulnerability

**Do not open a public issue or discussion to report a security vulnerability.**

This repository publishes articles and hosts discussions. It contains no product
source code, so a vulnerability is far more likely to belong to one of the DSX AI
Factory components than to this repository.

Report vulnerabilities in NVIDIA products through the NVIDIA Product Security
Incident Response Team (PSIRT):

- <https://www.nvidia.com/en-us/security/psirt-policies/>

## Problems with this repository itself

If you find a problem with the repository or the published site — a workflow
misconfiguration, exposed credentials in an article or example, or content that
should not be public — report it privately rather than in an issue:

- GitHub's private vulnerability reporting is **not currently enabled** on this
  repository (checked 2026-09-08) — the "Report a vulnerability" button will not
  work until an admin turns it on under Settings → Security.
- TODO-BEFORE-PUBLIC: enable private vulnerability reporting, or add a real
  monitored security contact (email or form) here in the meantime —
  "contact the maintainers directly" is not itself a reachable channel.

## Credentials in content

Articles frequently contain example commands, configuration, and output. If you
spot a real credential, token, internal hostname, or internal URL in published
content, treat it as a security report and follow the process above. Do not open a
pull request that removes it, since the value remains in the repository history and
needs to be rotated regardless.
