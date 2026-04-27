# Level 5: 시나리오 검증 및 정리

**작성일:** 2026-04-27  
**상위 문서:** `04` (Epic) · `05` (Journey) · `06` (Stories) · `08` (Technical Gherkin)  
**범위:** 4레벨 문서 일관성·엣지·사용자 중심·구현 가능성 점검, 남은 액션

---

## 1. 시나리오 완성도 체크리스트

### 1.1 4레벨 일관성 확인

#### Epic → Journey

| 항목 | 상태 | 비고 |
|------|------|------|
| Epic의 성공 지표가 Journey에 반영됨 | [x] | `04` §5(도메인 95%, 계약 100%, 매직 넘버 0, INV 추적) ↔ `05` Step 4~5, DoD |
| Journey의 모든 단계가 Epic 목표 달성에 기여함 | [x] | Step 1(인식)→Invariant, 2(계약), 3(도메인 분리), 4(Dual-Track), 5(회귀) |
| Pain Points가 명확히 정의됨 | [x] | `05` 각 Step **함정(Pitfall)** — “구현 먼저”, “계약 흐림”, “Entity↔Control 역의존” 등 |

#### Journey → Story

| 항목 | 상태 | 비고 |
|------|------|------|
| Journey의 각 Stage마다 최소 1개 Story | [x] | US-01~05가 Step 2~4에 대응(`06` 개요 표) |
| Story가 구체적인 기능으로 변환됨 | [x] | `BlankFinder` / `MissingNumberFinder` / `Validator` / `Solver` + 입력 검증 |
| Acceptance Criteria가 측정 가능함 | [x] | `06` 각 Story AC — 예외 종류, 개수(빈칸 2), 정렬, 6요소·1-based 등 |

#### Story → Technical

| 항목 | 상태 | 비고 |
|------|------|------|
| 모든 AC가 Gherkin 시나리오로 변환됨(또는 매핑됨) | [x] | `08` Feature + Scenarios; US-01(오류 3~5), US-05(성공·역). *일부 AC는 별도 `Scenario Outline` 권장* |
| Given-When-Then이 명확함 | [x] | `08` — Background, 표 기반 `Given`, `When` 절차 분리 |
| 테스트 자동화 가능 | [x] | `pytest-bdd` / `behave` / AAA 단위 테스트로 Step Definition 연결 가능(`08` § 끝) |

---

### 1.2 Edge Case 커버리지

#### 정상 케이스

| 항목 | 상태 | 비고 |
|------|------|------|
| Happy Path 시나리오 존재 | [x] | `08` “작은 수 → 큰 수” 완성(별도 `Given` 픽스처 권장) / “역순” 성공·`05` Step 4 Happy Path |

#### 예외 케이스

> 본 프로젝트는 **로컬 Python·CLI·네트워크 없음** 전제. 일반 웹/앱 체크리스트 항목은 **도메인에 맞게 대체**한다.

| 항목 | 상태 | Magic Square 대응 |
|------|------|-------------------|
| 네트워크 오류 | [N/A] | 네트워크 I/O 없음. *대체: 파일/외부 I/O 도입 시 재평가* |
| 권한 없음 | [N/A] | OS 권한 이슈 없음(순수 로컬). *대체: 결과 파일 쓰기 시 권한* |
| 잘못된 입력 | [x] | `08` Scenario: 빈칸 개수·중복·범위; `05` Step 5-2, `06` US-01 |
| 중복 실행 / 동시성 | [x] | *의미를 “동일 입력 재호출 시 결정적 결과”로 해석* — `Solver` 동일 `grid` → 동일 6요소(또는 동일 `None`); 병렬 미사용이면 [N/A]로도 가능 |
| (추가) 도메인 예외 | [x] | 4×4 아님, `0` 개수 ≠2, `TypeError` — `05` · `06` |

#### 경계 케이스

| 항목 | 상태 | Magic Square 대응 |
|------|------|-------------------|
| 최솟값, 최댓값 (허용 범위) | [x] | 값 **1, 16**; Magic Sum **34** — `constants` + `rules` 테스트 |
| 빈 값 | [x] | `[]` / `None` 격자 — `ValueError`·`TypeError` (`05` 5-2) |
| 특수 문자 | [x] | **CLI**에서 문자열 파싱 시: 비숫자·구분자 오류 — `Boundary` 계약 테스트(스펙에 있을 때) |
| (추가) 0 vs 빈칸 | [x] | `0` 정확히 2개 아님 — `08` / US-01 |

---

### 1.3 사용자 중심성

