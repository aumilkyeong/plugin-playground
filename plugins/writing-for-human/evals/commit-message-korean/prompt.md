---
name: commit-message-korean
description: 커밋 메시지도 사람이 읽을 글로 보고 skill이 발동하며, 무엇을 고쳤는지 드러나는 한국어 제목 줄을 쓴다
tags: [write, light]
max_turns: 6
allowed_tools: [Read, Skill]
---

이 변경을 커밋하려고 해. 커밋 메시지를 써줘.

```diff
--- a/stats.py
+++ b/stats.py
@@ -1,2 +1,4 @@
 def average(values):
+    if not values:
+        return 0
     return sum(values) / len(values)
```
