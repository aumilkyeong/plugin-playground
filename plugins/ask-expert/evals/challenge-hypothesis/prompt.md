---
name: challenge-hypothesis
description: 사용자가 자기 가설을 검토해 달라고 하면 아키텍트를 반박 모드로 불러 반박 근거부터 찾고, 가설을 그대로 맞다고 돌려주지 않는다
tags: [architect, rebuttal]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Agent, Skill]
---

상품 목록에서 상세로 갔다가 돌아오면 카테고리와 정렬이 풀려. 필터 상태를 zustand 전역 store로 옮기면 해결될 것 같은데, 검토해줘.
