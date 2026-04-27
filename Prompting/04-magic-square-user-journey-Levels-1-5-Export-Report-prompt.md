# Magic Square user journey epic
_Exported on 4/27/2026 at 17:24:27 GMT+9 from Cursor (3.0.16)_

---

**User**

Magic Square를 위한 사용자 여정 작성 (Epic → User Story → Task)을 하고자 합니다.
먼저, Level 1: Epic (비즈니스 목표): EPIC — Business Goal에 대한 내용을 다음처럼 작성해 주세요.
Epic: “Invariant(불변조건) 기반 사고 훈련 시스템 구축”
목적
- 4x4 Magic Square 문제를 활용하여:
- Invariant 중심 설계 사고 훈련
- Dual-Track TDD 적용 훈련
- 입력/출력 계약 명확화 훈련
- 설계 → 테스트 → 구현 → 리팩토링 흐름 체화

성공 기준
- Domain Logic 95% 이상 테스트 커버리지
- 입력 검증 100% 계약 테스트 통과
- 하드코딩 없음
- 매직 넘버 없음
- Invariant → Test 추적 가능

---

**Cursor**

내용을 파악했습니다. 이제 Epic 문서를 작성하겠습니다.

`Report/04-user-journey-epic.md` 파일을 작성했습니다. 구성 내용을 요약하면 다음과 같습니다.

---

**문서 구조 (7개 섹션)**

| 섹션 | 내용 |
|------|------|
| **1. 목적** | 4가지 훈련 영역을 "핵심 질문" 형태로 명확화 |
| **2. 배경 및 맥락** | 왜 4×4인지, Dual-Track TDD가 무엇인지 정의 |
| **3. 범위** | In Scope / Out of Scope 경계 명시 |
| **4. 핵심 Invariant 목록** | INV-01~10을 ID·적용 범위·위반 결과로 정리 |
| **5. 성공 기준** | 커버리지·추적 가능성 등 측정 방법까지 명시 |
| **6. Invariant → Test 추적 구조** | docstring 태그(`Invariant: INV-XX`) 형식 예시 |
| **7. ECB 레이어별 책임** | Boundary / Control / Entity 별 담당 Invariant 매핑 |

**핵심 설계 결정**

- `INV-09`: Magic Sum(34)과 격자 크기(4)를 `entity/constants.py`에 명명 상수로만 허용 — 하드코딩 금지를 Epic 수준에서 명시
- `INV-10`: 모든 테스트 함수에 `Invariant: INV-XX` 태그를 docstring으로 강제하여 **"Invariant → Test 추적 가능"** 성공 기준을 구조적으로 담보
- Dual-Track TDD(Contract Track / Algorithm Track)를 배경 섹션에서 정의하여 Level 2 User Story 분해의 기반으로 사용

Level 2 (User Story) 작성이 준비되면 `05-user-journey-stories.md`로 이어가시면 됩니다.

---

**User**

Level 2: User Journey (사용자 여정)를 다음 내용처럼 작성해 주세요.
Persona
소프트웨어 개발 학습자
TDD 훈련 중
Clean Architecture 이해 중

Journey
Step 1 — 문제 인식
“마방진을 구현한다”가 아니라

Step 2 — 계약 정의
입력 스키마 정의
출력 스키마 정의
예외 정책 정의


Step 3 — Domain 분리
BlankFinder
MissingNumberFinder
MagicSquareValidator
Solver

Step 4 — Dual-Track 진행
UI RED / Logic RED 병렬
GREEN 최소 구현
REFACTOR 통합 정리

Step 5 — 회귀 보호
엣지 케이스 추가
입력 오류 케이스 추가
조합 실패 케이스 추가

---

**Cursor**

`Report/05-user-journey-level2.md` 파일을 작성했습니다. 구성 내용을 요약하면 다음과 같습니다.

---

**Persona**

학습자의 핵심 불안("테스트를 먼저 짜야 한다는 건 알겠는데 무엇을 테스트해야 하는지 모르겠다")과 성공 신호를 명시하여, 여정이 누구를 위한 것인지를 먼저 고정했습니다.

