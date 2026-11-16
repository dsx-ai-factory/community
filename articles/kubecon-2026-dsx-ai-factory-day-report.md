# **Ground to Token: NVIDIA's DSX AI Factory Message at KubeCon**

## **Executive summary**

NVIDIA's message at DSX Day (KubeCon North America, Salt Lake City, November 2026\) was simple: the AI factory is the new unit of compute, and the metric that matters is how fast a site goes from bare ground to serving tokens. Everything presented, close to 20 open-source projects across three sessions, was positioned as a piece of that one mission.

![Bob Wise opening DSX Day with the slide What is DSX AI Factory Platform?][image1]

*Opening DSX Day at KubeCon North America, Salt Lake City.*

Five ideas carried the day:

1. **Ground-to-token time is the KPI.** Trillions of dollars are flowing into AI factories, so every week a cluster sits unconfigured, unhealthy or cold is lost return. DSX exists to shrink that time.  
2. **One stack, fully modular, fully open.** DSX runs from power-grid protocols to inference serving. Every layer is meant to be usable on its own, inside someone else's platform.  
3. **NVIDIA is moving up the stack into Kubernetes itself.** Projects such as NVKE, NVKR, AICR and NodeWright let AI factory operators go from raw GPU capacity to a managed Kubernetes service, and then to AI services on top.  
4. **Inference economics are a memory problem.** Dynamo treats every GPU's memory across the cluster as one shared pool, and attacks the two costliest wastes: recomputing work already done and waiting minutes for workers to start or recover.  
5. **Community is the strategy, not a side effect.** NVIDIA framed contributions, roadmap feedback and hiring (50 open Kubernetes roles) as how the stack gets built, and explicitly asked the room to file issues.

The quick reference below names every project in one line. The rest of the paper walks the stack from the ground up, follows one NVL72 rack through a working day, then covers the open-source play and the open questions raised in the room.

## **Quick reference: every project in one line**

Short on time? This is what each project does, ordered from the power feed up to the AI agent. Details are in the sections below, and repos and presenters are in the Project reference at the end.

| Project | What it does | Status |
| :---- | :---- | :---- |
| **DSX Flex, Exchange, MaxLPS, Sim** | The facility layer: protocols for talking to the power grid and building systems, dynamic power software, and site simulation | On the DSX map; not covered in depth |
| **NICo** | Discovers and provisions bare-metal GPU servers, DPUs and racks through APIs, including firmware and tenant isolation | Shipping |
| **Topograph** | Discovers how the cluster is wired and labels nodes so work lands in the right place | On the DSX map |
| **NVKR** | Builds signed node OS images and Kubernetes components from pinned, validated inputs | Preview |
| **NVKE** | Creates and runs many Kubernetes clusters on your own GPU bare metal, as a managed service | Preview |
| **AICR** | Works out, installs and validates the right drivers and operators for your GPU, cloud, OS and workload | Graduated |
| **NodeWright** | Changes the host OS under Kubernetes nodes safely and declaratively, without re-imaging | Shipping |
| **GPU Operator, Network Operator, DRA driver** | Install GPU drivers and networking on each node and hand GPUs to the workloads that request them | Long-standing |
| **NVSentinel** | Spots GPU faults, moves work off the node, and repairs it automatically | Graduated |
| **Cluster Readiness Engine** | Burns in a cluster with real training and NCCL tests before it takes production work | New |
| **NVIDIA Run:ai** | Shares GPUs across teams and clusters with quotas, policies, scheduling and visibility | Open source |
| **KAI Scheduler** | Decides which workload gets the next GPU: gang scheduling, fair share, GPU fractions, topology awareness | CNCF Sandbox |
| **Workload Map (Karta)** | One standard description of any Kubernetes workload type, so tools handle them all without custom code | Pre-1.0 |
| **Slinky** | Runs Slurm jobs and Kubernetes workloads in one queue on the same GPUs | Not yet part of DSX |
| **Dynamo** | Turns a GPU cluster into one inference system: smart routing, shared KV cache, split prefill and decode, autoscaling | 1.0 |
| **Grove** | Places the parts of a multi-node inference workload together across the NVLink domain | Part of Dynamo |
| **Model Express** | Starts new inference workers by copying model weights from a peer GPU instead of from disk | Part of Dynamo |
| **Snapshot** | Restores a fully started GPU worker in seconds instead of a minutes-long cold start | Preview |
| **Agent Substrate** | Secure runtime for agent sandboxes that suspends idle ones and wakes them on demand | Early |

## **The thesis: shrink ground-to-token time**

