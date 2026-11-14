# A Week at KubeCon with DSX AI Factory: A Contributor Workshop and a Maintainer Social

Most open source projects have the same quiet problem. People can see the issues, the code, and the contributing guide, and still don't contribute, because the distance between reading a repository and getting a first pull request merged is longer than it looks. You need a working environment, an understanding of the CI, and someone to ask when it breaks. Each of those takes minutes with a maintainer in the next chair and days alone, which is the idea behind the DSX OS Contributor Workshop: put the people who use a project in the same room as the people who build it, and spend the time on real issues instead of slides.

It starts with an explicit conversation with partners and customers about contributing, because "contributions welcome" in a README is easy to ignore and a maintainer saying "this issue is yours" across a table is not. That conversation is how we grow participation from outside NVIDIA, and in Salt Lake City it meant the cloud native community already in town for KubeCon. The part that matters most comes afterward, keeping the contributions going, which we measure by who is still active 90 days later and not by pull requests opened on the day.

The [first workshop](https://www.linkedin.com/pulse/building-dsx-os-open-what-its-customers-partners-did-one-arun-gupta-iehsc/), an invite-only day at NVIDIA headquarters in September, showed what happens when the distance between a user and a maintainer disappears, and the second took the format to Salt Lake City on Monday, November 9, the day before KubeCon + CloudNativeCon North America opened. Warren Barkley opened with an introduction to DSX, every product manager gave a lightning introduction, and then people split into contribution sprints across these streams:

- **Building and running clusters:** NVIDIA Kubernetes Engine, Kubernetes Recipes, GPU Operator
- **Keeping them ready, running, and healthy:** AI Cluster Runtime, NVSentinel, Nodewright, Topograph
- **NVIDIA Run:ai**

In each, you claimed an issue, opened a draft pull request, and got a live review from a maintainer.

> **[PHOTO: the workshop room with project tables. Caption: "Each project at its own table."]**

## What happened at the tables

At the Kubernetes Recipes table, contributors opened four pull requests that are now all merged, two CLI fixes and two features, one of which lets you filter the recipe catalog by platform and output type. Two Workload Map contributors opened pull requests before the afternoon ended, one adding Argo Rollouts to the catalog and one fixing how Milvus etcd and MinIO pods are identified. On the Infra Controller table, a Crusoe engineer filed a detailed issue about public IPs, NAT, and load balancers for tenant networks, a question that comes from running bare metal for customers. At Dynamo, one contributor added a router queue wait metric that is now in review. At AI Cluster Runtime, the afternoon with Upbound produced a new issue and two closed through pull requests. [Confirm OK to name Upbound and Crusoe.] Asked for one word, teams said exciting, fruitful, foundational, and mind-expanding, and one Dynamo contributor offered "lots of dependencies, models are big, Wifi is slow."

> **[PHOTO: a maintainer and a contributor at a table. Caption: "Live review."]**

81 people attended, and the contributor sessions drew 40 organizations. In the 24 hours around the workshop, 57 contributors across 12 repositories opened 36 pull requests and 28 issues and left 64 comments, putting activity 59% above a typical day. Of those contributors, 19 were first-timers, against a usual 5. Four pull requests merged that day and 32 more were in review, and 96% of survey respondents said the workshop was a good use of their time.

## The first community meetings

The afternoon ended with the first in-person community meetings, where four project communities kicked off their regular meetings: GPU Operator, NVIDIA Run:ai, DSX Kubernetes cluster management, and DSX Kubernetes cluster health and configuration. [Roughly how many people joined, and what they agreed to do next.]

## The Maintainer Social

A workshop brings newcomers to our projects, but much of what we build depends on people already deep in the cloud native ecosystem, the maintainers of Kubernetes and the CNCF projects around it. A booth is no place to build those relationships, so we designed the evening as the opposite: a small, invite-only social, casual and relationship-first, with no keynotes and no hard pitches. The aim was for maintainers to meet the NVIDIA people working on neighboring problems and hear where DSX OS projects could use help. It was also our way of thanking the people who maintain the community.

Forty-seven external maintainers and community leaders came, from 18 organizations, and spent the evening with NVIDIA product, engineering, and leadership, including Warren Barkley and Bob Wise. The room included members of the Kubernetes Steering Committee, a member of the CNCF Technical Oversight Committee, the SIG-Node co-chair, and maintainers of KubeVirt and OpenShell.

> **[PHOTO: the social, from the "Maintainer Social Nov 9" folder. Caption: "The first DSX AI Factory Maintainer Social."]**

One NVIDIA engineer wrote afterward that the invite list was spot on, with long-term maintainers who are interested in adopting NVIDIA software and also able to help NVIDIA engineers get more involved in key upstream projects. [Confirm the quote and whether to name him.] [One or two moments from the evening, in your own words.] We plan to make it a standing event at every KubeCon. As in September, what stood out was less the code than the people.

## Thank you

Thank you to the 40 organizations that spent the day with us [optional: names that agreed to be named], the maintainers who joined the social, and the NVIDIA product managers and engineers who gave up their day. My co-leads Shally Garg and Pavitar Thiara shared the planning with me.

## What comes next

The next workshop is a holiday edition in December focused on NVIDIA Run:ai, with partner workshops planned for GTC in San Jose in March. [Confirm the December date and what can be said publicly about GTC.] To take part in the meantime, explore [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory), request a Slack invite at [inviter.co/dsx-ai-factory](https://inviter.co/dsx-ai-factory), or find a project community in the [communities](../communities/README.md) directory. If you have ever worked around a bug instead of reporting it, pick a project and tell us what is missing.

---

© 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
