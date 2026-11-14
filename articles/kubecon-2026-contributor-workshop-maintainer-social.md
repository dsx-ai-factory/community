# A Week at KubeCon with DSX AI Factory: A Contributor Workshop and a Maintainer Social

In the 24 hours around the DSX OS Contributor Workshop in Salt Lake City, 57 contributors across 12 repositories opened 36 pull requests and 28 issues and left 64 comments. Compared with a typical day over the previous 30 days:

- **Overall activity was up 59%.**
- **Pull requests were up 79%**, 36 against a typical 20.
- **First-time contributors were up nearly 4x**, 19 against a typical 5.

Four pull requests merged the same day, and 32 more were in review with maintainers.

Most open source projects have the same quiet problem. People can see the issues, the code, and the contributing guide, and still don't contribute, because the distance between reading a repository and getting a first pull request merged is longer than it looks. You need a working environment, an understanding of the CI, and someone to ask when it breaks. Each of those takes minutes with a maintainer in the next chair and days alone, which is the idea behind the DSX OS Contributor Workshop: put the people who use a project in the same room as the people who build it, and spend the time on real issues instead of slides.

It rests on three ideas:

- **An explicit conversation with partners and customers about contributing.** "Contributions welcome" in a README is easy to ignore, and a maintainer saying "this issue is yours" across a table is not.
- **More participation from outside NVIDIA.** In Salt Lake City, that meant the cloud native community already in town for KubeCon.
- **Keeping the contributions going.** We measure it by who is still active 90 days later, not by pull requests opened on the day.

The [first workshop](https://www.linkedin.com/pulse/building-dsx-os-open-what-its-customers-partners-did-one-arun-gupta-iehsc/), an invite-only day at NVIDIA headquarters in September, showed what happens when the distance between a user and a maintainer disappears, and the second took the format to Salt Lake City on Monday, November 9, the day before KubeCon + CloudNativeCon North America opened. Warren Barkley opened with an introduction to DSX and the kickoff of the in-person community meetings, every product manager gave a lightning introduction, and then people split into contribution sprints across four streams:

- **Building and running clusters:** NVIDIA Kubernetes Engine, Kubernetes Recipes
- **Keeping them ready, running, and healthy:** AI Cluster Runtime, NVSentinel, Nodewright, Topograph
- **GPU Operator and Operands**
- **NVIDIA Run:ai**

Contributing meant more than code: you could discuss the roadmap, file an issue, give a maintainer feedback in person, or open a draft pull request and get a live review, and all of it counted.

> **[PHOTO: workshop room. Caption: "Each project at its own table."]**

## What happened at the tables

Some teams spent contribution time on roadmap discussions and requirements, four project communities used the day to kick off regular community meetings, and others shipped code. See the [upcoming community meetings](https://github.com/dsx-ai-factory/community/blob/main/articles/dsx-ai-factory-community-meetings.md) to join one.

At the Kubernetes Recipes table, contributors opened four pull requests that are now all merged, two CLI fixes and two features, one filtering the recipe catalog by platform and output type. Two Workload Map contributors opened pull requests, one adding Argo Rollouts to the catalog and one fixing how Milvus etcd and MinIO pods are identified. On the Infra Controller table, an engineer from a GPU cloud provider filed a detailed issue about public IPs, NAT, and load balancers for tenant networks, a question that comes from running bare metal for customers. At Dynamo, one contributor added a router queue wait metric that is now in review. At AI Cluster Runtime, the afternoon with a cloud native platform company produced a new issue and two closed through pull requests.

Asked for one word to describe the day, the teams said enlightening, exciting, cool, adaptable, mind-expanding, fruitful, exploratory, human, and foundational.

> **[PHOTO: maintainer and contributor. Caption: "Live review."]**

The contributor sessions drew 40 organizations, and in the survey afterward, 96% of respondents said the workshop was a good use of their time, and 44% said very much.

## The Maintainer Social

A workshop brings newcomers to our projects, but much of what we build depends on people already deep in the cloud native ecosystem, the maintainers of Kubernetes and the CNCF projects around it. So we invited a small group to a casual evening, with no keynotes and no pitches. The invitation was simple: we wanted to thank them for their work in the cloud native community and celebrate it, introduce them to the NVIDIA maintainers who do the work on our projects, and hear where their own projects overlap with ours and how we show up in the community.

Around 50 maintainers of cloud native projects and community leaders came from 18 organizations and spent the evening with NVIDIA product, engineering, and leadership, including Warren Barkley and Bob Wise. The room included members of the Kubernetes Steering Committee, a CNCF Technical Oversight Committee member, the SIG-Node co-chair, and maintainers of [OpenShell](https://blogs.nvidia.com/blog/open-source-openshell-infrastructure/), the project NVIDIA donated to the CNCF that week.

> **[PHOTO: the social. Caption: "The first DSX AI Factory Maintainer Social."]**

One NVIDIA engineer wrote afterward that the invite list was spot on, with long-term maintainers who want to adopt NVIDIA software and can help us get more involved upstream. [Confirm quote and attribution.] I enjoyed bringing the external maintainers and NVIDIA maintainers together. It has always been people over code, because meaningful relationships are what make you more effective when you collaborate. We plan to make it a standing event at every KubeCon.

## Thank you

Thank you to the 40 organizations that spent the day with us [optional: names], the maintainers who joined the social, and the NVIDIA product managers and engineers who gave up their day. My co-leads Shally Garg and Pavitar Thiara shared the planning with me.

## Get involved

To take part, explore [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory), request a Slack invite at [inviter.co/dsx-ai-factory](https://inviter.co/dsx-ai-factory), or find a project community in the [communities](../communities/README.md) directory. If you have ever worked around a bug instead of reporting it, pick a project and tell us what is missing.

---

© 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
