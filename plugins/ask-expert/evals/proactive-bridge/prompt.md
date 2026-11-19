---
name: proactive-bridge
description: 묻지 않았어도 구현 요청 안에 앱과 웹이 따를 계약처럼 되돌리기 어려운 결정이 있으면 Claude가 먼저 아키텍트에게 자문하고, 사용자가 정하기 전까지 그 결정에 기대는 구현을 멈춘다
tags: [architect, proactive, heavy]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Write, Edit, Agent, Skill]
---

이 웹은 우리 Flutter 앱의 웹뷰 안에서도 열려. 앱에서 로그인 토큰을 받아오는 기능이랑 공유하기 기능을 쓸 수 있게 앱-웹 브릿지를 추가해줘.
