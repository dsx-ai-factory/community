# A Week at KubeCon with DSX AI Factory: A Contributor Workshop and a Maintainer Social

Most open source projects have the same quiet problem. The people who would like to contribute can see the issues, the code, and the contributing guide, and still don't, because the distance between reading a repository and getting a first pull request merged is longer than it looks. You need a working development environment, you need to know how the CI behaves, you need to know which issue is safe to pick up, and you need to know who to ask when the build fails halfway through the afternoon. Each of those takes a few minutes with a maintainer in the next chair and a few days alone, which is the idea behind the DSX OS Contributor Workshop: put the people who use a project in the same room as the people who build it, and spend the time on real issues instead of slides.

We run it with four goals. The first is to raise the baseline of open source hygiene across every participating repository before the event, so that no attendee gets blocked by a missing setup guide or an unclear contribution process. The second is to have an explicit conversation with partners and customers about contributing to our repositories, in place of the implied "contributions welcome." The third is to grow participation from outside NVIDIA, and in Salt Lake City that meant the cloud native community that was already in town for KubeCon. The fourth, and the one I care about most, is to keep the contributions going after the day, which we measure by who is still active 90 days later and not by how many pull requests were opened that afternoon. We track progress on a ladder with five rungs, Engage, Enable, Build, Land, and Grow, because early progress depends on shared purpose and good documentation while the later rungs need hardware access and full validation, and we don't want the later requirements to slow down someone who has only reached the second rung.

The second workshop took place on Monday, November 9, at a hotel in downtown Salt Lake City, the day before KubeCon + CloudNativeCon North America opened. It was one half of a co-located day, with a morning deep dive on AI inference and the contributor workshop in the afternoon. After a short orientation, people chose a path. One path was a supported contribution sprint, where you claim an issue, open a draft pull request, run CI, and get a live review from a maintainer. The other was a roundtable with product managers and maintainers, for people who came with their organization's requirements and integration ideas and wanted to put them in front of the people who decide what gets built. Attendees were encouraged to bring their AI coding assistants, and a lot of them did.

> **[PHOTO: the workshop room with the project tables, wide shot. Suggested caption: "The afternoon contributor workshop in Salt Lake City, with each project at its own table."]**

## What happened at the tables

Each project had its own table with its product manager and engineers sitting at it, and the Show and Tell at the end is where the stories came out. On the NVIDIA Kubernetes Engine and Kubernetes Recipes table, three contributors went from roadmap discussions to implementation and left with two merged fixes and two open pull requests, while also surfacing requirements nobody on the team had written down. At Dynamo, six contributors started with environment setup and ended with code and documentation improvements moving into review. Snapshot had five contributors exploring the architecture, two pull requests, and a few issues that need more design work than an afternoon allows. NVIDIA AI Cluster Runtime resolved two issues through pull requests, and its team also learned where test access and validation make it hard for outsiders to take part, which is the kind of finding you only get by watching someone try. The NVIDIA Infra Controller table drew seven to ten contributors into use-case and architecture discussions and filed two new issues, and the Workload Map team had three contributors open two pull requests, with one of them taking ownership of an issue. Several teams, including GPU Operator, Health and Resilience, Nodewright, KAI Scheduler, and NVIDIA Run:ai, spent their time on requirements, integration questions, and feedback, and nobody I spoke to thought of that as a lesser outcome, since on the ladder it is exactly what the first rung looks like.

> **[PHOTO: a maintainer and a contributor working through a pull request at a table, or the Show and Tell. Suggested caption: "A contributor and a maintainer reviewing a pull request together."]**

The numbers say the same thing in a different voice. About 285 people had registered and 81 attended, with 50 staying all day, 7 coming for the afternoon contributor session only, and 24 coming for the morning only. The people in the contributor sessions came from 40 organizations, a mix of GPU cloud and infrastructure companies, large technology companies, enterprises, cloud native startups, and universities. In the 24 hours around the workshop, 57 contributors across 12 repositories opened 36 pull requests and 28 issues and left 64 comments, which put overall activity 59% above a typical day. The figure I like best is that 19 of the contributors were first-timers, against a usual 5. Four pull requests merged the same day, and 32 more were in review with maintainers by the time we counted. One of our engineering leads summed it up afterward by saying that the workshop produced merged pull requests, new contributors, and a better contributor setup in a single week, and that it is an inexpensive way to grow the community. [Confirm the quote is okay to use.]

