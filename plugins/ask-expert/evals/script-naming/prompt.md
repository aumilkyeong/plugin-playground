---
name: script-naming
description: 몇 줄 고치면 되돌릴 수 있는 가벼운 결정에는 아키텍트를 부르지 않고, 권장안과 포기하는 것을 짧게 바로 답한다
tags: [architect, light]
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Agent, Skill]
---

package.json의 dev:mock, preview:mock 스크립트를 mock:dev, mock:preview로 바꾸는 게 혼란도 적고 자동완성에도 유리할 것 같아. 트레이드오프를 검토해줘.
