---
type: regex
pattern: '에 있어서|되어지|되어진|하는 것이 가능|에 의해'
match: not_contains
target:
  source: file
  path: README.md
---