---

**5개 Step 상세 구조**

각 Step마다 다음 4가지를 통일된 형식으로 기술했습니다.

| 항목 | 역할 |
|------|------|
| **핵심 원칙** | 이 단계에서 지켜야 할 사고 규칙 |
| **산출물** | 체크리스트 형태로 완료 여부를 측정 가능하게 |
| **완료 조건(Exit Condition)** | 다음 Step으로 넘어가기 위한 게이트 |
| **함정(Pitfall)** | 학습자가 자주 빠지는 오류와 그 결과 |

---

**Step별 핵심 내용**

| Step | 핵심 전달 |
|------|-----------|
| **Step 1** | "만든다" → "언제나 참인 것을 먼저 묻는다"는 사고 전환, 코드 0줄 조건 |
| **Step 2** | 입력 스키마·출력 스키마·예외 정책을 각각 표와 코드 예시로 명문화 |
| **Step 3** | `BlankFinder / MissingNumberFinder / MagicSquareValidator / Solver` 4개 컴포넌트의 책임·레이어·의존성 방향을 역방향 금지 예시와 함께 정의 |
| **Step 4** | Track A(계약)와 Track B(알고리즘)의 RED 예시 코드, GREEN 금지 행동 표, REFACTOR 순서 5단계 |
| **Step 5** | 엣지·오류·조합 실패 케이스를 Invariant ID와 연결한 표, 회귀 보호 실행 명령 포함 |

Level 3 (Task) 작성이 필요하시면 `06-user-journey-tasks.md`로 이어가시면 됩니다.

---

**User**

Level 3: User Stories를 다음 내용처럼 작성해 주세요.
Story 1 — 입력 검증
As a 학습자
I want to 입력이 정확히 4x4인지 검증되길 원한다
So that 잘못된 데이터가 Domain으로 전달되지 않도록 한다

Acceptance Criteria:
4x4가 아니면 예외
빈칸 2개 아니면 예외
중복 숫자 예외
범위 위반 예외

Story 2 — 빈칸 탐색
As a 학습자
I want to 0의 좌표를 정확히 찾고 싶다
So that 조합 시도가 가능하다

Acceptance Criteria:
row-major 순서 유지
정확히 2개 반환

Story 3 — 누락 숫자 탐색
Acceptance Criteria:
1~16 중 누락 2개
오름차순 반환

Story 4 — 마방진 판정
Acceptance Criteria:
모든 행 합 동일
모든 열 합 동일
대각선 동일

Story 5 — 두 조합 시도
Acceptance Criteria:
small→first blank 시도
실패 시 reverse
정답 배열 길이 6

---

**Cursor**

Level 3 User Stories 문서를 작성합니다. `05-user-journey-level2.md`와 Epic의 US 번호를 참고해 일관되게 맞춥니다.



`06-user-journey-stories.md`에 Level 3 User Stories를 작성합니다.



Epic 문서에 User Story가 `05-user-journey-stories.md`로 잘못 링크되어 있어 `06-user-journey-stories.md`로 정정합니다.



`Report/06-user-journey-stories.md`에 Level 3 User Stories를 정리해 두었고, Epic·Journey 문서에 있던 **다음 단계 링크**를 실제 파일명(`06`·`07`)에 맞게 맞춰 두었습니다.

---

**문서 구성 요약**

| Story | As a / I want / So that | 핵심 AC |
|-------|-------------------------|--------|
| **US-01** 입력 검증 | 요청하신 문장 그대로 + “빈칸 2개”를 **부분 퍼즐** 계약으로 설명 | 4×4 아님, 빈칸≠2, 중복, 범위 |
| **US-02** 빈칸 탐색 | `0` 좌표, row-major, 조합을 위해 | **정확히 2개**, row-major |
| **US-03** 누락 숫자 | `As a` 문장을 동일 톤으로 보강 | **누락 2개**, **오름차순** |
| **US-04** 마방진 판정 | 완성 격자 + 행·열·대각 + (권장) 1~16 퍼뮤테이션 | 행/열/대각 동일 |
| **US-05** 두 조합 | 작은 수→**첫** 빈칸, 실패 시 **reverse**, **정답 6원소** `[r0,c0,v0,r1,c1,v1]` | 2회 시도만(범위 밖은 별 Story) |

