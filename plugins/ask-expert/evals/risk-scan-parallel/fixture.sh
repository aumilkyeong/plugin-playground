#!/usr/bin/env bash
# 성능, 접근성, 보안, 신뢰성 위험이 섞여 심어진 결제 화면 설계 문서를 만든다.
set -euo pipefail

mkdir -p docs/design
cat > docs/design/checkout-redesign.md <<'MD'
# 결제 화면 개편 설계

## 목표

모바일 결제 전환율을 올린다. 결제 화면을 한 페이지로 줄이고, 외부 결제 위젯을 붙인다.

## 화면 구성

- 맨 위에 프로모션 히어로 이미지(PNG, 약 3MB)를 둔다. 디자인 시안 비율에 맞추기 위해 크기는 CSS로 나중에 조정한다.
- 주문 요약, 배송지, 결제 수단, 결제 버튼 순서로 둔다.
- 결제 버튼은 시안의 그라데이션과 애니메이션을 그대로 살리기 위해 `<div onClick={pay}>`로 만든다.

## 데이터와 인증

- 로그인 후 받은 액세스 토큰을 `localStorage`에 저장하고, 결제 API를 부를 때 `Authorization` 헤더에 넣는다.
- 주문 완료 후 서버가 내려주는 완료 안내 문구(HTML)를 `dangerouslySetInnerHTML`로 그대로 그린다. 마케팅 팀이 문구를 바꿀 수 있게 하기 위해서다.

## 외부 결제 위젯

- 결제사가 준 스크립트를 `<head>`에 `<script src="https://pay.example.com/widget.js">`로 넣는다. 위젯이 준비되기 전에 사용자가 누르지 않도록 스크립트가 다 받아질 때까지 화면을 그리지 않는다.

## 오류 처리

- 결제 API가 실패하면 예외를 그대로 던진다. 페이지 전체를 다시 불러오면 되므로 따로 오류 화면은 두지 않는다.
MD
