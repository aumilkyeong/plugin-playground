---
name: risk-scan-parallel
description: 여러 관점에 걸친 무거운 설계(결제) 문서의 위험을 찾아 달라고 하면 아키텍트를 렌즈별로 나눠 2~3번 부르고, 위험을 필수 수정과 확인 필요로 나눠 번호를 붙여 돌려준다
tags: [architect, risk-scan, heavy]
max_turns: 40
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Agent, Skill]
---

docs/design/checkout-redesign.md 설계에서 내가 놓친 위험이 있는지 검토해줘.