**Story 1과의 정합:** “빈칸 2개”는 이전의 “`0`은 임의 개수”와 달라서, **부분 퍼즐(빈칸 정확히 2·`0` 표기)** 을 US-01에 명시하고, INV-08(부분 vs 완성)과 `complete` 입력은 별 계약으로 나누는 식으로 적어 두었습니다.

**Story 5:** `정답 배열 길이 6`을 **row-major 첫/둘째 빈칸**에 넣은 값에 대응하는 `[r0,c0,v0,r1,c1,v1]` 로 해석해 AC-5.4에 넣었습니다.

**크로스 참조:** `04-user-journey-epic.md` §8의 “User Story 상세” 링크를 `06-user-journey-stories.md`로, `05-user-journey-level2.md` 끝의 “다음 문서”는 `06`(Stories) + `07`(Tasks)로 정리해 두었습니다.

---

**User**

Level 4:구현 시나리오 - Technical를 다음 내용처럼 작성해 주세요.
Feature: 4x4 마방진 완성

  불변조건 기반 로직을 검증하기 위해
  TDD를 연습하는 개발자로서
  부분적으로 채워진 4x4 마방진을 완성하고 싶다

  Background:
    Given 4x4 행렬이 주어지고
    And 0은 빈칸을 의미하며
    And 정확히 2개의 셀이 0을 포함하고 있고
    And 숫자는 1부터 16 사이여야 하며
    And 0을 제외한 중복 숫자는 허용되지 않으며
    And 4x4의 마방진 상수는 34이다

  Scenario: 작은 수 → 큰 수 순서로 마방진이 완성되는 경우
    Given 다음과 같은 행렬이 주어졌을 때:
      | 16 |  2 |  3 | 13 |
      |  5 | 11 | 10 |  8 |
      |  9 |  7 |  0 | 12 |
      |  4 | 14 | 15 |  0 |
    When 시스템이 빈칸 좌표를 찾고
    And 누락된 두 숫자를 찾은 뒤
    And 작은 숫자를 첫 번째 빈칸에 배치하고
    And 큰 숫자를 두 번째 빈칸에 배치하면
    Then 모든 행의 합은 34여야 하고
    And 모든 열의 합은 34여야 하며
    And 두 대각선의 합도 34여야 하고
    And 결과는 길이 6의 배열로 반환되어야 하며
    And 반환되는 좌표는 1-index 기준이어야 한다

  Scenario: 역순 배치 시 마방진이 완성되는 경우
    Given 다음과 같은 행렬이 주어졌을 때:
      | 16 |  2 |  3 | 13 |
      |  5 | 11 | 10 |  8 |
      |  9 |  7 |  0 | 12 |
      |  4 | 14 | 15 |  0 |
    When 작은 숫자를 첫 번째 빈칸에 배치했을 때 마방진이 되지 않고
    And 큰 숫자를 첫 번째 빈칸에 배치했을 때 마방진이 되면
    Then 시스템은 역순 배치 결과를 반환해야 하며
    And 최종 행렬은 마방진 상수 34를 만족해야 한다

  Scenario: 빈칸 개수가 올바르지 않은 경우
    Given 행렬에 빈칸이 1개만 존재할 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다

  Scenario: 중복 숫자가 존재하는 경우
    Given 0을 제외한 중복 숫자가 포함된 행렬일 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다

  Scenario: 값의 범위를 벗어난 경우
    Given 행렬에 16을 초과하는 숫자가 포함되어 있을 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다

---

**Cursor**

Level 4 Technical 시나리오 문서를 추가하고, 기존 Report와 링크를 맞춥니다.



표의 셀 정렬을 원문에 맞게 고치고, `06`의 ‘다음 문서’에 Level 4 링크를 추가합니다.



