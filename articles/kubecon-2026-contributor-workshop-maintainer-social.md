# A Week at KubeCon with DSX AI Factory: A Contributor Workshop and a Maintainer Social

On Monday, November 9, we ran the second DSX OS Contributor Workshop in Salt Lake City, the day before KubeCon + CloudNativeCon North America 2026 opened. In the 24 hours around the workshop, 57 contributors across 12 repositories opened 36 pull requests and 28 issues and left 64 comments. Compared with a typical day, overall activity was up 59%, pull requests were up 79%, and the number that stayed with me is that 19 of the contributors were first-timers, against a usual 5. Four pull requests merged the same day, and 32 more were in review with maintainers by the time we counted. That evening, we hosted the first DSX AI Factory Maintainer Social, a private gathering of 47 external maintainers and community leaders.

This is the follow-up to [Building DSX AI Factory Projects Together at KubeCon North America 2026](kubecon-2026-dsx-os-contributor-workshop.md). The first workshop, in September at NVIDIA headquarters, was about getting customers and partners in a room with the maintainers of the DSX OS projects. This one went to where the cloud native community already was. If you build AI infrastructure on Kubernetes, you were probably in Salt Lake City that week, and the goal this time was to grow participation from that community, with an eye on who is still contributing 90 days from now and not only on who opened a pull request on the day.

## What the day looked like

The day was a co-located event with two halves, a morning deep dive on AI inference and an afternoon contributor workshop, and people could join either or both. About 285 people had registered and 81 attended: 50 stayed all day, 7 came for the afternoon contributor session only, and 24 came for the morning only. The people in the contributor sessions came from 40 organizations, a mix of GPU cloud and infrastructure companies, large technology companies, enterprises, cloud native startups, and universities.

The afternoon followed what we described beforehand: a short orientation to the DSX OS projects, a long block of contribution sprints and roadmap roundtables, a Show and Tell, and then the first in-person community meetings. Attendees were encouraged to bring their AI coding assistants, and most of the time went into forking a repository, setting up an environment, opening a draft pull request early so a maintainer could follow along, and asking questions at the table. Each project had its own table with its product manager and engineers sitting at it, which is the part of the format I would not change.

The Show and Tell is where the stories came out. On the NVIDIA Kubernetes Engine and Kubernetes Recipes table, three contributors went from roadmap discussions to implementation and left with two merged fixes and two open pull requests, while also surfacing requirements nobody on the team had written down. At Dynamo, six contributors started with environment setup and ended with code and documentation improvements moving into review. Snapshot had five contributors exploring the architecture, two pull requests, and a few issues that need more design work than an afternoon allows. NVIDIA AI Cluster Runtime resolved two issues through pull requests, and its team also learned where test access and validation make it hard for outsiders to participate, which is the kind of finding you only get by watching someone try. The NVIDIA Infra Controller table drew seven to ten contributors into use-case and architecture discussions and filed two new issues, and the Workload Map team had three contributors open two pull requests, with one of them taking ownership of an issue. Several teams, including GPU Operator, Health and Resilience, Nodewright, KAI Scheduler, and NVIDIA Run:ai, spent their time on requirements, integration questions, and feedback, and nobody I spoke to thought of that as a lesser outcome.

## The first community meetings

The afternoon ended with the first in-person community meetings, where several project communities held the kickoff of their regular meetings. [What happened in the meetings, which communities met, roughly how many people joined, and what they agreed to do next.]

## The Maintainer Social

The workshop brings contributors to the DSX AI Factory projects. The Maintainer Social went the other direction, and it was a first for us. That evening, to thank the cloud native community and celebrate its maintainers, we brought together a curated group for a private social, with 47 external maintainers and community leaders from 18 organizations spending the evening with NVIDIA product, engineering, and leadership teams, including Warren Barkley and Bob Wise. The room included members of the Kubernetes Steering Committee, a member of the CNCF Technical Oversight Committee, the SIG-Node co-chair, and maintainers of KubeVirt and OpenShell. [Optional: name the organizations that agreed to be named.]

There was no agenda, which was deliberate, and the energy in the room produced a lot of useful conversations. One NVIDIA engineer who was there wrote afterward that the invite list was spot on, with long-term maintainers of Kubernetes and other CNCF projects who are interested in adopting NVIDIA software and also able to help NVIDIA engineers get more involved in key upstream projects. [Confirm the quote and whether to name him.] [One or two moments from the evening, in your own words.] We plan to make it a standing event at every KubeCon.

## What it adds up to

A contributor workshop and a maintainer social look like two different events, and I think of them as two halves of the same week. The workshop gave people outside NVIDIA a reason to open their first pull request in the DSX AI Factory projects, and the social was our way of saying thank you to the maintainers whose projects those contributions depend on. As in September, what stood out was less the code than the people, and the code followed quickly once they had met.

## Thank you

This only worked because the contributors showed up ready to build. Thank you to the 40 organizations that spent the day with us [optional: list the ones that agreed to be named, and confirm before naming enterprises], and to the maintainers who joined the social. Thank you as well to the NVIDIA product managers and engineers who gave up their day at the tables, and to the teams behind NVIDIA Run:ai, Workload Map, KAI Scheduler, Snapshot, Dynamo, Health and Resilience, AI Cluster Runtime, Nodewright, NVIDIA Kubernetes Engine and Kubernetes Recipes, GPU Operator, and Infra Controller for showing up. My co-leads Shally Garg and Pavitar Thiara shared the planning with me, along with the events team, and the results came together because of them.

## What comes next

The next workshop is a holiday edition in December focused on NVIDIA Run:ai, and we are planning partner workshops at GTC in San Jose in March. [Confirm the December date and what can be said publicly about GTC.] Between workshops, there are three places to take part, and you are welcome in each of them:

- **GitHub:** [github.com/dsx-ai-factory](https://github.com/dsx-ai-factory) is where the DSX OS open source projects live in one organization, so anyone who wants to contribute has one place to start.
- **Slack:** request an invite at [inviter.co/dsx-ai-factory](https://inviter.co/dsx-ai-factory) for questions, ideas, and conversations with the maintainers.
- **Community meetings:** the [communities](../communities/README.md) directory lists each project community and how its meetings work.

If you maintain a project that touches AI infrastructure, or you run an AI factory and have ever worked around a bug instead of reporting it, pick a project in the GitHub organization, look at the open issues, and tell us what is missing.

---

© 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
