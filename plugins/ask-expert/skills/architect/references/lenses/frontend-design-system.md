# 디자인 시스템과 반응형

디자인 값(토큰)의 계층, 공통 컴포넌트 API의 모양, 여러 화면 환경(PC, 모바일 웹, 앱 웹뷰) 대응 방식을 정한다.

## 코드에서 먼저 확인할 것
- 컴포넌트 안에 색·간격·크기 원시값이 직접 쓰였는지, 의미 있는 이름의 토큰을 거치는지.
- 공통 컴포넌트의 props 수와 분기 수. 도메인 이름이 든 분기(`if (isXxxPage)`)가 있는지.
- 포커스·키보드·팝업 겹침을 직접 구현했는지, 검증된 headless 부품 위에 스타일만 입혔는지.
- 반응형 기준: 화면 폭만 보는지, 포인터 정밀도·hover 가능 여부·가상 키보드·안전 영역(노치)까지 다루는지.
- 디자인 도구의 값과 코드의 값을 누가 어떻게 맞추는지.

## 판단 기준
- **토큰 계층:** 테마(다크 모드, 브랜드)가 둘 이상이거나 곧 생기면 원시값 → 의미 토큰 → 컴포넌트 토큰으로 나누고, 테마가 하나뿐이면 원시값과 의미 토큰 두 층으로 시작한다. 지키는 것: 테마 전환 비용.
- **컴포넌트 API:** 변형이 몇 개면 props로, 조합이 자유로워야 하면 compound component나 slot으로 나눠 props 폭증을 막는다. 지키는 것: 유연성 대비 일관성.
- **직접 만들지 빌려 올지:** 포커스 관리·키보드 이동·접근성 속성이 복잡한 부품(대화상자, 메뉴, 콤보박스)은 검증된 headless 부품을 쓰고, 단순한 표시 부품은 직접 만든다. 지키는 것: 접근성, 유지 비용.
- **입력 환경 대응:** 터치와 마우스에서 동작이 달라야 하면 화면 폭이 아니라 포인터·hover 미디어 쿼리로 가른다. 지키는 것: 기기별 사용성.

## 과설계 신호
- 테마가 하나이고 제품이 하나인데 3계층 토큰과 멀티 브랜드 거버넌스를 만든다.
- 쓰는 곳이 하나인 컴포넌트를 디자인 시스템에 넣는다.

## 지킬 장치
- 컴포넌트에서 원시 색상값·매직 넘버를 막는 lint 규칙.
- 공통 컴포넌트를 역할(role) 기준으로 찾는 컴포넌트 테스트와 시각 회귀 테스트.

## 원문
수치, 기준 번호, 지원 범위는 답할 때 여기서 확인한다.
- Design Tokens Format: https://www.designtokens.org/tr/drafts/format/
- Radix Primitives: https://www.radix-ui.com/primitives/docs/overview/introduction
- MDN pointer media feature: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/pointer
- MDN env(): https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/env
