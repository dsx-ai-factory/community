# Build NVIDIA Run:ai With Us: Join the Run:ai Contributor Workshop

Every AI platform eventually has to answer two questions: who gets the next GPU, and how quickly can a model start serving on it. On December 16, we are hosting the NVIDIA DSX Contributor Workshop for NVIDIA Run:ai and its family of related projects, in person at NVIDIA headquarters in Santa Clara, California, and online. Bring your engineering team, your technical challenges, and your integration ideas, and spend the day building with the NVIDIA maintainers.

The workshop covers eight projects, and each one is useful on its own:

- **[NVIDIA Run:ai](https://github.com/dsx-ai-factory/run-ai):** an open platform for orchestrating AI workloads and GPUs on Kubernetes.
- **[KAI Scheduler](https://github.com/kai-scheduler/KAI-Scheduler):** gang scheduling, fair share, and topology-aware placement. It is a CNCF Sandbox project that NVIDIA donated, and the community shapes it.
- **[KAI Resource Management](https://github.com/kai-scheduler/kai-resource-management):** projects, departments, quotas, and node pools.
- **[GPU Fractioning Operator](https://github.com/kai-scheduler/gpu-fractioning):** CUDA-native GPU fractions with hard memory isolation.
- **[Workload Map](https://github.com/dsx-ai-factory/workload-map):** one contract that describes any workload type.
- **[Model Streamer](https://github.com/dsx-ai-factory/model-streamer):** [add a one-line description].
- **[Snapshot](https://github.com/ai-dynamo/snapshot):** gets GPU pods ready in seconds instead of minutes by restoring a fully initialized workload.
- **[Grove](https://github.com/ai-dynamo/grove):** Kubernetes enhancements for network-topology-aware gang scheduling and autoscaling.

## Where these projects fit in DSX OS

These workshops are focused on model serving and the platform side of the DSX stack, the part where inference services get deployed and GPU capacity gets shared across workloads. In the [DSX OS documentation](https://docs.nvidia.com/dsx#dsx-os), that is the Model Serving domain, home to Model Streamer, Snapshot, and Grove, and the Workload and GPU Orchestration domain, home to NVIDIA Run:ai, KAI Scheduler, KAI Resource Management, the GPU Fractioning Operator, and Workload Map. The November workshop at KubeCon covered other parts of DSX OS, such as Accelerated Kubernetes and infrastructure, so this one is a chance to go deep on the platform your own services run on.

## Why participate

You get to work directly with the teams developing the software your platform can build on:

- **Advance integrations:** explore architecture and resolve technical questions with the maintainers.
- **Contribute improvements:** work on code, tests, documentation, examples, and actionable issues.
- **Shape project direction:** share your deployment experience, requirements, and proposed enhancements.
- **Build engineering relationships:** make contacts and agree on follow-up work.

## Who should attend

The workshop is for partner engineers, architects, and technical leads building GPU clouds, Kubernetes platforms, AI infrastructure, or complementary software, and both new and experienced contributors are welcome. If you have ever worked around a scheduling limit instead of reporting it, this is a good day to say what is missing. The architecture is still taking shape, so a pull request can influence how these projects handle real GPU fleets.

## What we are aiming for

The workshop is built around four goals:

- **Grow non-NVIDIA participation with the community.** The projects get better when the people who run them in production help shape them.
- **Build community momentum that outlasts the event.** We measure success by who is still contributing 90 days later, not by how many pull requests were opened on the day.
- **Accelerate ecosystem-wide collaboration.** Partners, platform builders, and maintainers in the same room make integration questions much easier to settle.
- **Convert new contributors into merged-pull-request authors.** Maintainers are on hand all day to review in real time, so that a first contribution ends up merged and not abandoned in a fork.

We would like you to leave with a contribution underway, an integration plan, a documented requirement, or a scoped joint engineering task.

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

Most of the morning goes to project-specific sprints, and there is plenty of time in them to talk with the product managers and maintainers of these projects. After lunch, partners share their insights, and the afternoon stays open for optional discussions. What you do in the sprints depends on where you are:

- **Starting out:** discuss the roadmap with the product managers and identify areas where you can contribute.
- **Already have an area in mind:** take that discussion further with the maintainers and land a pull request.
- **Working on a pull request:** get feedback from the maintainers and get it merged.
- **Already merged a pull request:** tell us more about which integrations need to be built next.

You do not need to write code to take part. Discussing the roadmap, filing an issue, or giving a maintainer feedback in person all count, and so does opening a draft pull request and getting a live review.

## How to get ready

Bring a laptop and a use case, integration challenge, or contribution idea, and share your interests in advance so we can match your team with the right maintainers. Pick a good first issue in KAI Scheduler or KAI Resource Management, join the #kai-scheduler channel on the CNCF Slack, and [request an invite to the DSX AI Factory Slack](https://inviter.co/dsx-ai-factory) so you can reach the team before and during the day. You are welcome to bring your favorite AI coding assistant.

## Express interest

[Contact and email.] Tell us your company, who is attending, the projects you are interested in, and optionally the work you would like to propose. Room details and preparation instructions will follow. If you cannot join us on the day, the issues are open and the maintainers are in the Slack, so you can start any time.

---

© 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
