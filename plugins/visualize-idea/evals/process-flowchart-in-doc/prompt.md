---
name: process-flowchart-in-doc
description: 갈래와 되돌아가는 길이 있는 과정을 문서에 도식화해 달라고 하면 skill이 발동해, 판단 갈래가 보이는 Mermaid 흐름도를 넣고 화살표에 뜻을 밝히며 메시지를 말하는 제목이나 캡션을 단다
tags: [visualize, medium]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Write, Edit, Agent, Skill]
---

우리 팀 신규 입사자 온보딩 과정을 도식화해서 `docs/onboarding.md`에 넣어줘.

1. 입사자가 첫날 계정을 신청한다.
2. IT팀이 신청을 검토한다. 정보가 빠졌으면 반려하고, 입사자가 보완해서 다시 신청한다.
3. 승인되면 노트북을 받는다.
4. 노트북을 받은 날 멘토가 배정되고, 멘토와 첫 과제를 정한다.
5. 첫 과제를 마치면 온보딩이 끝난다.
