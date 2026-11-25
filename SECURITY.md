# Security

## Reporting a vulnerability

If you discover a potential security vulnerability, do not submit it through
GitHub Issues, pull requests, Discussions, GitHub Security Advisories, GitHub
private vulnerability reporting, or other public channels. Report it directly
to NVIDIA PSIRT through one of these channels:

- **Web (preferred):**
  [NVIDIA Vulnerability Disclosure Program](https://www.nvidia.com/en-us/security/report-vulnerability/)
- **Email:** [psirt@nvidia.com](mailto:psirt@nvidia.com). Encrypt sensitive
  information using the
  [NVIDIA public PGP key](https://www.nvidia.com/en-us/security/pgp-key).

This repository publishes articles and hosts discussions. It contains no product
source code, so a vulnerability is far more likely to belong to one of the DSX AI
Factory components than to this repository. Report it to PSIRT either way; PSIRT
routes it to the right team.

Please include the following information:

- The product or repository, and the affected component, article, file, or URL.
- The type of vulnerability and how you found it.
- Step-by-step reproduction instructions and any proof-of-concept code.
- The expected impact.
- Relevant logs or configuration snippets, with secrets and personal or customer
  identifiers removed.

NVIDIA PSIRT manages vulnerability intake, validation, remediation coordination,
and disclosure. Response timing, coordinated disclosure, and reporter
acknowledgement are governed by the
[NVIDIA PSIRT policies](https://www.nvidia.com/en-us/security/psirt-policies/).

## Problems with this repository itself

If you find a problem with the repository or the published site — a workflow
misconfiguration, exposed credentials in an article or example, or content that
should not be public — report it to NVIDIA PSIRT through the channels above
rather than in an issue.

## Credentials in content

Articles frequently contain example commands, configuration, and output. If you
spot a real credential, token, internal hostname, or internal URL in published
content, treat it as a security report and follow the process above. Do not open a
pull request that removes it, since the value remains in the repository history and
needs to be rotated regardless.