| 항목 | 상태 | 비고 |
|------|------|------|
| **실제 사용자 검증** | | *학습/훈련 프로젝트 — 역할을 아래로 조정* |
| 동료(또는 멘토) 1명과 **시나리오·Gherkin** 리뷰 | [ ] | `08` Feature / AC와 실제 퍼즐 수식 일치 여부 |
| 프로젝트 **규칙·Epic** 담당 1명과 **Journey** 정합 확인 | [ ] | `04`~`05`·Pain Point·DoD |
| **피드백 반영** (문서·취득기준) | [ ] | 리뷰 후 `Report/` 업데이트·커밋 |
| **감정 흐름** | [x] | `05` Persona — *핵심 불안 / 성공 신호*; *각 Step은 “인지 부담”→“통제감” 전환*으로 읽힘 |
| 각 Journey Stage마다 **감정/장애물** 표시(선택) | [x] | `05` **함정** = 부정, Exit Condition = 긍정 전환 훅 |
| **부정 → 긍정** 전환 명확 | [x] | Step마다 *완료 조건*으로 “다음으로 넘어갈 수 있음” 정의 |

---

### 1.4 구현 가능성 (Magic Square / ECB / TDD)

> 원본 제안의 *QR, 오프라인 DB, API*는 본 **학습·CLI·도메인** 범위에 맞지 않아 **다음 항목으로 대체**한다.

#### 기술·설계 검증 (대체 체크리스트)

| 항목 | 상태 | 비고 |
|------|------|------|
| `pytest`·`pytest-cov`·프로젝트 품질 기준(`.cursorrules`) 정합 | [x] | 커버리지 하한, contract 마커 |
| **ECB** 의존성 방향·금지 사항 (`boundary`→`control`→`entity`) 검토 | [x] | `05` Step 3, `04` §7 |
| **마방진·부분 퍼즐** 자동 판정 알고리즘(행·열·대각) 설계 | [x] | `06` US-04, `entity/rules` |
| **2빈칸 2수** 조합(순·역) 탐색 설계 | [x] | `06` US-05, `08` (동일 `Given`과 수식 주의 — `08` § 검산) |
| (선택) Gherkin 러너(`pytest-bdd`) 도입 시 Step Definition **중복** 방지 | [ ] | `tests/features/` 구조 |
| (선택) `black` / `mypy` / `isort` CI | [ ] | `pyproject.toml` 기준 |

#### 데이터·모델 요구사항 (대체)

| 항목 | 상태 | 비고 |
|------|------|------|
| 필요한 **Entity·상수** 정의(GRID_SIZE, MAGIC_SUM, `0`=빈칸) | [x] | `04` INV-09, `06`, `08` |
| **공개 API/계약** 초안(함수 시그니처, 예외) | [x] | `05` Step 2, `06` Story별 |
| REST/GraphQL **API** | [N/A] | Out of Scope(`04` §3) |
| **오프라인 DB** | [N/A] | 동일 |
| **QR** | [N/A] | 동일 |

---

## 2. 4레벨 추적 요약 (문서 ID)

| Level | 문서 | 역할 |
|-------|------|------|
| 1 | `04-user-journey-epic.md` | Epic, Invariant, 성공 기준 |
| 2 | `05-user-journey-level2.md` | Persona, Journey 5 Step, Pitfall |
| 3 | `06-user-journey-stories.md` | US-01~05, AC |
| 4 | `08-level4-implementation-scenario-technical.md` | Gherkin, BDD |
| 5 | 본 문서 | 검증·갭·N/A 정리 |

> `07-user-journey-tasks.md`는 **Task** 분해만 쓰는 경우 별도 유지; 없으면 `06` 하단 T-01~ 참고.

---

## 3. 알려진 갭(문서间)

| # | 갭 | 권장 조치 |
|---|----|-----------|
| G1 | `08` 동일 격자로 “작→큰 성공”·“역 성공” **동시** 만족 **불가** (수식) | `08`에 기술된 대로 **Scenario 1/2** `Given` **분리**·`Scenario Outline` |
| G2 | Level 5 **동료/멘토 리뷰** 미체크 | 캘린더 리뷰 1회 |
| G3 | BDD **자동 러너** 미연동 시 [x] “자동화 가능”은 **이론상** — 실제 [ ] 로 바꾸고 Step Def 구현 시 [x] |

---

## 4. 최종 Sign-off (필요 시)

| 역할 | 이름 | 날짜 | 승인 |
|------|------|------|------|
| Story·AC & Gherkin | | | ☐ |
| 엣지·경계·예외 & 테스트 | | | ☐ |
| 아키텍처(ECB)·TDD | | | ☐ |

---

*본 문서는 Level 5 (시나리오 검증 및 정리) 산출물이며, 리뷰·피드백 반영 후 [ ] 항목을 [x]로 갱신한다.*
