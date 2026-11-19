---
name: state-location
description: 상태를 어디에 둘지 묻는 보통 무게의 구조 질문에 skill이 발동해 아키텍트에게 자문하고, 넘긴 브리프에 Claude가 떠올린 안을 끼워 넣지 않으며, 권장안과 포기하는 것이 달린 번호 결정으로 돌려준다
tags: [architect, decision, medium]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Agent, Skill]
---

상품 목록에서 카테고리랑 정렬을 고르고 상세로 들어갔다가 '목록으로'를 누르면 고른 게 다 풀려. 이 필터 상태를 어디에 두는 게 좋을지 검토해줘.