Warren Barkley, who runs the DSX product business, called it the "uber mission": shrink the time it takes to go from ground to token. His reasoning was economic. When trillions of dollars go into AI factories, the owners need tokens coming out as soon as possible.

He framed DSX as the third step in a progression:

1. **Servers** — NVIDIA used to sell 1U boxes.  
2. **Rack scale** — systems like the NVL72 made the rack the unit.  
3. **AI factories** — the whole site, from power and cooling to model serving, is now the unit, and needs a software stack to match.

Two supporting claims mattered:

* **This is not just for neoclouds.** Warren said "pretty well every hyperscaler you can name" already runs pieces of this open source on tens of thousands of GPUs.  
* **NVIDIA runs it on itself.** NVIDIA's internal research cloud (DGX Cloud) is about 368,000 GPUs today, with a plan to reach one million by the end of 2027\. Lessons from operating that fleet feed the roadmap; customer use cases fill the gaps NVIDIA's own workloads don't cover.

Why it matters: NVIDIA is shifting the conversation from "how many GPUs" to "how quickly do those GPUs earn." Every project below is pitched as removing a delay somewhere between the power feed and the first token.

## **The map: one stack from power grid to model serving**

DSX is NVIDIA's name for the full AI factory software stack, and the opening slide from Bob Wise, Warren's engineering counterpart, shows it as layers. The bottom row is new territory for a chip company: protocols for talking to the power grid (Flex) and to building management systems (Exchange), plus power software and site simulation. Above it sits **DSX OS**, the software that runs inside the data center.

![DSX AI Factory Platform · redrawn from the session slide][image2]

DSX AI Factory Platform · redrawn from the session slide

The hands-on workshop then narrowed this to a working slice, "from nodes to the model, in one stack": NVIDIA GPU nodes, a Kubernetes cluster created by NVKE (whose images NVKR builds), the GPU Operator, DRA driver and NVSentinel as the GPU runtime (installed and validated by AICR), KAI Scheduler for scheduling, and Dynamo, Grove, Model Express and Snapshot serving NVIDIA's Nemotron model. Slurm batch jobs run in the same cluster through Slinky.

![The stack for the day slide: from nodes to the model, in one stack][image3]

*The workshop's hands-on slice, from NVIDIA GPU nodes to the Nemotron model, with Slurm jobs sharing the same cluster.*

The sections that follow walk this slice from the bottom up.

## **The foundation: from bare metal to a working GPU cluster**

NVIDIA's foundation message: getting a GPU cluster from racked hardware to "ready for AI" takes too long, and NVIDIA now ships open-source tools for every step. Eric Chapman summed up the direction as helping operators move "from bare-metal GPU capacity, to Kubernetes as a managed service, and ultimately to on-demand AI services on top of Kubernetes."

The chain runs in this order:

| Step | Project | What it does | Status |
| :---- | :---- | :---- | :---- |
| 1\. Bring up the hardware | **NICo** (NVIDIA Infrastructure Controller) | Discovers bare-metal GPU servers, DPUs and racks; handles firmware, network paths, tenant isolation and secure reuse through APIs | Shipping; new Cluster API provider (CAPNICo) |
| 2\. Pin the software | **NVKR** (NVIDIA Kubernetes Recipes) | Build and release system for NVKE that pins a validated combination of node OS, Kubernetes distribution and per-node components for each GPU generation; builds, signs and publishes them to an OCI registry with SBOMs and provenance you can verify.  | Preview; not yet for production |
| 3\. Create the cluster | **NVKE** (NVIDIA Kubernetes Engine) | Management plane for running a managed Kubernetes service on your own GPU bare metal: creates independent workload clusters (each with its own control plane, etcd and node pools) through an API or nvkectl, provisions machines through NICo, manages node pools and upgrades, and attests each node with SPIFFE/SPIRE and its TPM before it joins. Clusters ship with OVN-Kubernetes as CNI (with DPU offload) and an OpenTelemetry pipeline.  | Preview; not yet for production; NICo is the only supported infrastructure provider |
| 4\. Configure the cluster | **AICR** (AI Cluster Runtime) | Captures known-good combinations of drivers, operators, kernels and system settings as version-locked recipes for your exact GPU, Kubernetes version, cloud and workload; outputs Helm, Argo CD, Flux, Helmfile, Terraform and more; then validates the live cluster. It configures clusters but does not create them.  | Graduated |
| 5\. Change the hosts safely | **NodeWright** (formerly Skyhook) | Kubernetes-aware package manager for the host OS under your nodes: declarative, with interruption budgets, node selectors and protected pods; cordons, drains and reboots only when a package needs it; updates drivers, kernel modules and config in place, no re-imaging | Shipping |

