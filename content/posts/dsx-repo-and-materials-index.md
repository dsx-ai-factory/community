---
title: DSX Repo and Materials Index
date: 2026-09-08
authors: DSX AI Factory Community
type: index
tier: 1
pillar: index
last_reviewed: 2026-09-08
draft: true
---

The single entry point for the `dsx-ai-factory` organization and the material around
it. This page points outward rather than restating anything, so it stays in scope and
does not go stale as components ship (90-day plan, s.4). It is generated from
[`data/repos.txt`](https://github.com/dsx-ai-factory/community/blob/main/data/repos.txt).
Edit that file, not this one.

### dsx-ai-factory repos

- **[libredfish](https://github.com/dsx-ai-factory/libredfish)**: A Rust crate for interacting with DMTF Redfish endpoints. (MIT, open source)
- **[nv-redfish](https://github.com/dsx-ai-factory/nv-redfish)**: NVIDIA's next-generation Redfish crate. (Apache-2.0, open source)
- **[fleet-intelligence-agent](https://github.com/dsx-ai-factory/fleet-intelligence-agent)**: Host agent for GPU telemetry collection and attestation. (Apache-2.0, open source)
- **[infra-controller](https://github.com/dsx-ai-factory/infra-controller)**: Hardware lifecycle management and multitenant networking (NiCo / Carbide). (Apache-2.0, open source)
- **[nv-rms](https://github.com/dsx-ai-factory/nv-rms)**: NVIDIA Rack Management Service. (Apache-2.0, open source)
- **[nv-rms-client](https://github.com/dsx-ai-factory/nv-rms-client)**: Rust language client crate for NVIDIA Rack Management Service. (Apache-2.0, open source)
- **[nv-config-manager](https://github.com/dsx-ai-factory/nv-config-manager)**: Switch infrastructure config manager (KIWI). (Apache-2.0, open source)
- **[nv-telemetry](https://github.com/dsx-ai-factory/nv-telemetry)**: Libraries for bare-metal telemetry collection. (Apache-2.0, open source)
- **[dsx-exchange](https://github.com/dsx-ai-factory/dsx-exchange)**: DSX Exchange (event bus and schemas). (Apache-2.0, open source)
- **[dsx-github-actions](https://github.com/dsx-ai-factory/dsx-github-actions)**: Shared GitHub Actions CI library for DSX. (Apache-2.0, open source)
- **[attribution](https://github.com/dsx-ai-factory/attribution)**: NVIDIA Attribution (FACT). Private GitHub collaboration with customers. (unknown, internal, not yet public)
- **[health-validation](https://github.com/dsx-ai-factory/health-validation)**: Hardware health check catalog and evaluation engine for NVIDIA GPU nodes. (unknown, internal, not yet public)
- **[fleet-intelligence-oob-collector](https://github.com/dsx-ai-factory/fleet-intelligence-oob-collector)**: Fleet Intelligence out-of-band collector for BMC inventory, attestation, and telemetry. (Apache-2.0, internal, not yet public)
- **[run-ai](https://github.com/dsx-ai-factory/run-ai)**: Run:ai AI workload orchestration platform for Kubernetes (DSX-internal working copy; see the upstream section for the public run-ai org). (Apache-2.0, internal, not yet public)
- **[testwave](https://github.com/dsx-ai-factory/testwave)**: Cloud-native platform for automated testing across Kubernetes clusters. (Apache-2.0, internal, not yet public)
- **[community](https://github.com/dsx-ai-factory/community)**: This repository. Community articles and discussions about the open-source components of the NVIDIA DSX AI Factory. (CC-BY-4.0, internal, not yet public)

### NVIDIA org repos

- **[AICR (AI Cluster Runtime)](https://github.com/NVIDIA/aicr)**: Tooling for optimized, validated, and reproducible GPU-accelerated AI runtime in Kubernetes. (Apache-2.0, open source, NVIDIA org)
- **[NVSentinel](https://github.com/NVIDIA/NVSentinel)**: Detects and remediates GPU faults on Kubernetes nodes. (Apache-2.0, open source, NVIDIA org)
- **[NVCF (Cloud Functions)](https://github.com/NVIDIA/nvcf)**: Platform for deploying and routing GPU-accelerated inference, streaming, and batch workloads at scale. (Apache-2.0, open source, NVIDIA org)
- **[Exemplar Performance](https://github.com/NVIDIA/exemplar-performance)**: Ready-to-use recipes for evaluating AI use case performance across hardware and software combinations. Renamed from dgxc-benchmarking. (unknown, open source, NVIDIA org)
- **[DPF (DOCA Platform Framework)](https://github.com/NVIDIA/doca-platform)**: Manages provisioning and service orchestration for BlueField DPUs. (Apache-2.0, open source, NVIDIA org)
- **[NiCo REST (Infra Controller REST)](https://github.com/NVIDIA/infra-controller-rest)**: NVIDIA Infra Controller REST API. Public but archived; disposition (move, stay archived, or superseded) is an open question in the Org POR. (Apache-2.0, archived, NVIDIA org)
- **[AI Cloud-Ready Validation](https://github.com/NVIDIA/ai-cloud-validation)**: Validation and management tools for NVIDIA AI Cloud environments. Renamed from ISV-NCP-Validation-Suite. (Apache-2.0, open source, NVIDIA org)
- **[Kata Containers (NVIDIA fork)](https://github.com/NVIDIA/kata-containers)**: NVIDIA's fork of the lightweight-VM container runtime Kata Containers. (Apache-2.0, open source, NVIDIA org)
- **[DSX-DOCS](https://github.com/NVIDIA/dsx-docs)**: DSX common and cross-component documentation. Deliberately kept private/internal, the repo the DSX AI Factory org proposal keeps non-public. (unknown, internal, NVIDIA org)
- **[Omniverse DSX Blueprint](https://github.com/NVIDIA-Omniverse-blueprints/omniverse-dsx-blueprint-for-ai-factories)**: Omniverse Libraries and OpenUSD workflows for coordinated AI factory planning and digital twins. (unknown, open source, NVIDIA-Omniverse-blueprints org)
- **[AIF Digital Twin Pipeline Samples](https://github.com/NVIDIA-Omniverse/aif-pipeline-samples)**: Sample scripts and presets for SimReady USD assets in Omniverse, focused on CAD ingestion for AI Factory digital twins. (MIT, open source, NVIDIA-Omniverse org)

### Upstream and third party

- **[KAI Scheduler](https://github.com/kai-scheduler/KAI-Scheduler)**: Kubernetes-native scheduler for AI workloads at scale. CNCF Sandbox project, a Series of LF Projects, LLC; NVIDIA does not hold the merge gate. (Apache-2.0, foundation-governed (CNCF / Linux Foundation))
- **[DRA Driver for NVIDIA GPUs](https://github.com/kubernetes-sigs/dra-driver-nvidia-gpu)**: Dynamic Resource Allocation driver for NVIDIA GPUs on Kubernetes, donated to kubernetes-sigs. (Apache-2.0, foundation-governed (Kubernetes SIGs / CNCF))
- **[Dynamo](https://github.com/ai-dynamo/dynamo)**: Datacenter-scale distributed inference serving framework. (unknown, open source, NVIDIA-controlled (ai-dynamo org, not NVIDIA-branded))
- **[Grove](https://github.com/ai-dynamo/grove)**: Kubernetes enhancements for network-topology-aware gang scheduling and autoscaling. (Apache-2.0, open source, NVIDIA-controlled (ai-dynamo org, not NVIDIA-branded))
- **[Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer)**: Fast model-weight loading library for GPU inference serving. (Apache-2.0, open source, NVIDIA-controlled (run-ai org, not NVIDIA-branded))

### Video

To be added.

### Documentation

To be added.

