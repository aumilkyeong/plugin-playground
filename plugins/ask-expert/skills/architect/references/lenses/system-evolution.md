# 경계와 진화: 도메인, 팀, 점진 이전

모듈·서비스 경계를 어디에 긋고, 기존 구조를 멈추지 않고 어떻게 바꾸고, 결정을 어떻게 남기고 지킬지 정한다.

## 코드에서 먼저 확인할 것
- 같은 단어가 영역마다 다른 뜻으로 쓰이는가 (경계 후보)
- 기능 하나를 바꿀 때 함께 고쳐야 하는 폴더·팀 수
- 바꾸려는 기존 코드를 몇 곳에서 부르는가, 호출부를 한 곳으로 모을 수 있는가
- 이미 내린 결정 기록(ADR)과 그것을 지키는 자동 검사가 있는가
- 이 영역을 맡는 사람·팀 수와 그들이 함께 알아야 하는 범위

## 판단 기준
- **경계 긋기:** 용어의 뜻이 바뀌는 곳, 함께 바뀌는 코드 묶음을 경계로 둔다. 경계 사이는 공개 API로만 오간다. 지키는 것: 변경 범위, 인지 부하
- **공들일 곳:** 차별화되는 핵심 영역은 직접 만들고 깊게 설계한다. 지원 영역은 단순하게. 흔한 영역(인증, 결제, 검색)은 기성품이나 외부 서비스를 쓴다
- **바꾸는 방법:** 빅뱅 재작성 대신 단계적으로 바꾼다. 바깥 경로를 하나씩 새 구현으로 돌리면 strangler fig, 내부 의존을 바꾸면 branch by abstraction(추상화를 먼저 끼우고 뒤를 바꿈), 낡은 모델이 새 모델로 새어 들면 번역 계층(anti-corruption layer)
- **팀과 구조:** 경계를 한 팀이 감당할 수 있는 범위에 맞춘다. 구조는 소통 경로를 닮으므로(콘웨이 법칙) 경계를 바꾸면 담당도 함께 바꾼다
- **결정 남기기:** 되돌리기 어려운 결정은 ADR(대안, 포기한 것, 다시 볼 조건)로 남기고, 지킬 수 있는 규칙은 자동 검사로 강제한다

## 과설계 신호
- 팀이 하나인데 팀 경계를 이유로 서비스를 나눈다
- 경계가 아직 흔들리는 초기에 서비스·패키지를 물리적으로 나눈다
- 흔한 영역을 직접 만든다

## 지킬 장치
- 의존 규칙 정적 검사(예: dependency-cruiser, ArchUnit): 경계 밖에서는 공개 진입점만 import한다
- 순환 의존 검사

## 원문
수치, 기준 번호, 지원 범위는 답할 때 여기서 확인한다.
- Strangler fig application: https://martinfowler.com/bliki/StranglerFigApplication.html
- Branch by abstraction: https://martinfowler.com/bliki/BranchByAbstraction.html
- Bounded context: https://martinfowler.com/bliki/BoundedContext.html
- Conway's law: https://martinfowler.com/bliki/ConwaysLaw.html
- Team Topologies key concepts: https://teamtopologies.com/key-concepts
- Architecture decision records: https://adr.github.io/