![Build the Kubernetes foundation with NVKE and NVKR slide][image4]

*NVKR builds and publishes, the NVKE management plane drives workload clusters, and NICo provisions the bare-metal GPU machines.*

Under all of this sit the long-standing building blocks Francis Guillier reviewed: the **GPU Operator** (driver, container toolkit, device plugin), the **Network Operator**, the **DRA driver** for GPU resource allocation, and **Topograph** for topology discovery.

### **Why AICR got the most airtime**

Nathan Taber described the problem in customer terms. Teams told NVIDIA they spent two to three weeks or more re-tuning dozens of parameters every time a new GPU SKU arrived or Kubernetes was upgraded. Both now happen often.

AICR's workflow is four steps: **snapshot** the cluster's facts, **pick an intent** and resolve a recipe, **bundle** it into deployment artifacts, then **deploy and validate**. Validation runs at three levels: deployment, conformance and performance, up to the CNCF AI conformance checks. It runs as a CLI, a REST API server, a Go library and an in-cluster snapshot agent; NVIDIA also announced an AICR operator that keeps a cluster up to date. Every recipe ships with signed provenance and SBOMs.

Two points stood out:

* **Day-zero support is the goal.** Nathan's stated aim: nobody should take delivery of a new NVIDIA GPU and not know how to run it. Vera Rubin recipes landed about a week before the event.  
* **Recipes are built dynamically, in layers** (GPU, workload, cloud, OS). That design is deliberate so outside companies can contribute their own optimizations.

As of the October 29, 2026 support slide, AICR covers 12 Kubernetes services (EKS, GKE, AKS, OKE, LKE, MK8s, OpenShift, RKE2, k0s, NVKE, bare metal, kind), 11 GPU accelerators from A100 and L40 through GB300 and VR200, 5 operating systems, 6 deployer families, and 5 workload platforms (Kubeflow, Slurm, Kueue, Dynamo, NIM). Items marked preview include VR200, RKE2, k0s and NVKE. This slide is newer than the repo's README, which still lists a different validated set (for example BCM, Metal3, RHEL and Talos, plus Run:ai as a platform).

