# DSX AI Factory Community

DSX AI Factory Community publishes articles and hosts discussions about the
open-source components of NVIDIA's DSX AI Factory platform. It exists so a developer,
partner, or customer working with DSX has one place to find release notes, technical
deep dives, how-tos, and community conversation about the components as they ship.

**This repository does not contain source code.** Community articles and posts may
include example code snippets for illustration, but each named project lives in its
own repository. Article content will be added in a follow-up pull request; this one
covers the repository's compliance and governance scaffolding.

## Open-Source Components

- **[libredfish](https://github.com/dsx-ai-factory/libredfish)** — a Rust crate for interacting with DMTF Redfish endpoints.
- **[nv-redfish](https://github.com/dsx-ai-factory/nv-redfish)** — NVIDIA's next-generation Redfish crate.
- **[Rack Management Service (RMS)](https://github.com/dsx-ai-factory/nv-rms)** — NVIDIA Rack Management Service.
- **[RMS Client](https://github.com/dsx-ai-factory/nv-rms-client)** — Rust client crate for NVIDIA Rack Management Service.
- **[Switch Infrastructure Config Manager](https://github.com/dsx-ai-factory/nv-config-manager)** — switch infrastructure config manager for large-scale datacenter operations.
- **[Fleet Intelligence](https://github.com/dsx-ai-factory/fleet-intelligence-agent)** — host agent for GPU telemetry collection and attestation.
- **[nv-telemetry](https://github.com/dsx-ai-factory/nv-telemetry)** — libraries for bare-metal telemetry collection.
- **[DSX Exchange](https://github.com/dsx-ai-factory/dsx-exchange)** — DSX Exchange event bus and schemas.
- **[DSX GitHub Actions](https://github.com/dsx-ai-factory/dsx-github-actions)** — shared GitHub Actions CI library for DSX.

A fuller index of components across the `dsx-ai-factory` and `NVIDIA` GitHub orgs will
be added in a follow-up pull request.

## Contributing

Contributions are welcome from NVIDIA employees, partners, customers, and the wider
open-source community.

- Propose an article by opening an **Article proposal** issue. An editor will confirm the topic and a publishing slot before you write.
- Fix a typo, a broken link, or a stale version number by opening a pull request directly.
- Read [CONTRIBUTING.md](CONTRIBUTING.md) first. All commits must be signed off (`git commit -s`) under the Developer Certificate of Origin.

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## Governance

[GOVERNANCE.md](GOVERNANCE.md) describes the roles, the content approval path,
the publishing schedule, and how outdated articles are marked.

## License

Content in this repository is licensed under
[Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE).

You may share and adapt it, including commercially, provided you give appropriate credit.
Contributors keep the copyright in their own work. See
[CONTRIBUTING.md](CONTRIBUTING.md#licensing-and-ownership-of-contributions).

Third-party components are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Security

Do not report security vulnerabilities in a public issue or discussion. Follow
[SECURITY.md](SECURITY.md).
