# NVIDIA Brings DSX AI Factory Open Source Projects Together in One GitHub Organization

[NVIDIA DSX](https://www.nvidia.com/en-us/data-center/products/dsx/) unifies AI factory design and operations across compute, networking, power, cooling, facilities, and software. Running an AI factory is largely an orchestration and operations problem, and [DSX OS](https://docs.nvidia.com/dsx#dsx-os) is the operating layer of the platform built for it. DSX OS is open source, vertically integrated, and horizontally composable: the components work together for teams running the full stack, and each can also be adopted on its own and integrated into an existing platform. It provides modular software for lifecycle management, runtime consistency, health automation, resiliency, and multi-tenant AI factory operations.

NVIDIA is now consolidating the open source projects behind DSX OS into a single GitHub organization, [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory). Selected projects that have lived under github.com/NVIDIA and other NVIDIA-owned organizations are moving there in phases, and new DSX open source projects will launch there directly. The first projects have already moved, including [NVIDIA Infra Controller (NICo)](https://github.com/dsx-ai-factory/infra-controller) and [Topograph](https://github.com/dsx-ai-factory/topograph). Four projects launched in the organization directly: [NVIDIA Run:ai](https://github.com/dsx-ai-factory/run-ai), [Health Validation](https://github.com/dsx-ai-factory/health-validation), [Attribution](https://github.com/dsx-ai-factory/attribution), and [Recovery](https://github.com/dsx-ai-factory/NVIDIA-Recovery).

## Why building in the open is critical

**Built by an ecosystem.** No single company builds an AI factory alone. Cloud providers, software vendors, hardware makers, and the teams racking systems on the ground all build against the same infrastructure layer at the same time. When that layer is open, they can work in parallel, report the bug they hit instead of working around it, and adapt the code to their own environments instead of waiting on a single roadmap. Open interfaces also let technologies from different providers work together, so the orchestration layer is something the ecosystem can adopt, extend, and improve.

**Trust and shared problems.** Software that power-cycles hardware, updates firmware, and decides which nodes receive work across thousands of machines needs to be readable before it is run, and open source lets operators inspect the code instead of relying on a vendor's description of it. The problems are also shared. Every operator faces the same questions of topology, health, and recovery, so a fix contributed once serves every AI factory that picks up newer versions.

**Shaping what comes next.** New demands from agentic applications, distributed inference, and power constraints are creating coordination problems that are still being worked out. Opening the software invites the community to help define what comes next, with a shared goal of getting more useful output from every GPU, watt, and dollar invested in an AI factory.

## Why a dedicated organization

**One home.** The DSX OS components grew up in different places. Some began as internal tools, some arrived with teams that joined NVIDIA, and some were open source from their first commit. As a result, a customer, partner, or contributor looking at DSX OS has had to know which of several organizations to search. A single organization gives the portfolio one name and one place to engage.

**Why not github.com/NVIDIA.** The NVIDIA organization holds more than 800 public repositories across many unrelated product areas, so DSX OS projects are hard to find there and do not read as one portfolio. A dedicated organization makes them easy to discover and lets them have their own contributor teams and access rules.

**A long-term commitment.** The move also reflects how NVIDIA intends to develop this software. A dedicated organization signals that DSX open source is a long-term investment for NVIDIA. It continues NVIDIA's long-standing commitment to developing in the open, welcoming contributions, and co-designing with partners, so that the people operating AI factories can shape the software they run. NVIDIA also continues to contribute to the upstream projects the ecosystem builds on, including Kubernetes.

## Building together in practice

NVIDIA hosted an invite-only DSX contributor workshop on September 30, 2026, where partner companies worked alongside NVIDIA engineers on projects across the stack. External contributions saw a significant uptick on that day, and partners opened issues and pull requests that extend the software to their own platforms. Read more about the day in this [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7514479530074509312/). The next workshop, the [DSX OS Inference Workshop](https://events.nvidia.com/dsx-os-inference-workshop), is planned for KubeCon + CloudNativeCon North America 2026 in November. Every public software project in the organization accepts issues and pull requests.

## What stays the same

A GitHub organization is a source code home, not a product identity. The move does not change project maintainers, licenses, or the history of issues, pull requests, and releases, all of which transfer with each repository. Every software project is released under an OSI-approved license, and nearly all of them under Apache 2.0. GitHub redirects existing repository URLs, so current clones and links keep working. Kubernetes API groups, labels, and annotations in the nvidia.com domain are unchanged, as are documentation on docs.nvidia.com and artifacts published on [NGC](https://catalog.ngc.nvidia.com/), PyPI, and crates.io. We plan to move artifacts that are currently published on GitHub Pages and GHCR to NGC.

## What to expect

The timeline for the remaining projects is coordinated centrally. Each project announces its own move in its README and release notes before anything changes, so users and contributors can plan ahead. Until a project announces its move, nothing changes for its users. Projects that are governed in a community or foundation home, or that already have an organization of their own, stay where they are.

The organization page lists each project as it arrives, and watching it is the simplest way to follow progress. Detailed migration guidance, including what to update in CI references, chart repositories, and image locations, will be published in the project documentation rather than in this post. Each project's repository links back to this post and to the shared guidance in [dsx-ai-factory/community](https://github.com/dsx-ai-factory/community), so the picture for any one project stays with that project.

Beyond the move itself, we plan to start community meetings for the DSX projects this year, so that users and contributors can follow progress and ask questions directly. Join us for the first in-person meetings for some of the projects at [KubeCon + CloudNativeCon North America 2026](https://www.nvidia.com/en-us/events/kubecon-and-cloudnative-con-north-america/) in November.

## Get started

- Explore the projects at [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory) and watch the ones you rely on.
- Read the DSX OS overview and documentation at [docs.nvidia.com/dsx](https://docs.nvidia.com/dsx).
- Join the conversation in the [DSX AI Factory Slack](https://inviter.co/dsx-ai-factory).
- Meet the DSX OS teams at [KubeCon + CloudNativeCon North America 2026](https://www.nvidia.com/en-us/events/kubecon-and-cloudnative-con-north-america/) in November.

> © 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
