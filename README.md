# Magic Square (4×4) — 부분 격자 완성

Invariant(불변조건)와 **UI·Logic 이원 TDD**, **ECB(Entity–Control–Boundary)** 를 연습하기 위한 **4×4 Magic Square** 프로젝트이다.  
부분적으로 비어 있는 격자(빈칸 `0` **2개**)를, 약속된 절차(최대 두 조합 시도)로 완성하는 **CLI 중심** 학습 코드베이스를 목표로 한다.

---

## 범위 (요약)

요구사항의 **한줄 요약**은 [`docs/PRD.md`](docs/PRD.md)를 본다.

| 구분 | 내용 |
|------|------|
| **In scope** | 4×4 도메인, 입력 검증 계약, 마방진 판정, 빈칸 2개 부분 격자 완성 흐름, ECB, CLI 경계, pytest·커버리지 하한 |
| **Out of scope** | GUI/Web UI, DB 영속(필수 아님), 5×5 이상 |

자세한 스토리·Invariant 매핑은 PRD [§2](docs/PRD.md#2-범위-scope)·[§4](docs/PRD.md#4-핵심-invariant-epic-기준-inv-0110)·[§5](docs/PRD.md#5-기능-요구사항-user-stories-us-0105)를 참고한다.

---

## 문서 지도

| 목적 | 문서 |
|------|------|
| 목표·범위·스토리 압축·NFR | [**docs/PRD.md**](docs/PRD.md) |
| User Story·수용 기준(AC)·컴포넌트 **정본** | [**Report/04.3-user-journey-stories.md**](Report/04.3-user-journey-stories.md) |
| 도메인 API·CLI 계약·에러코드·검증 순서 | [**Report/02-4x4-magic-square-tdd-clean-architecture-design.md**](Report/02-4x4-magic-square-tdd-clean-architecture-design.md) |
| 문제 정의(코드 없음) | [Report/01-4x4-magic-square-problem-definition.md](Report/01-4x4-magic-square-problem-definition.md) |
| Epic·여정 | [Report/04.1-user-journey-epic.md](Report/04.1-user-journey-epic.md), [Report/04.2-user-journey-level2.md](Report/04.2-user-journey-level2.md) |
| Gherkin·Level5 검증 | [Report/04.4-level4-implementation-scenario-technical.md](Report/04.4-level4-implementation-scenario-technical.md), [Report/04.5-level5-scenario-verification.md](Report/04.5-level5-scenario-verification.md) |
| `.cursorrules` 설계 메모 | [Report/03-cursorrules-setup.md](Report/03-cursorrules-setup.md) |
| L1~L5 통합 스냅샷 | [Report/04-magic-square-user-journey-Levels-1-5-Export-Report.md](Report/04-magic-square-user-journey-Levels-1-5-Export-Report.md) |

> **참고:** PRD의 표에는 `06-user-journey-stories.md` 등 이전 파일명이 나올 수 있다. 이 저장소의 **Level 3 User Stories 정본 파일명**은 **`Report/04.3-user-journey-stories.md`** 이다.

---

## 아키텍처 원칙 (요약)

- **ECB:** `entity`(규칙·상태) / `control`(유스케이스 흐름) / `boundary`(CLI·입력 1차 검사·출력 직렬화). Entity는 Boundary에 의존하지 않는다. ([PRD §6.1](docs/PRD.md#61-ecb-프로젝트-규칙))
- **Dual-Track TDD:** **UI 트랙** = 경계의 UX Contract(메시지·에러코드) RED. **Logic 트랙** = 도메인·Control RED. 서로 구현 세부에 의존하지 않는다. ([PRD §2.4](docs/PRD.md#24-dual-track-범위-정렬-ui--logic--mlops))

구체적 클래스명·입출력 스키마는 **Report/02**를 따른다.

---

## User Story 요약 (PRD §5 + 04.3 정본)

| ID | 제목 | 한 줄 |
|----|------|--------|
| **US-01** | 입력 검증 | 4×4, 빈칸(`0`) 2개, 0이 아닌 값의 범위·중복 검증 |
| **US-02** | 빈칸 탐색 | `0` 위치를 row-major로 2개 |
| **US-03** | 누락 숫자 | 1~16 중 누락 2개, 오름차순 |
| **US-04** | 마방진 판정 | 완성 격자에 대해 행·열·대각·Magic sum 및 순열 |
| **US-05** | 두 조합 시도 | 작은 수→첫 빈칸·큰 수→둘째, 실패 시 역; 최대 2회; 성공 시 6원소·1-based 좌표 |

**의존(권장):** US-01 → US-02 / US-03 → US-04 → US-05.

---

## To-Do List

### Traceability — To-Do → Work Order

- **핵심:** 모든 상위 To-Do가 곧바로 “테스트 한 개”로 떨어지지는 않는다. **어떤 조건을 허용·거부할지, 무엇을 반환·표시할지** 같은 **판단(Decision)**이 생기는 지점만 **검증 가능한 계약(Work Order)**으로 쪼갠다.  
- **비율:** **To-Do 1 : Work Order N** — 한 스토리(또는 경계 시나리오)에서 RED로 고정할 “결정”이 여러 개면, Work Order는 그만큼 늘어난다. (명명·리팩터·디렉터리 정리 같이 **판단이 없는** 작업은 Work Order·테스트에 강제로 맞출 필요가 없다.)  
- **이 프로젝트:** GUI는 범위 밖([PRD §2.2](docs/PRD.md#22-out-of-scope))이므로, 슬라이드의 «격자 UI»에 해당하는 것은 **CLI/Boundary**의 **입력 수신·형식·성공/실패 메시지**로 둔다.  
- **정본:** User Story·AC → [`Report/04.3-user-journey-stories.md`](Report/04.3-user-journey-stories.md) ; 계약·에러·I/O → [`Report/02-4x4-magic-square-tdd-clean-architecture-design.md`](Report/02-4x4-magic-square-tdd-clean-architecture-design.md).

### 상위 To-Do (무엇을 끝낼 것인가)

| ID | 항목 | 정본 |
|----|------|------|
| **TD-1** | 부분 격자·**입력 검증** (US-01) | 04.3 Story 1, 02 InputContract·검증 순서 |
| **TD-2** | **빈칸** row-major 2곳 (US-02) | 04.3 Story 2, 02 `BlankLocator` |
| **TD-3** | **누락 2수**·후보 쌍 (US-03) | 04.3 Story 3, 02 `MissingNumberDetector` |
| **TD-4** | **완성** 격자 **마방진 판정** (US-04) | 04.3 Story 4, 02 `MagicSquareValidator` |
| **TD-5** | **두 조합**·솔버 오케스트레이션 (US-05) | 04.3 Story 5, 02 `CombinationEvaluator`·`MagicSquareSolver` |
| **TD-6** | **Boundary** — CLI·에러·출력 (Dual-Track **UI** 측) | 02 §2 Screen Layer, ErrorContract, §2.4 문구 |
| **TD-7** | **NFR** — 커버리지, 상수, INV–테스트 추적 | [PRD §8](docs/PRD.md#8-비기능-요구-nfr--품질-목표) |

- [ ] **TD-1** — US-01 완료 (검증된 `int[][]` / `Matrix4x4`만 도메인으로)
- [ ] **TD-2** — US-02 완료
- [ ] **TD-3** — US-03 완료
- [ ] **TD-4** — US-04 완료
- [ ] **TD-5** — US-05 완료
- [ ] **TD-6** — CLI·에러·성공 6원소 직렬화 (로직 규칙은 Entity/Control에만)
- [ ] **TD-7** — NFR·품질 게이트

### To-Do → Work Order (검증 계약, 1:N)

아래 **WO-\*** 는 “**무엇을 판정·고정할지**”를 나눈 것이다. 테스트 이름은 팀 컨벤션에 맞게 붙이되, **같은 판단**이면 **하나의 Work Order**에 묶는다.

#### TD-1 · US-01 — 입력 검증·부분 격자

| WO ID | ECB | Work Order(판단·검증 계약) | 참고 |
|-------|-----|---------------------------|------|
| **WO-1.1** | **Boundary** | 4×4가 아니면 `INVALID_SIZE` (다른 위반과 겹쳐도 **이 코드가 먼저**). | 02 §2.3, UI-SZ-\* |
| **WO-1.2** | **Boundary** | 셀 값이 0~16이 아니면 `INVALID_VALUE_RANGE` (row-major **첫** 위반). | 02 UI-VR-\* |
| **WO-1.3** | **Boundary** | `0`의 개수가 2가 아니면 `INVALID_BLANK_COUNT`. | 02 UI-BC-\* |
| **WO-1.4** | **Boundary** | 0을 제외한 값이 중복이면 `INVALID_DUPLICATE` (첫 쌍). | 02 UI-DU-\* |
| **WO-1.5** | **Entity** (또는 팩터리) | 위를 통과한 격자를 **불변** `Matrix4x4`(동등)로 표현. **도메인 숫자는 0~16·2빈칸**이란 사실만; 마방진 여부는 여기서 판정하지 않음. | 04.3 AC-1.1~1.4, INV-08 |

#### TD-2 · US-02 — 빈칸 탐색

| WO ID | ECB | Work Order(판단·검증 계약) | 참고 |
|-------|-----|---------------------------|------|
| **WO-2.1** | **Entity** | `0` 칸 좌표 **2개**를 **row-major**로 반환. | 04.3 AC-2.1, INV-09(논리) |
| **WO-2.2** | **Entity** (엣지) | 선제 조건(빈칸 수 ≠2)이면 `IllegalStateException` 등 **도메인 내부** 실패 — 보통은 TD-1에서 차단. | 02 BL-05~07 |

#### TD-3 · US-03 — 누락 숫자

| WO ID | ECB | Work Order(판단·검증 계약) | 참고 |
|-------|-----|---------------------------|------|
| **WO-3.1** | **Entity** | 1~16 중 격자에 없는 수 **정확히 2개**, **오름차순** 리스트(또는 `MissingPair`). | 04.3 AC-3.1~3.2, 02 MD-\* |

#### TD-4 · US-04 — 완성 마방진 판정

| WO ID | ECB | Work Order(판단·검증 계약) | 참고 |
|-------|-----|---------------------------|------|
| **WO-4.1** | **Entity** | **완성(0 없음)** 격자에 대해 `validate() -> bool` — 4행·4열·주·부 대각 **모두 동일 합(34)**. | 04.3 AC-4.1~4.3, 02 `MAGIC_SUM` 상수 |
| **WO-4.2** | **Entity** | 위가 참일 때(또는 팀 합의에 따라) **1~16 순열**이 아니면 `false` (INV-03과 정합). | 04.3 AC-4.5 |
| **WO-4.3** | **Entity** | `0`이 남은 격자는 **완성 판정 API에 넣지 않음** (예: `ValueError` 또는 `false` — **팀이 하나로 고정**). | 04.3 AC-4.4 |

#### TD-5 · US-05 — 두 조합·솔버

| WO ID | ECB | Work Order(판단·검증 계약) | 참고 |
|-------|-----|---------------------------|------|
| **WO-5.1** | **Control** | 누락 두 수(오름차순 **작은 수, 큰 수**)에 대해 **1차:** 작은 수→빈칸1, 큰 수→빈칸2 (row-major 빈칸). 완성 후 TD-4로 판정. | 04.3 AC-5.1~5.2, INV-10 |
| **WO-5.2** | **Control** | 1차 실패 시 **2차:** 큰 수→빈칸1, 작은 수→빈칸2. | 04.3 AC-5.3, 최대 2회 AC-5.5 |
| **WO-5.3** | **Control** / **Entity** | 성공 시 `Solution` = `int[6]`: `[r1,c1,n1,r2,c2,n2]` (좌표 **1-based**). | 02 OutputContract |
| **WO-5.4** | **Control** | 둘 다 실패: 도메인 `NoSolutionException` 등 → Boundary에서 `NO_SOLUTION`. | 02 ErrorContract, UC-04 |

#### TD-6 — Boundary (CLI = «UI» 트랙, 슬라이드의 표시·출력에 대응)

| WO ID | ECB | Work Order(판단·검증 계약) | 참고 |
|-------|-----|---------------------------|------|
| **WO-6.1** | **Boundary** | 원시 입력(파일/stdin/argv) → `int[4][4]` 파싱; 실패는 TD-1과 **동일 에러체계**로. | 02 흐름 1~5단계 |
| **WO-6.2** | **Boundary** | `MagicSquareSolver`(또는 유스케이스) **호출 전**에 1~4단계 검증 끝내기(도메인에 쓰레기 미전달). | PRD §6.1, ECB |
| **WO-6.3** | **Boundary** | **성공:** 6원소·형식·좌표 범위 `1..4` (02 UI-FMT-01~03). **실패(무해):** 고정 문구 `NO_SOLUTION` (02 §2.4). | Dual-Track |

#### TD-7 — NFR

| WO ID | — | Work Order(판정) | 참고 |
|-------|---|------------------|------|
| **WO-7.1** | | 전체 커버리지 **≥80%**, 도메인 목표 **≥95%**. | [PRD §8](docs/PRD.md#8-비기능-요구-nfr--품질-목표) |
| **WO-7.2** | | Magic sum 등 **하드코딩 숫자 없음** — `entity/constants`. | PRD §4 INV-09 |
| **WO-7.3** | | (선택) `Invariant: INV-XX` / `@pytest.mark.contract` 로 추적. | 04.3 TDD 힌트, PRD §8 |

**상세 Phase 체크리스트·같이 보기:** [**docs/IMPLEMENTATION-TODO.md**](docs/IMPLEMENTATION-TODO.md) · [`Report/06-readme-implementation-todo-export.md`](Report/06-readme-implementation-todo-export.md) (내보내기 요약)

---

## 빠른 시작 (구현 후)

애플리케이션 패키지·엔트리포인트가 추가되면 이 절에 설치·실행 예시를 적는다. (현재는 요구사항·설계 문서가 선행된 상태다.)

```bash
# 예시 (구현 시 조정)
# python -m magic_square ...
# pytest
```

---

## 라이선스

미정 — 저장소에 `LICENSE`가 추가되면 이 문서를 갱신한다.
