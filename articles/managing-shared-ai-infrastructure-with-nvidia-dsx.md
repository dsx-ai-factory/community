# Managing Shared AI Infrastructure with NVIDIA DSX

Shared AI infrastructure needs more than available GPUs. Teams need consistent Kubernetes environments, confidence that the infrastructure is healthy, and dependable access to shared resources.

At KubeCon + CloudNativeCon North America 2026, NVIDIA is demonstrating how selected [NVIDIA DSX OS](https://docs.nvidia.com/dsx#dsx-os) open-source components work together to support shared AI infrastructure. Together, these components address the challenges of provisioning AI-ready Kubernetes environments, validating infrastructure health, sharing GPU resources across teams, and managing development, training, inference, and AI agent workloads.

This recipe introduces the relevant projects, explains how they work together, and outlines the role each plays in the overall workflow. The linked repositories provide the implementation details needed to adopt the components in your own environment.

## Establish an AI-ready Kubernetes environment

Building AI-ready Kubernetes environments requires more than provisioning clusters. Platform teams need a way to operate managed Kubernetes infrastructure, maintain traceable software builds and releases, and establish validated runtime configurations for GPU-accelerated workloads.

Three open-source projects address these requirements.

- [NVIDIA Kubernetes Engine (NVKE)](https://github.com/dsx-ai-factory/nvke) is a newly announced open-source project that provides the management plane for running a managed Kubernetes service on NVIDIA GPU infrastructure. It enables platform teams to create independent Kubernetes workload clusters, each with its own control plane and node pools, and manage their lifecycle, including scaling and Kubernetes upgrades.
- [NVIDIA Kubernetes Recipes (NVKR)](https://github.com/dsx-ai-factory/nvkr) builds software artifacts for NVKE and AICR from pinned inputs, supporting traceable builds, publication, and release verification according to defined policies.
- [NVIDIA AI Cluster Runtime (AICR)](https://github.com/NVIDIA/aicr) provides version-locked recipes based on validated combinations of drivers, operators, and system configurations for GPU-accelerated Kubernetes environments. These recipes can be used to generate deployment configurations and validate the resulting runtime.

Starting with these components gives platform teams a reliable foundation on which to build shared AI infrastructure. This helps teams deploy and run AI workloads on a consistent, reproducible environment while reducing the risk of configuration mismatches and software compatibility issues.

## Validate infrastructure readiness and monitor health

GPU infrastructure can appear healthy until distributed AI workloads expose hardware failures or performance issues. Platform teams need to identify these problems before production workloads run and detect faults that arise during operation.

Two open-source projects address these challenges:

- [NVIDIA Cluster Readiness Engine (NVCRE)](https://github.com/NVIDIA/cluster-readiness-engine) runs distributed training and communication tests to assess GPU infrastructure readiness. It measures performance, identifies faulty nodes, and reports failures before production workloads are deployed.
- [NVSentinel](https://github.com/NVIDIA/NVSentinel) monitors GPU and node health during operation, detecting faults and supporting configurable responses such as node isolation, workload draining, and remediation.

These capabilities help establish a reliable foundation for shared AI infrastructure by validating GPU readiness before deployment and supporting ongoing infrastructure health. This reduces the risk of hardware issues disrupting distributed training, inference, and other AI workloads.

## Share GPU resources across teams

When multiple teams share GPU infrastructure, they need predictable access to resources without leaving available capacity unused. Different workloads also have different GPU requirements, from small development tasks to distributed training and inference. Managing this requires a way to allocate resources fairly, schedule workloads efficiently, and make better use of available GPU capacity.

Four open-source projects address these challenges:

- [KAI Resource Management](https://github.com/kai-scheduler/kai-resource-management) organizes resources across departments and projects, providing resource quotas and guarantees that determine how GPU capacity is allocated across teams.
- [KAI Scheduler](https://github.com/kai-scheduler/KAI-Scheduler) determines which workloads run and where they are placed, scheduling workloads according to available resources, priorities, and fairness policies.
- [GPU Fractioning Operator](https://github.com/kai-scheduler/gpu-fractioning) enables multiple workloads to share a physical GPU instead of each requiring an entire GPU. It works alongside KAI Scheduler to enforce fractional GPU memory allocations, improving utilization of shared GPU resources.
- [Workload Map](https://github.com/dsx-ai-factory/workload-map) provides a standardized way to describe Kubernetes workloads, regardless of their type or framework. KAI Scheduler uses these definitions to understand how pods are related and coordinate their scheduling, including for complex distributed AI workloads.

To see how these capabilities work together, consider two projects sharing GPU resources. Configure resource guarantees for each project and allow workloads to borrow unused capacity from the other. KAI Scheduler places workloads according to available resources, while GPU Fractioning Operator allows smaller workloads to share a physical GPU. When a project needs its guaranteed capacity, the scheduler can reclaim borrowed resources according to the configured scheduling policies. A preemptible borrowing workload returns to the queue and restarts when resources become available.

## Manage AI workloads through NVIDIA Run:ai

Managing shared GPU resources is only part of the challenge. Teams also need a way to submit, manage, and monitor different AI workloads across projects, from development and training to distributed inference and AI agents.

[NVIDIA Run:ai](https://github.com/dsx-ai-factory/run-ai) brings the orchestration projects together in an integrated, open-source platform for centralized GPU resource and workload management. Through its UI and APIs, teams can submit and manage workloads across projects, monitor their status and resource allocations, and track GPU metrics.

NVIDIA Run:ai can manage a wide range of AI workloads on the same shared infrastructure. Create development workspaces with fractional GPU allocations so developers can experiment without reserving an entire GPU, or run distributed training workloads across multiple workers.

For more complex workloads, integrate other NVIDIA open-source projects with NVIDIA Run:ai. Use [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) for distributed inference, coordinating frontend, prefill, and decode components to serve models. NVIDIA Run:ai manages the GPU resources and scheduling for these components alongside other AI workloads, allowing inference and training to share the same infrastructure.

The same shared infrastructure can also support AI agents through [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell). Run agents in isolated OpenShell sandboxes, with their models hosted by separate inference services. OpenShell controls what agents can access and do, including permissions, tools, and network connections, while NVIDIA Run:ai manages the scheduling and resources for the agent workloads and their inference services.

To support additional Kubernetes workload types, use [Workload Map](https://github.com/dsx-ai-factory/workload-map) to define their structure and relationships. NVIDIA Run:ai can use these definitions to recognize and manage workloads from different frameworks through the same platform, extending the range of applications teams can bring onto their shared GPU infrastructure.

## Get started

- Explore the projects at [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory) and watch the ones you rely on.
- Read the DSX OS overview and documentation at [docs.nvidia.com/dsx](https://docs.nvidia.com/dsx).
- Join the conversation in the [DSX AI Factory Slack](https://inviter.co/dsx-ai-factory).

> © 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
