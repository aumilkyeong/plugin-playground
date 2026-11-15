---
type: regex
pattern: '이 문서(에서|는)|살펴보(겠|자|도록)|알아보(겠|자|도록)|정리하면|결론적으로|도움이 되(었|길|기를)'
match: not_contains
target:
  source: file
  path: README.md
---