첫 시나리오에 넣은 구체 수치를 검산했는데, 주어진 격자는 **작은 수→첫 빈칸, 큰 수→둘째 빈칸**이면 마방진이 되지 않고, **역(6, 1)**이 맞습니다. 문서의 잘못된 ‘권장 Then’을 바로잡겠습니다.



`Report/08-level4-implementation-scenario-technical.md`를 추가해 두었습니다. 요지만 정리합니다.

---

**포함한 내용**

- **Level 4 메타데이터** (날짜, 상위 문서, 목적, Gherkin/도구 대응)
- **기술 약속** 표: Magic Sum 34(상수), 빈칸 2·`0`, **결과 6요소 + 좌표 1-based**
- 요청하신 **Feature / Background / 5 Scenarios**를 Gherkin 코드 펜스로 **그대로** 수록
- Invariant·US 매핑, `pytest-bdd` 스텁 예시, `07`·`.feature` 분리 안내
- `06-user-journey-stories.md`의 “다음 문서”에 **08** 링크 추가

---

**같은 격자에 대한 검산(문서에도 씀)**

주어진 4×4(빈칸 2)에서 누락 수는 **1·6**이고, row-major 첫/둘째 빈칸에 **(1,6)**이면 3·4행 합이 34가 되지 **않고**, **(6,1)**이면 **마방진**이 됩니다.  
그래서 **동일 `Given` 표**로 “작은 수 → 첫 빈칸, 큰 수 → 둘째 빈칸 **성공**”과 “**역**으로 성공” **둘 다**를 **그대로** 만족시키는 것은 **끼리** 맞지 않습니다. 문서에는 TDD 쪽에서 쓰려면 (1) **1차 성공 전용**은 **다른 행렬**로 두거나, (2) **Scenario 1·2**의 **Examples**를 **분리**하라고 적어 두었습니다. 요청하신 Gherkin 문장은 삭제하지 않고, **일관성**만 설명에 보강했습니다.

---

**User**

Level 5: 시나리오 검증 및 정리를 다음 내용처럼 작성해 주세요.
시나리오 완성도 체크리스트
✅ 4레벨 일관성 확인
Epic → Journey
[x] Epic의 성공 지표가 Journey에 반영됨
[x] Journey의 모든 단계가 Epic 목표 달성에 기여
[x] Pain Points가 명확히 정의됨
Journey → Story
[x] Journey의 각 Stage마다 최소 1개 Story
[x] Story가체적인 기능으로 변환됨
[x] Acceptance Criteria가 측정 가능
Story → Technical
[x] 모든 AC가 Gherkin 시나리오로 변환
[x] Given-When-Then이 명확
[x] 테스트 자동화 가능
✅ Edge Case 커버리지
정상 케이스
[x] Happy Path 시나리오 존재
예외 케이스
[x] 네트워크 오류
[x] 권한 없음
[x] 잘못된 입력
[x] 중복 실행
경계 케이스
[x] 최솟값, 최댓값
[x] 빈 값
[x] 특수 문자
✅ 사용자 중심성
실제 사용자 검증
[ ] 현장 엔지니어 1명과 시나리오 리뷰
[ ] 관리자 1명과 Journey 검증
[ ] 피드백 반영
감정 흐름
[x] 각 Journey Stage마다 감정 표시
[x] 부정 → 긍정 전환 명확
✅ 구현 가능성
기술 검증
[x] QR 스캔 라이브러리 조사 완료
[x] 오프라인 DB 방식 결정
[x] 자동 검증 알고리즘 설계
데이터 요구사항
[x] 필요한 Entity 모두 정의됨 (Mission 2)
[x] API 스펙 초안 작성

---

**Cursor**

Magic Square 프로젝트에 맞게 Level 5 문서를 작성합니다. 템플릿의 네트워크·QR 등 비관련 항목은 도메인에 맞게 치환합니다.



`Report/09-level5-scenario-verification.md`에 Level 5 **시나리오 검증 및 정리**를 반영해 두었습니다.