![AICR What's supported today slide][image5]

*AICR coverage as of October 29, 2026\. Items marked \* are in preview.*

### **The modularity promise**

Eric was explicit that none of this forces an all-NVIDIA stack. If you already have a Kubernetes management system, use NVKR to build what it runs. If you run a Cluster API system, plug in the NICo provider. AICR installs on any cluster, NVKE-made or not. If the NVKE management plane goes down, existing clusters keep running; you just can't create new ones until it's back.

![NodeWright six-step flow slide][image6]

*NodeWright's six-step flow changes the hosts under Kubernetes nodes without re-imaging.*

## **Health and resilience: GPUs are brittle, so automate the repair loop**

NVIDIA's point here: a node that looks healthy is not the same as a cluster that can survive a large training run, and you need both a passive and an active check. Kai Wombacker presented the pair as one integrated loop.

|  | NVSentinel | NVIDIA Cluster Readiness Engine (NVCRE) |
| :---- | :---- | :---- |
| Question it answers | Is this node healthy right now? | Can this cluster survive real training? |
| Mode | Passive, always on, plus an optional Preflight check before a job starts | Active certification, deep burn-in |
| How | Real-time GPU, NIC and system fault detection via DCGM, syslog and cloud-provider maintenance events (XID, ECC, NVLink and thermal faults among them) | Runs real distributed training and NCCL burn-in, topology-aware across node groups; measures training goodput and bandwidth |
| Action | Cordons and drains the faulty node, then remediates with a targeted GPU reset or a reboot. Each step is opt-in; the default install only monitors | Reports failed nodes before they reach production |
| Maturity | Graduated; scales to some of the largest supercomputer clusters | New |

The two feed each other. Nodes that fail certification are routed to NVSentinel for repair. Nodes coming back from repair can be re-certified automatically. On the roadmap, once a "Maestro" integration lands, nodes needing hardware repair will route there for break-fix.

![Active and Passive GPU Cluster Reliability slide][image7]

*NVCRE certifies, NVSentinel detects and repairs, and each routes nodes to the other.*

The wider portfolio on the DSX map also lists Health Validation, Attribution and Recovery, which were mentioned but not presented.

This ties back to the opening session. Warren cited advisory-board feedback along the lines of "GPUs are brittle and I want to run them at several nines." NVIDIA's response was to open-source the health tooling it runs internally.

## **Scheduling and orchestration: deciding who gets the next GPU**

The message here: GPUs are scarce, expensive and shared, so the scheduler is where utilization and fairness are won or lost. NVIDIA has broken Run:ai into open, standalone parts so others can use them in their own platforms.

**NVIDIA Run:ai** (Omer Benedict) is now open source under Apache 2.0. It is an AI workload and GPU orchestration platform: one control plane that manages many Kubernetes GPU clusters, with governance through departments, projects, quotas, policies and RBAC, full metrics, and UI, CLI, REST API and MCP server interfaces. Four of its core projects are also usable on their own:

| Project | What it does |
| :---- | :---- |
| **KAI Scheduler** | Gang scheduling, fair share, GPU fractions and topology-aware placement. Now a CNCF Sandbox project. |
| **KAI Resource Management** | Projects, departments, quotas and node pools. Just open-sourced. |
| **GPU Fractioning Operator** | CUDA-native GPU fractions with hard memory isolation. |
| **Workload Map** | One contract that describes any workload type (see below). |

Hagay Sharon's pitch for KAI Scheduler was aimed squarely at contributors: the architecture is still taking shape, so a PR now can define how the industry schedules AI workloads, and the code will run on real GPU fleets.

**Workload Map** (Yael Frank), published as the open-source project **Karta**, solves a quieter problem: Kubernetes has no common way to see the status of every workload, because each framework brings its own CRD. A Karta definition uses jq path expressions to say where a workload's pod templates, replica counts and status live, so schedulers, controllers and dashboards can read and update any workload type through one SDK. The catalog covers 20+ frameworks (Dynamo, Grove, Ray, Kubeflow, Agent Sandbox, KServe and more). Tools such as KAI Scheduler, Run:ai, NVIDIA Cloud Functions and NVIDIA Recovery read it, so "build on it once, and your app supports them all." It includes a CLI and supports suspend and unified status. 

**Slinky** brings Slurm and Kubernetes together. The Slurm team, which joined NVIDIA through an acquisition last year, presented two pieces: **slurm-operator** runs Slurm inside a Kubernetes cluster, and **slurm-bridge** translates Kubernetes pods into Slurm jobs. The result is one queue and one pool of compute where training and inference coexist, with Slurm's priority, preemption, backfill and fair share. Slinky is not yet formally part of DSX.

![Slinky unified scheduling of Slurm and Kubernetes slide][image8]

*Developers submit with kubectl, researchers with sbatch; both land in one queue on shared compute.*

Asked directly whether Run:ai and Slinky overlap, NVIDIA said yes. Both act as Kubernetes scheduling plugins with different approaches, each has places where it is stronger today, and the teams are collaborating through upstream Kubernetes groups rather than forcing a merge.

## **Inference with Dynamo: treat the cluster's memory as one pool**

The longest session was a hands-on Dynamo workshop, and its message was that serving cost is driven by two wastes: redoing work the cluster has already done, and waiting for workers to start. Dynamo, which reached version 1.0 in March 2026, is an orchestration layer above inference engines (vLLM, SGLang, TensorRT-LLM): it doesn't replace them, it coordinates them across nodes with disaggregated serving, KV-aware routing, multi-tier KV caching and SLA-driven autoscaling. Its tagline: "Turn a GPU cluster into one inference system."

![Dynamo slide: turn a GPU cluster into one inference system][image9]

*Dynamo routes requests across vLLM, SGLang and TensorRT-LLM workers as one coordinated GPU cluster.*

The demo ran NVIDIA's Nemotron 120B model (NVFP4, about 80 GB on disk) on vLLM, on a 3-node, 24-GPU cluster, using an agentic coding workload because its context grows on every turn.

### **The fundamentals NVIDIA wanted everyone to hold**

* **Two phases, two bottlenecks.** *Prefill* reads the prompt and builds the KV cache; it is compute-heavy and sets time to first token (TTFT). *Decode* generates one token at a time; it is memory-bandwidth-heavy and sets inter-token latency.  
* **GPU memory has three tenants.** Model weights (fixed), workspace (activations, buffers, graphs) and the KV cache. The KV cache grows with context length and with the number of users, so it is what limits concurrency.  
* **There is a memory ladder.** On-chip SRAM, then HBM, then host DRAM, then remote storage: each step down is cheaper, larger and slower. When HBM fills, the engine must evict (and later recompute) or offload.  
* **Throughput and interactivity trade off.** Pushing tokens-per-second-per-user up serves fewer people per megawatt; pushing concurrency up serves more people more slowly. Batch and RL rollouts sit on one end, interactive chat on the other.

### **Four techniques, each aimed at a specific waste**

| Technique | Waste it removes | How it works | Result shown |
| :---- | :---- | :---- | :---- |
| **Model Express** | Slow scale-up from storage | New workers pull weights peer-to-peer from a worker that already has them, over NVLink or RDMA via the NIXL library, instead of reading disk. A small metadata server tracks who holds what. It has its own repo and a vLLM loader, so it works without the rest of Dynamo. | Startup 463 s to 246 s |
| **KV-aware routing** | Recomputing prompts already cached | Workers publish KV-cache events; the router knows which blocks sit on which worker and at what memory tier. It scores each worker on cache overlap and on current load, so it avoids both recompute and hotspots. | P90 latency at 128 users: 140 s (1 worker), 113 s (2 workers, round-robin), 54 s (2 workers, KV-aware). Prefill work cut from 54 blocks to 25 in the example |
| **KVCR** (KV cache sharing) | Cache stuck on the wrong worker | If the router sends a request to a worker without the cache, that worker pulls the cache from the worker that has it. All GPU memory in the cluster acts as one KV pool. Works standalone with vLLM or SGLang. | TTFT on a 60k-token prompt: 2,417 ms cold vs 319 ms with a pulled cache. Benchmarks: 25 to 50% speedups, 2x faster TTFT on one DeepSeek benchmark, a production user seeing a 14% higher cache hit rate |
| **Disaggregation** | Long prompts stalling everyone's decode | Prefill and decode run on separate worker pools, each sized and tuned for its phase; the KV cache moves between them over NIXL. | Roughly halved TTFT in a larger NVIDIA test; gains are biggest with long prompts, long outputs and high concurrency |

**Dynamo Planner** closes the loop by autoscaling prefill and decode pools independently. It runs in one of two modes: a *load* mode that checks queued prefill tokens and decode KV demand every 5 seconds, or an *SLA* mode that targets a latency goal (the example: 500 ms TTFT and 50 ms between tokens) and forecasts demand every 3 minutes to add replicas ahead of need.

Multi-tenancy came up from the floor. Beyond separate namespaces or clusters, Dynamo can apply a per-tenant salt to the KV-cache hash, so one tenant can never reuse another's cache.

On Dynamo versus NIM, NVIDIA was candid: NIM is the simple, packaged, one-or-two-command option; Dynamo is "batteries not included" and far more configurable, which is why it needed a multi-hour workshop.

## **Fault tolerance: a failed worker should cost seconds, not minutes**

NVIDIA's point: in production, the expensive part of a failure is not the lost request but the minutes of degraded capacity while a worker restarts. A cold vLLM worker took about 8 minutes end to end in the demo, and the Snapshot slide showed cold starts of 394 s (GLM-5.3), 908 s (DeepSeek-V4-Pro) and 1,111 s (DeepSeek-V4.1). The usual fix is to over-provision GPUs and pay for them to sit idle. Dynamo and its companion projects offer a ladder of tools instead, one per failure type.

![Figures stated in the Dynamo workshop transcript and on the Snapshot slide · KubeCon NA 2026][image10]

Figures stated in the Dynamo workshop transcript and on the Snapshot slide · KubeCon NA 2026

| Failure | Tool | What it does |
| :---- | :---- | :---- |
| Any fault mid-request | **Request migration** | The router moves an in-flight request to another worker; the client keeps receiving the same stream. Also lets you drain workers on scale-down without killing requests. |
| Engine crash or hang, GPU fine | **GPU Memory Service \+ Shadow engine** | Weights live in a separate process's shared CUDA memory. A pre-compiled "shadow" vLLM process sleeps on the same weights and takes over in about 7 s when the active engine dies. Costs about 200 to 250 MB per GPU. |
| Engine crash, cache worth keeping | **KVCR Guard** | A separate process owns the CPU-side KV cache, so it survives the worker. Other workers keep pulling that cache, and the restarted worker reloads it. |
| GPU failed or node lost | **Snapshot** | A standalone, Kubernetes-native checkpoint and restore system that Dynamo integrates. It checkpoints a fully started worker (CUDA context, kernels, CUDA graphs, NCCL state, and today the weights) using CRIU plus CUDA checkpointing, then restores it on another GPU or node with matching hardware and driver. About 30 s in the demo. |
| Any scale-up (roadmap) | **Snapshot \+ Model Express** | Restore everything except weights from the snapshot, stream weights from a peer. About 14 s in preview. |

Snapshot is also a scaling tool, not only a recovery tool: take one snapshot of the first worker and use it to start every replica. Ron Kahn's framing on the slide was "capture a ready worker once, restore it to Ready every time."

![Snapshot: The Cold Start Answer slide][image11]

*Capture a ready worker once, restore it to Ready every time.*

## **Agent Substrate: the next workload shape**

NVIDIA's forward-looking message: AI agents break the assumptions Kubernetes was built on, and the community is building a new primitive for them. Running large numbers of agent sandboxes as ordinary pods has hit the limits of the Kubernetes control plane.

**Agent Substrate** is described as a security-hardened, zero-trust runtime for sandboxed agent environments. It has two core concepts:

* **Workers** — the pods, grouped into worker pools.  
* **Actors** — the agent environments scheduled onto those workers.

The key observation is that most agent sandboxes sit idle most of the time. Agent Substrate snapshots an idle environment, suspends it, and resumes it only when a user sends the next request. This is the same snapshot-and-restore idea as the Snapshot project, applied to agents instead of model servers.

What NVIDIA is building around it:

* **A policy layer (new project).** Version 1 scheduling is simple. NVIDIA is starting a project for a policy layer between Agent Substrate and AI platforms, to decide who gets access first across sandboxes, RL workloads and other agent tasks, using CNCF concepts like quotas and priorities. They asked practitioners for input.  
* **Dynamo integration.** A user guide shows how to run an inference endpoint plus sandboxes on top of Agent Substrate.  
* **OpenShell.** The OpenShell team is working on a proof of concept with the Agent Substrate team; details were not shared.

The Dynamo team also mentioned built-in integrations with agent frameworks (they named OpenCode and Claude Code) that send hints about session state, so the KV cache can be pinned, spread or evicted at the right time.

## **A day in the life: one NVL72 rack, from loading dock to live tokens**

The easiest way to see why each project exists is to follow one rack. Picture a platform engineer at an AI factory who takes delivery of a GB300 NVL72: 72 GPUs across 18 compute trays, joined by one NVLink domain. By the end of the day it is serving an AI coding agent. Every step below is handled by one of the open-source projects NVIDIA presented.

This is an illustrative workflow assembled from the DSX Day sessions, not a published NVIDIA runbook. Several of the pieces (NVKE, NVKR, Snapshot, Agent Substrate) are still in preview.

### **Morning: from racked hardware to a cluster that's ready to serve**

![Day 0 for one GB300 NVL72 · illustrative, assembled from the DSX Day sessions][image12]

Day 0 for one GB300 NVL72 · illustrative, assembled from the DSX Day sessions

Two things run in the background all day. **NVSentinel** watches every GPU from the moment the cluster exists, and **AICR**'s validation can be rerun after any upgrade to confirm nothing has drifted.

The chain is also swappable, which was NVIDIA's modularity point. An operator who already runs their own Kubernetes platform can skip NVKE and still use NVKR images, the NICo Cluster API provider, and AICR on top.

### **Afternoon: an agent's request comes in**

The rack now serves a coding agent. Every turn the agent sends repeats the repository, the conversation so far and the latest tool output, so most of each prompt is something the cluster has already processed.

![One agent request on the NVL72 · illustrative, assembled from the Dynamo workshop][image13]

One agent request on the NVL72 · illustrative, assembled from the Dynamo workshop

On a quiet afternoon that is the whole story. The interesting part is what happens when something changes, because that is where the rest of the stack earns its place.

| Event | What happens | Projects doing it |
| :---- | :---- | :---- |
| Traffic spikes and time to first token drifts past its target (500 ms in the session example) | Planner adds prefill or decode workers; KAI Scheduler and Grove place them inside the NVLink domain; each new worker restores from a snapshot and pulls weights from a peer instead of disk, so it is ready in seconds | Dynamo Planner, KAI Scheduler, Grove, Snapshot, Model Express |
| A GPU throws an XID error mid-response | NVSentinel detects it through DCGM, then cordons and drains the tray. Dynamo migrates the in-flight request, so the agent's stream keeps flowing. KVCR Guard keeps that worker's cached context available to other workers | NVSentinel, Dynamo request migration, KVCR Guard |
| The faulty tray is repaired | NVSentinel resets the GPU or reboots the tray; Cluster Readiness Engine re-certifies it before it takes work again; a replacement worker restores from a snapshot | NVSentinel, Cluster Readiness Engine, Snapshot |
| A driver or kernel fix has to roll out | NodeWright applies it tray by tray within an interruption budget, cordoning and draining only where the package needs a reboot | NodeWright |
| The agent goes idle between turns | Agent Substrate snapshots and suspends its sandbox, then resumes it when the next request arrives | Agent Substrate |
| The next GPU generation lands | AICR already has a validated recipe for it, and NVKR builds the matching node image | AICR, NVKR |

The point NVIDIA was making is that no single project is the product. Each one removes a specific delay between the ground and the token, and each can be replaced by something the operator already runs.

## **The open-source play: community as a delivery strategy**

Every NVIDIA speaker returned to the same request: contribute, give feedback, and shape the roadmap. The scale of the commitment was stated in numbers.

* **Volume.** Over 200 projects released in the last 12 months and another 26 recently, plus projects donated to the community (OpenShell, the DRA driver and NVKE among those named).  
* **People.** Arun Gupta now runs open-source strategy, and NVIDIA has hired long-time open-source figures. Aaron Boyd, who runs Kubernetes engineering, announced 50 open roles across AICR, NVKE, NVKR and related projects.  
* **Ecosystem.** NVIDIA became a CNCF Platinum member and KAI Scheduler is a CNCF Sandbox project. Speakers stressed vendor neutrality: "we don't care who you work for."

Arun was precise about how feedback becomes roadmap. NVIDIA counts four kinds of contribution: a new issue, a PR, a comment on an existing issue, or a comment on an existing PR. His blunt rule: "If it's not captured as an issue, it probably won't be acted upon." Doc fixes, UX feedback and "here is what you're not doing right" all count.

The event itself modeled the flywheel NVIDIA wants. A morning of talks was followed by an afternoon contributor workshop with product managers at assigned tables, a show-and-tell of what attendees built, and the first in-person community meetings, split into four groups. Several projects will now run virtual community meetings in CNCF style.

The subtext is strategic. By making each layer open and usable alone, NVIDIA invites hyperscalers, neoclouds and platform vendors to build on its software rather than around it. That keeps NVIDIA's view of how an AI factory should run at the center of the stack, even where NVIDIA does not own the platform.

## **Caveats and open questions from the room**

NVIDIA was open about limits, and the audience pushed on several points. These are the gaps worth knowing before repeating any claim above.

| Topic | What was raised | NVIDIA's answer |
| :---- | :---- | :---- |
| Maturity | NVKE and NVKR | Both described as "very new and early" and in preview. Their READMEs say they aren't for production yet, and no NVKR release is qualified. The roadmap is open for input. |
| Networking | Why RoCE and RDMA are missing from the foundation diagram | Handled by the Network Operator inside the accelerated runtime, a few layers below what NVKE shows |
| Networking | Why NVKE uses OVN-Kubernetes when NVIDIA's reference architecture suggests HBN | OVN-Kubernetes is the new reference CNI for accelerated Kubernetes; more CNI work with DPU offload is due late November or early December 2026 |
| Resilience | What happens if the NVKE management cluster fails | Workload clusters stay up ("statically stable"); only new cluster operations stop |
| Shadow engine | Is it free? | No: about 200 to 250 MB of GPU memory per standby engine |
| Snapshot | Portability | Restores only onto matching hardware (same GPU and CPU type), and only single-node workloads for now. The KV cache isn't included but the weights are, which makes snapshots large. The repo says it isn't yet recommended for production-critical workloads. |
| Tuning | Is there an auto-tuner for NIXL and network settings? | Not in Dynamo today; some tuning sits in AICR and NVKE, the rest is manual |
| Integrations | Does OpenShell integrate with the Dynamo router? | Unknown to the presenter; the Dynamo team confirmed integrations with OpenCode and Claude Code |
| Overlap | Run:ai versus Slinky | Acknowledged; teams are collaborating upstream rather than merging |

## **Project reference**

Repos as shown on the session slides; presenters as named on the slides. Descriptions follow what NVIDIA's PMs presented; where that is newer than a repo's README (checked November 15, 2026), the text says so.

| Project | Layer | Presenter | Repo |
| :---- | :---- | :---- | :---- |
| NVIDIA Run:ai | Orchestration | Omer Benedict | [github.com/dsx-ai-factory/run-ai](https://github.com/dsx-ai-factory/run-ai) |
| KAI Scheduler | Orchestration | Hagay Sharon | [github.com/kai-scheduler/KAI-Scheduler](https://github.com/kai-scheduler/KAI-Scheduler) |
| Workload Map (Karta) | Orchestration | Yael Frank | [github.com/dsx-ai-factory/workload-map](https://github.com/dsx-ai-factory/workload-map) |
| Dynamo | Model serving | Stefan Schimanski | [github.com/ai-dynamo/dynamo](https://github.com/ai-dynamo/dynamo/) |
| Snapshot | Model serving | Ron Kahn | [github.com/ai-dynamo/snapshot](https://github.com/ai-dynamo/snapshot) |
| Grove | Model serving | Dynamo workshop team | [github.com/ai-dynamo/grove](https://github.com/ai-dynamo/grove) |
| Model Express | Model serving | Dynamo workshop team | [github.com/ai-dynamo/modelexpress](https://github.com/ai-dynamo/modelexpress) |
| NVSentinel and NVCRE | Health and resilience | Kai Wombacker | [github.com/NVIDIA/NVSentinel](https://github.com/NVIDIA/NVSentinel) |
| AI Cluster Runtime (AICR) | Accelerated Kubernetes | Nathan Taber | [github.com/NVIDIA/aicr](https://github.com/NVIDIA/aicr) |
| NodeWright | Accelerated Kubernetes | Nathan Taber | [github.com/NVIDIA/nodewright](https://github.com/NVIDIA/nodewright) |
| NVKE | Accelerated Kubernetes | Eric Chapman | [github.com/dsx-ai-factory/nvke](https://github.com/dsx-ai-factory/nvke/) |
| NVKR | Accelerated Kubernetes | Eric Chapman | [github.com/dsx-ai-factory/nvkr](https://github.com/dsx-ai-factory/nvkr/) |
| GPU Operator | Accelerated Kubernetes | Francis Guillier | Not shown |
| NICo | Infrastructure operations | Ninad Desai | [DSX docs](https://docs.nvidia.com/dsx) |

## **Glossary**

| Term | Meaning |
| :---- | :---- |
| AI factory | A data center built to turn power into AI output (tokens), treated as one system from the grid connection to model serving |
| Burn-in | Running a heavy, realistic workload on new or repaired hardware to catch faults before production |
| Cluster API (CAPI) | A Kubernetes standard for creating and managing clusters through Kubernetes-style APIs |
| Cold start | The minutes an inference worker spends loading weights and compiling before it can answer requests |
| CRD | Custom Resource Definition: how a framework adds its own object types to Kubernetes |
| DCGM | NVIDIA Data Center GPU Manager, the tool that reports GPU health and telemetry |
| Decode | The phase of inference that generates the answer one token at a time; limited by memory bandwidth |
| DPU | Data processing unit, such as NVIDIA BlueField, which takes networking and security work off the CPU |
| Gang scheduling | Starting all the pods of a distributed job together, or none of them |
| KV cache | The model's working memory of a prompt; reusing it avoids recomputing the same tokens |
| NCCL | NVIDIA's library for GPU-to-GPU communication in distributed jobs |
| NIXL | NVIDIA Inference Xfer Library, used to move weights and KV cache quickly between GPUs and nodes |
| NVL72 | A rack-scale system with 72 GPUs joined in one NVLink domain, so they can act like one large GPU |
| Prefill | The phase of inference that reads the prompt and builds the KV cache; limited by compute |
| TTFT | Time to first token: how long a user waits before the answer starts |
| XID error | An error code the NVIDIA driver reports when a GPU has a fault |

## **Learn more**

Rafay has been working closely with NVIDIA to integrate much of the DSX work described in this paper into the Rafay platform. We are also working with customers to run it in production.

Want to see how this applies to your AI infrastructure, or talk through what it takes to get from ground to token faster? Reach out to me. 

[image1]: images/kubecon-2026-dsx-ai-factory-day-report/image1.jpg
[image2]: images/kubecon-2026-dsx-ai-factory-day-report/image2.png
[image3]: images/kubecon-2026-dsx-ai-factory-day-report/image3.jpg
[image4]: images/kubecon-2026-dsx-ai-factory-day-report/image4.jpg
[image5]: images/kubecon-2026-dsx-ai-factory-day-report/image5.jpg
[image6]: images/kubecon-2026-dsx-ai-factory-day-report/image6.jpg
[image7]: images/kubecon-2026-dsx-ai-factory-day-report/image7.jpg
[image8]: images/kubecon-2026-dsx-ai-factory-day-report/image8.jpg
[image9]: images/kubecon-2026-dsx-ai-factory-day-report/image9.jpg
[image10]: images/kubecon-2026-dsx-ai-factory-day-report/image10.png
[image11]: images/kubecon-2026-dsx-ai-factory-day-report/image11.jpg
[image12]: images/kubecon-2026-dsx-ai-factory-day-report/image12.png
[image13]: images/kubecon-2026-dsx-ai-factory-day-report/image13.png