## The first community meetings

The afternoon ended with the first in-person community meetings, where several project communities held the kickoff of their regular meetings. [What happened in the meetings, which communities met, roughly how many people joined, and what they agreed to do next.]

## The Maintainer Social

A workshop is a good way to bring newcomers to our projects, but a lot of what we build depends on people who are already deep inside the cloud native ecosystem, the maintainers of Kubernetes and the CNCF projects around it. A booth at a conference is not where that kind of relationship gets built, so we designed the evening around the opposite of a booth: a small, invite-only social that was casual and relationship-first, with no keynotes and no hard pitches. The point was for maintainers to meet the NVIDIA people working on neighboring problems, hear where the DSX OS projects could use help, and leave with a way to stay in touch. It was also our way of thanking the cloud native community and celebrating the people who maintain it.

Forty-seven external maintainers and community leaders came, from 18 organizations, and spent the evening with NVIDIA product, engineering, and leadership teams, including Warren Barkley and Bob Wise. The room included members of the Kubernetes Steering Committee, a member of the CNCF Technical Oversight Committee, the SIG-Node co-chair, and maintainers of KubeVirt and OpenShell. [Optional: name the organizations that agreed to be named.]

> **[PHOTO: the social, from the "Maintainer Social Nov 9" folder. Suggested caption: "The first DSX AI Factory Maintainer Social, Salt Lake City."]**

The energy in the room was electric, and the conversations were useful ones. One NVIDIA engineer who was there wrote afterward that the invite list was spot on, with long-term maintainers of Kubernetes and other CNCF projects who are interested in adopting NVIDIA software and also able to help NVIDIA engineers get more involved in key upstream projects. [Confirm the quote and whether to name him.] [One or two moments from the evening, in your own words: who was talking to whom, what surprised you.] We plan to make it a standing event at every KubeCon.

> **[PHOTO: a second shot from the social, ideally of a conversation. Suggested caption: "Maintainers and NVIDIA engineers, no slides."]**

## What it adds up to

A contributor workshop and a maintainer social look like two different events, and I think of them as two halves of the same week. The workshop gave people outside NVIDIA a reason to open their first pull request in the DSX AI Factory projects, and the social was our way of thanking the maintainers whose projects those contributions depend on. As in September, what stood out was less the code than the people, and the code followed quickly once they had met.

## Thank you

This only worked because the contributors showed up ready to build. Thank you to the 40 organizations that spent the day with us [optional: list the ones that agreed to be named, and confirm before naming enterprises], and to the maintainers who joined the social. Thank you as well to the NVIDIA product managers and engineers who gave up their day at the tables, and to the teams behind NVIDIA Run:ai, Workload Map, KAI Scheduler, Snapshot, Dynamo, Health and Resilience, AI Cluster Runtime, Nodewright, NVIDIA Kubernetes Engine and Kubernetes Recipes, GPU Operator, and Infra Controller for showing up. My co-leads Shally Garg and Pavitar Thiara shared the planning with me, along with the events team, and none of this would have come together without them.

## What comes next

The next workshop is a holiday edition in December focused on NVIDIA Run:ai, and we are planning partner workshops at GTC in San Jose in March. [Confirm the December date and what can be said publicly about GTC.] Between workshops, there are three places to take part, and you are welcome in each of them:

- **GitHub:** [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory) is where the DSX OS open source projects live in one organization, so anyone who wants to contribute has one place to start.
- **Slack:** request an invite at [inviter.co/dsx-ai-factory](https://inviter.co/dsx-ai-factory) for questions, ideas, and conversations with the maintainers.
- **Community meetings:** the [communities](../communities/README.md) directory lists each project community and how its meetings work.

If you maintain a project that touches AI infrastructure, or you run an AI factory and have ever worked around a bug instead of reporting it, pick a project in the GitHub organization, look at the open issues, and tell us what is missing.

This is the follow-up to [Building DSX AI Factory Projects Together at KubeCon North America 2026](kubecon-2026-dsx-os-contributor-workshop.md), which describes the workshop's format and schedule ahead of the event.

---

© 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
