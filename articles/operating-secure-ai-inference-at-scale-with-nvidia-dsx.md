# Operating Secure AI Inference at Scale with NVIDIA DSX

Serving AI inference at scale takes more than a validated, shared Kubernetes foundation. Teams need a serving architecture that keeps latency low as demand grows, a way to share the same GPUs fairly between inference and training, and security controls for the AI agents and sensitive data now running on that infrastructure.

At KubeCon \+ CloudNativeCon North America 2026, NVIDIA is demonstrating how selected [NVIDIA DSX OS](https://docs.nvidia.com/dsx#dsx-os) open-source components work together to operate secure, low-latency AI inference on shared infrastructure. This builds on the AI-ready, validated, and orchestrated foundation covered in *Managing Shared AI Infrastructure with NVIDIA DSX* \[link TBD\] — this recipe picks up from there and focuses on serving inference, sharing GPUs between inference and training, and securing agents and data in use.

## Serve inference with a disaggregated, low-latency architecture

Large model inference has distinct compute phases — processing the prompt and generating tokens — with very different resource profiles. Running both phases on the same worker leaves performance on the table, and loading model weights for every new worker from cold storage adds latency teams can't always afford.

[NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) addresses this with a disaggregated serving architecture:

* **Frontend/Router** receives inference requests and routes them to the right worker, supporting both aggregated and disaggregated serving.
* **Prefill and Decode workers** split the compute-heavy initial pass from token generation, handing off KV cache state between them over high-speed interconnects (NIXL) instead of recomputing it.
* **Model Express** loads a new worker's weights peer-to-peer from a GPU that already has them, instead of pulling cold from storage — cutting deployment-to-ready time significantly for new or scaled-out workers.
* **Snapshot** restores a new worker from a previously saved, initialized engine state instead of a cold model load, so replacing or scaling a worker doesn't mean paying the full startup cost again.

Together, these let teams serve inference with lower latency and faster scaling than a single-phase, cold-start architecture allows.

## Share GPUs between inference and training

Inference and training workloads rarely need the same resources at the same time, but teams still need both to run on shared GPU infrastructure without one starving the other.

[Grove](https://github.com/ai-dynamo/grove) and [KAI Scheduler](https://github.com/kai-scheduler/KAI-Scheduler) — introduced in the shared-infrastructure foundation above — extend naturally here: Grove defines a Dynamo deployment's frontend, prefill, and decode workers as a coordinated group with startup dependencies, and KAI Scheduler places that group according to available resources and policy.

For teams that already run Slurm, slurm-bridge lets Slurm schedule Kubernetes pods directly, so a single Slurm queue can decide scheduling for both an inference workload and a training job competing for the same GPUs — no separate scheduling system to reconcile.

## Secure AI agents and protect data and models in use

Running AI agents and serving models on shared infrastructure raises a different kind of question: what can an agent actually do, and who can see the data and weights while they're being used?

* [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) runs each AI agent in its own isolated sandbox, with its own execution environment and controls over what the agent can access — including which tools it can call and which network destinations it can reach.
* NVIDIA Confidential Computing protects prompts and model weights while they're in use — not just at rest or in transit — using hardware-backed trusted execution environments and attestation, so sensitive data stays protected even during active inference.

Both extend the same shared infrastructure described above: agents and the inference services behind them are workloads like any other, scheduled and resourced the same way, with these additional controls layered on top.

## Get started

* Explore the projects at [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory) and the broader [NVIDIA](https://github.com/NVIDIA) and [ai-dynamo](https://github.com/ai-dynamo) GitHub organizations, and watch the ones you rely on.
* Read the DSX OS overview and documentation at [docs.nvidia.com/dsx](https://docs.nvidia.com/dsx).
* Join the conversation in the [DSX AI Factory Slack](https://inviter.co/dsx-ai-factory).

Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions — this license covers the text of this document, not NVIDIA's trademarks. Other company, product, and service names may be trademarks of their respective owners.
