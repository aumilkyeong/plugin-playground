# 프론트엔드 보안

신뢰 경계(무엇을 믿고 무엇을 검증할지), 스크립트 주입 방어, 인증 정보를 둘 자리, 서드파티 코드의 권한을 정한다.

## 코드에서 먼저 확인할 것
- HTML을 문자열로 넣는 곳(`dangerouslySetInnerHTML`, `innerHTML`)과 사용자 입력이 URL·속성에 들어가는 곳.
- 인증 토큰의 위치: `localStorage`, 메모리, `HttpOnly` 쿠키, 서버 세션.
- 콘텐츠 보안 정책(CSP)의 유무와 내용, 인라인 스크립트와 서드파티 스크립트 목록.
- 권한 검사를 어디서 하는지: 서버(미들웨어, 서버 컴포넌트, API)인지 클라이언트 화면 숨김뿐인지.
- 앱 웹뷰나 다른 창에서 오는 메시지를 출처 확인 없이 처리하는 곳.

## 판단 기준
- **권한 검사 위치:** 데이터 접근 권한은 항상 서버에서 판정하고, 클라이언트 검사는 화면 편의로만 쓴다. 지키는 것: 기밀성.
- **토큰 위치:** 브라우저에서 쓰는 세션이면 `HttpOnly; Secure; SameSite` 쿠키나 서버 세션에 두고, 스크립트가 읽어야만 하는 토큰이면 수명을 짧게 하고 메모리에 둔다. 쿠키 인증이면 CSRF 방어를 함께 정한다. 지키는 것: 탈취 시 피해 범위.
- **HTML 삽입:** 서식 있는 사용자 콘텐츠를 보여야 하면 정제 라이브러리를 거치고 삽입 지점을 한 곳으로 모은다. 서식이 필요 없으면 텍스트로만 그린다. 지키는 것: XSS 방어.
- **CSP:** 서드파티 스크립트가 적고 통제 가능하면 nonce 기반의 엄격한 정책, 많고 바꾸기 어려우면 보고 전용으로 시작해 위반을 모은 뒤 조인다. 지키는 것: 주입 피해 축소.
- **메시지 수신:** 다른 창·웹뷰에서 오는 메시지는 출처와 형식을 검증한 뒤에만 처리한다. 지키는 것: 신뢰 경계.

## 과설계 신호
- 공격 표면이 작은 내부 도구에 외부 서비스 수준의 다층 정책을 한꺼번에 들인다(위협 모델 없이).

## 지킬 장치
- HTML 직접 삽입 API를 lint로 막고, 허용 지점 하나만 예외로 둔다.
- CSP 위반 보고를 수집한다.
- 보안 헤더(CSP, 쿠키 속성)를 E2E나 응답 검사로 확인한다.

## 원문
수치, 기준 번호, 지원 범위는 답할 때 여기서 확인한다.
- MDN CSP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
- OWASP XSS Prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- OWASP Session Management: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP CSRF Prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- MDN Trusted Types: https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API
