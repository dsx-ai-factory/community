# Build NVIDIA Run:ai With Us: Join the Contributor Workshop on December 16

Every AI platform eventually has to answer two questions: who gets the next GPU, and how quickly can a model start serving on it. On December 16, we are hosting the NVIDIA DSX Contributor Workshop in person at NVIDIA headquarters in Santa Clara, California, and online. It focuses on model serving and the platform side of [DSX OS](https://docs.nvidia.com/dsx#dsx-os), through NVIDIA Run:ai and its family of related projects. Bring your engineering team, your technical challenges, and your integration ideas, and spend the day building with the NVIDIA maintainers.

The workshop covers eight projects, and each one is useful on its own:

- **[NVIDIA Run:ai](https://github.com/dsx-ai-factory/run-ai):** an open platform for orchestrating AI workloads and GPUs on Kubernetes.
- **[KAI Scheduler](https://github.com/kai-scheduler/KAI-Scheduler):** a Kubernetes-native scheduler for AI workloads at large scale, with batch scheduling, bin-packing and spread, workload priority, hierarchical queues, and fairness policies. It is a CNCF Sandbox project that NVIDIA donated, and the community shapes it.
- **[KAI Resource Management](https://github.com/kai-scheduler/kai-resource-management):** Kubernetes-native resource management with projects, departments, quotas, and node pools.
- **[GPU Fractioning Operator](https://github.com/kai-scheduler/gpu-fractioning):** CUDA-native GPU fractions with hard memory isolation.
- **[Workload Map](https://github.com/dsx-ai-factory/workload-map):** a standard way to describe the structure of any Kubernetes workload type.
- **[Model Streamer](https://github.com/dsx-ai-factory/model-streamer):** loads SafeTensors model weights as PyTorch tensors.
- **[Snapshot](https://github.com/ai-dynamo/snapshot):** gets GPU pods ready in seconds instead of minutes by restoring a fully initialized workload.
- **[Grove](https://github.com/ai-dynamo/grove):** Kubernetes enhancements for network-topology-aware gang scheduling and autoscaling.

The timing is good for engineers who like to get in early. Snapshot can now keep checkpoints in any S3-compatible object store, and vLLM and TensorRT-LLM have both merged the pieces it relies on. Model Streamer is getting faster at moving weights onto GPUs, with direct io_uring reads from block devices and reads straight into the device under tensor parallelism. Grove's APIs just reached beta while its integrations with the KAI Scheduler and Kueue keep deepening, and a new alpha node-assignment plugin in the KAI Scheduler is the first of a stack, with filtering, reclaim, metrics, and docs still to come. Workload Map now ships a CLI and a Headlamp plugin that runs a WebAssembly build of its engine. Most of this is unfinished in the best way, which is where a pull request counts for the most.

## Why participate

You get to work directly with the teams developing the software your platform can build on:

- **Advance integrations:** explore architecture, resolve technical questions with the maintainers, and tell us which integrations still need to be built.
- **Contribute improvements:** work on code, tests, documentation, examples, and actionable issues, whether you are starting out or getting a pull request merged.
- **Shape project direction:** discuss the roadmap and share your deployment experience, requirements, and proposed enhancements.
- **Build engineering relationships:** make contacts and agree on follow-up work.

We want more of the people who run these projects in production to help shape them, and we want that momentum to outlast the day, so we measure success by who is still contributing 90 days later. You should leave with a contribution underway, an integration plan, a documented requirement, or a scoped joint engineering task.

## Who should attend

The workshop is for partner engineers, architects, and technical leads building GPU clouds, Kubernetes platforms, AI infrastructure, or complementary software, and both new and experienced contributors are welcome. If you have ever worked around a scheduling limit instead of reporting it, this is a good day to say what is missing. The architecture is still taking shape, so a pull request can influence how these projects handle real GPU fleets.

## What the day looks like

The session runs in person and online, and all times are Pacific.

| Time | Topic |
| --- | --- |
| 8:30 – 9:00 AM | Arrival and Setup |
| 9:00 – 9:30 AM | Introduction to Run:ai platform and projects |
| 9:30 – 10:00 AM | Project-specific sprint, starts with project introductions |
| 10:00 AM – 12:30 PM | Contribution sprints |
| 12:30 – 1:15 PM | Lunch |
| 1:15 – 2:00 PM | Partner insights |
| 2:00 PM onwards | Optional discussions |

Most of the morning goes to project-specific sprints, and there is plenty of time in them to talk with the product managers and maintainers of these projects, who are on hand to review in real time. After lunch, partners share their insights, and the afternoon stays open for optional discussions.

You do not need to write code to take part. Discussing the roadmap, filing an issue, or giving a maintainer feedback in person all count, and so does opening a draft pull request and getting a live review.

## How to get ready

Bring a laptop and a use case, integration challenge, or contribution idea, and share your interests in advance so we can match your team with the right maintainers. Pick a good first issue in KAI Scheduler or KAI Resource Management, join the #kai-scheduler channel on the CNCF Slack, and [request an invite to the DSX AI Factory Slack](https://inviter.co/dsx-ai-factory) so you can reach the team before and during the day. You are welcome to bring your favorite AI coding assistant.

## Express interest

[Contact and email.] Tell us your company, who is attending, the projects you are interested in, and optionally the work you would like to propose. Room details and preparation instructions will follow. If you cannot join us on the day, the issues are open and the maintainers are in the Slack, so you can start any time.

---

© 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
