---
title: What Has Been Released in DSX So Far
date: 2026-09-08
authors: DSX AI Factory Community
type: exploratory
tier: 2
pillar: portfolio
last_reviewed: 2026-09-08
draft: true
---

Before this repository existed, DSX had already open-sourced a lot. This is the
backlog post: a look at what has shipped so far, so the component release posts that
follow have something to follow.

## The count, as of today

38 DSX components are public today, spanning [KAI Scheduler](https://github.com/kai-scheduler/KAI-Scheduler)
and the [DRA Driver for NVIDIA GPUs](https://github.com/kubernetes-sigs/dra-driver-nvidia-gpu)
at the Linux Foundation, to [Dynamo](https://github.com/ai-dynamo/dynamo) and
[GPU Operator](https://github.com/NVIDIA/gpu-operator) under NVIDIA's own orgs, to the
first components that have already moved into `dsx-ai-factory` itself:
[infra-controller](https://github.com/dsx-ai-factory/infra-controller),
[fleet-intelligence-agent](https://github.com/dsx-ai-factory/fleet-intelligence-agent),
[dsx-exchange](https://github.com/dsx-ai-factory/dsx-exchange), and others. Most of
what's public today is still homed outside `dsx-ai-factory`, in the main `NVIDIA` org
or in NVIDIA-controlled orgs that don't carry the NVIDIA name. That migration is
ongoing, not finished, and the [DSX Repo and Materials Index](dsx-repo-and-materials-index.md)
tracks it as it happens.

## Where the components sit

Sorted by DSX brand rather than by which GitHub org happens to hold the repo, most of
what's public clusters into DSX OS: cluster orchestration and provisioning (GPU
Operator, the DRA Driver, [Project Topograph](https://github.com/NVIDIA/topograph),
[Nodewright](https://github.com/NVIDIA/nodewright)), infrastructure management
(the Rack Management Service and its client, [Switch Infrastructure Config
Manager](https://github.com/dsx-ai-factory/nv-config-manager), the Nautobot
NVDataModels family), monitoring and observability ([NVSentinel](https://github.com/NVIDIA/NVSentinel),
Fleet Intelligence), scheduling and inference (KAI Scheduler, Grove, Dynamo, [Run:ai
Model Streamer](https://github.com/run-ai/runai-model-streamer)), and security
([NVTrust Attestation](https://github.com/NVIDIA/nvtrust), the Kata Containers forks).

DSX Exchange has one component public so far: the event bus and schemas in
`dsx-exchange`. DSX Sim has two, both Omniverse-based (the [DSX Blueprint for AI
Factories](https://github.com/NVIDIA-Omniverse-blueprints/omniverse-dsx-blueprint-for-ai-factories)
and the [AIF Digital Twin Pipeline Samples](https://github.com/NVIDIA-Omniverse/aif-pipeline-samples)).
DSX Flex and DSX MaxLPS, the power and cooling side of DSX, don't have open-source
components yet. That's not a gap in this count; it's where DSX genuinely isn't
open source, alongside hardware and facilities more broadly.

## What is next

This post is a snapshot, not a running total. For the current count and the full
list with licenses and status, the [materials index](dsx-repo-and-materials-index.md)
is the source of truth and updates as components move or new ones ship. What follows
this post are the individual component release posts: what shipped, the problem it
solves, and what's next, one component at a time. If there's a component you'd like
to see covered first, say so in [Discussions](https://github.com/dsx-ai-factory/community/discussions).
