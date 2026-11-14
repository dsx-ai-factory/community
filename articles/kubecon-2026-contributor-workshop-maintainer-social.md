# A Week at KubeCon with DSX AI Factory: A Contributor Workshop and a Maintainer Social

Most open source projects have the same quiet problem. People can see the issues, the code, and the contributing guide, and still don't contribute, because the distance between reading a repository and getting a first pull request merged is longer than it looks. You need a working environment, you need to know how the CI behaves, and you need to know who to ask when the build fails halfway through the afternoon. Each of those takes minutes with a maintainer in the next chair and days alone, which is the idea behind the DSX OS Contributor Workshop: put the people who use a project in the same room as the people who build it, and spend the time on real issues instead of slides.

We run it with four goals: raise open source hygiene across the participating repositories beforehand so nobody gets blocked by a missing setup guide, have an explicit conversation with partners and customers about contributing, grow participation from outside NVIDIA, and keep contributions going afterward. We measure that last one by who is still active 90 days later, not by pull requests opened on the day. Progress is tracked on a five-rung ladder, Engage, Enable, Build, Land, and Grow, so that later requirements like hardware access don't slow down someone still on the second rung.

The second workshop took place on Monday, November 9, in downtown Salt Lake City, the day before KubeCon + CloudNativeCon North America opened. After a short orientation, people chose a path: a supported contribution sprint, where you claim an issue, open a draft pull request, and get a live review from a maintainer, or a roundtable with product managers and maintainers for people who brought their organization's requirements. Many attendees brought their AI coding assistants.

> **[PHOTO: the workshop room with project tables. Caption: "Each project at its own table."]**

## What happened at the tables

On the NVIDIA Kubernetes Engine and Kubernetes Recipes table, three contributors went from roadmap discussions to implementation and left with two merged fixes and two open pull requests. At Dynamo, six contributors started with environment setup and ended with code and documentation changes in review. NVIDIA AI Cluster Runtime resolved two issues through pull requests and learned where test access makes it hard for outsiders to take part, which you only discover by watching someone try. The NVIDIA Infra Controller table drew seven to ten contributors into architecture discussions and filed two new issues, and Workload Map had three contributors open two pull requests, with one taking ownership of an issue. Other teams spent the afternoon on requirements and feedback, which on the ladder is exactly what the first rung looks like.

> **[PHOTO: a maintainer and a contributor reviewing a pull request. Caption: "Live review at the table."]**

About 285 people registered and 81 attended, from 40 organizations in the contributor sessions. In the 24 hours around the workshop, 57 contributors across 12 repositories opened 36 pull requests and 28 issues and left 64 comments, putting activity 59% above a typical day. The figure I like best is that 19 of the contributors were first-timers, against a usual 5. Four pull requests merged that day and 32 more were in review. One engineering lead said afterward that the workshop produced merged pull requests, new contributors, and a better contributor setup in a single week. [Confirm the quote is okay to use.]

## The first community meetings

The afternoon ended with the first in-person community meetings, where several project communities kicked off their regular meetings. [Which communities met, roughly how many people joined, and what they agreed to do next.]

## The Maintainer Social

A workshop brings newcomers to our projects, but much of what we build depends on people already deep in the cloud native ecosystem, the maintainers of Kubernetes and the CNCF projects around it. A booth is not where those relationships get built, so we designed the evening as the opposite: a small, invite-only social, casual and relationship-first, with no keynotes and no hard pitches. The aim was for maintainers to meet the NVIDIA people working on neighboring problems, hear where DSX OS projects could use help, and leave with a way to stay in touch. It was also our way of thanking the community and celebrating the people who maintain it.

Forty-seven external maintainers and community leaders came, from 18 organizations, and spent the evening with NVIDIA product, engineering, and leadership, including Warren Barkley and Bob Wise. The room included members of the Kubernetes Steering Committee, a member of the CNCF Technical Oversight Committee, the SIG-Node co-chair, and maintainers of KubeVirt and OpenShell.

> **[PHOTO: the social, from the "Maintainer Social Nov 9" folder. Caption: "The first DSX AI Factory Maintainer Social."]**

One NVIDIA engineer wrote afterward that the invite list was spot on, with long-term maintainers who are interested in adopting NVIDIA software and also able to help NVIDIA engineers get more involved in key upstream projects. [Confirm the quote and whether to name him.] [One or two moments from the evening, in your own words.] We plan to make it a standing event at every KubeCon. As in September, what stood out was less the code than the people.

## Thank you

Thank you to the 40 organizations that spent the day with us [optional: names that agreed to be named], to the maintainers who joined the social, and to the NVIDIA product managers and engineers who gave up their day at the tables. My co-leads Shally Garg and Pavitar Thiara shared the planning with me, along with the events team.

## What comes next

The next workshop is a holiday edition in December focused on NVIDIA Run:ai, with partner workshops planned for GTC in San Jose in March. [Confirm the December date and what can be said publicly about GTC.] To take part in the meantime, explore [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory), request a Slack invite at [inviter.co/dsx-ai-factory](https://inviter.co/dsx-ai-factory), or find a project community in the [communities](../communities/README.md) directory. If you have ever worked around a bug instead of reporting it, pick a project, look at the open issues, and tell us what is missing. This is the follow-up to [Building DSX AI Factory Projects Together at KubeCon North America 2026](kubecon-2026-dsx-os-contributor-workshop.md).

---

© 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