---

**구성 요약**

1. **4레벨 일관성**  
   - Epic↔Journey, Journey↔Story, Story↔Technical를 표로 정리하고, `04`~`08`과의 대응을 **비고**에 달았습니다.  
   - “모든 AC가 Gherkin으로 변환”은 `08` 기준으로 [x]로 두고, *일부는 `Scenario Outline` 권장*으로 명시했습니다.

2. **Edge Case**  
   - **네트워크·권한**은 본 프로젝트(로컬 CLI) 기준 **N/A** + 대체 해석(파일/권한은 추후)을 적었습니다.  
   - **중복 실행**은 *동일 입력에 대한 결정적(deterministic) 동작*으로 맞췄습니다.  
   - **최솟·최댓, 빈 값, 비숫자(특수)**는 `05`·`06`·`08`에 맞춰 [x]로 연결했습니다.

3. **사용자 중심**  
   - “현장 엔지니어/관리자”는 **동료·멘토, Epic·규칙 담당**으로 바꾸고 [ ]는 **리뷰·피드백**용으로 남겼습니다.  
   - **감정**은 `05` Persona·Pitfall·Exit으로 [x] 근거를 적었습니다.

4. **구현 가능성**  
   - QR / 오프라인 DB / API는 **N/A(범위 밖)**.  
   - **pytest, ECB, rules, 2빈칸 조합, Gherkin** 등으로 **대체 체크리스트**를 넣었고, CI·pytest-bdd는 [ ]로 남겼습니다.

5. **갭**  
   - `08`의 **동일 격자·시나리오 1·2** 수식 이슈(G1)를 **알려진 갭**으로 다시 짚었습니다.

6. **문서 맵**  
   - `04`~`08`과 **09(본 문서)** 만의 **Level 1~5** 추적 표를 넣었습니다.

`06` 끝에 `09` 링크를 붙이지는 않았습니다(요청 범위 밖). 필요하면 `06` “다음 문서”에 `09` 한 줄을 추가할 수 있습니다.

---

**User**

Report 폴더에 "04"로 시작하는 이름으로 지금 작업한 내용을 보고서로 내보내줘

---

**Cursor**

Report 폴더 구조를 확인한 뒤, `04`로 시작하는 통합 보고서를 작성합니다.



Report 폴더에서 L1~L5 원문을 하나로 병합하는 방식이 가장 정확합니다. 터미널로 병합한 뒤 머리말(표지·요약·색인)을 앞에 삽입합니다.



메타데이터 줄에 Markdown 줄바꿈(행 끝 공백 2칸)을 넣고, 임시 병합 스크립트는 제거합니다.



다음 파일을 **Report 폴더**에 **`04`로 시작하는 이름**으로 내보냈습니다.

---

**파일:** `c:\DEV\MagicSquare\Report\04-magic-square-user-journey-Levels-1-5-Export-Report.md`  
**크기:** 약 50 KB (Markdown 전문 병합)

**구성**

1. **머리말** — 통합 내보내기 목적, `source of truth` vs 이 파일(스냅샷) 관계  
2. **요약 표** — Level 1~5 ↔ 원본 파일명  
3. **부록** — 아래 5개 문서를 **2026-04-27 기준**으로 순서대로 이어 붙인 전문(각 절 앞에 `<!-- SNAPSHOT FROM: ... -->` 주석)
   - `04-user-journey-epic.md`
   - `05-user-journey-level2.md`
   - `06-user-journey-stories.md`
   - `08-level4-implementation-scenario-technical.md`
   - `09-level5-scenario-verification.md`

**의도적으로 넣지 않은 것** (머리말에 안내): `01`~`03` Report(문제 정의, 설계, cursorrules). 필요하면 같은 방식으로 부록에 추가하면 됩니다.

**참고:** 병합용 임시 스크립트는 남기지 않고 지웠습니다. 나중에 다시 합쳐야 하면 “같은 방식으로 병합”이라고만 요청해 주시면 됩니다.

