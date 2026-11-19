#!/usr/bin/env bash
# 모의 API 실행 스크립트 이름이 dev:mock, preview:mock인 package.json을 만든다.
set -euo pipefail

cat > package.json <<'JSON'
{
  "name": "shop-web",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "dev:mock": "NEXT_PUBLIC_API_MOCKING=enabled next dev",
    "build": "next build",
    "preview": "next build && next start",
    "preview:mock": "NEXT_PUBLIC_API_MOCKING=enabled next build && next start",
    "test": "vitest"
  }
}
JSON
