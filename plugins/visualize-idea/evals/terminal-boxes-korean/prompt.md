---
name: terminal-boxes-korean
description: 채팅에서 상자 도식을 부탁하면 터미널 텍스트 도식으로 그리고, 한글 폭 검사(textwidth.py)를 돌린 뒤 내놓는다
tags: [visualize, light]
max_turns: 15
timeout_seconds: 400
allowed_tools: [Read, Write, Bash, Skill]
---

요청이 어떻게 흐르는지 터미널에서 바로 볼 수 있게 상자 도식으로 그려줘. 사용자가 웹 서버에 요청하면 웹 서버가 먼저 캐시를 확인하고, 캐시에 없으면 데이터베이스에서 읽어 온다.
