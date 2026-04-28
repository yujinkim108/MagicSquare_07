# To-Do 리스트 작성 참고 문서
_Exported on 4/28/2026 at 10:59:37 GMT+9 from Cursor (3.2.11)_

---

**User**

To-Do 리스트를 작성하고 싶습니다. 작성한 문서 중 무엇을 참조해서 만들어야 할까요?

---

**Cursor**

프로젝트 문서를 확인해 To-Do 리스트 작성에 참고할 자료를 파악합니다.



To-Do 리스트를 **무엇을 기준으로 쪼갤지**에 따라 참고 문서를 나누면 됩니다.

## 1. 먼저 볼 문서: `docs/PRD.md`

지금 워크스페이스에 있는 **`docs/PRD.md`**가 **한 번에 보는 요약본**입니다. 여기서 다음을 가져오면 To-Do의 **큰 축**을 잡기 좋습니다.

- **범위** (§2): In / Out of Scope  
- **User Story 순서** (§5): US-01 → US-02·US-03 → US-04 → US-05  
- **Invariant** (§4): INV-01~10  
- **비기능** (§8): 커버리지, 계약 테스트 등  
- **열린 이슈** (§9): G1~G3 같은 검증·데이터 이슈  

PRD 자체가 “**개별 `Report/*.md`가 상세·정본**”이라고 적혀 있어서, **작업 단위를 세분화할 때는 아래 Report로 내려가면 됩니다.

---

## 2. 작업 항목·수용 기준의 정본: `Report/`

PRD §2.3·§11에 나온 **레벨별 Report**를 쓰는 게 맞습니다.

| To-Do에 넣을 내용 | 주로 쓰는 문서 |
|------------------|----------------|
| Epic·성공 기준·INV 추적 | `04.1-user-journey-epic.md` (PRD의 `04-user-journey-epic`에 해당) |
| 단계별 여정·Pitfall | `04.2-user-journey-level2.md` |
| **US-01~05·AC·의존** | `04.3-user-journey-stories.md` (PRD에 적힌 `06-user-journey-stories`와 동일 계열) |
| **도메인 계약·I/O·에러코드·컴포넌트명** | `02-4x4-magic-square-tdd-clean-architecture-design.md` |
| Gherkin·기술 약속 | `04.4-level4-implementation-scenario-technical.md` |
| 검증·갭·Sign-off | `04.5-level5-scenario-verification.md` |
| L1~L5 한꺼번에 훑기 | `04-magic-square-user-journey-Levels-1-5-Export-Report.md` (병합 스냅샷, **세부는 개별 Report 우선**) |

**구현/테스트 할 일 목록**을 쓴다면 **`04.3-user-journey-stories` + `02`**를 같이 보는 구성이 가장 직접적입니다. Story는 04.3, “무엇을 반환·어떤 코드로 막는지”는 02에 있습니다.

---

## 3. 권장하지 않는 쪽: `Prompting/`

`*_prompt.md`는 Report를 **만들 때 쓰인 대화 흔적**이고, PRD에도 요구사항 본문은 **Report**를 보라고 되어 있습니다. To-Do의 근거 문서로는 **Report / PRD**를 쓰는 편이 좋습니다.

---

**요약:** **백로그·우선순위·스코프**는 **`docs/PRD.md`**, **구체적 할 일·AC·계약**은 **`Report/04.3` + `Report/02`** (필요 시 `04.4`·`04.5`)를 참조해 To-Do를 만드는 흐름이 문서 구조와 맞습니다.

---

**User**

당신은 시니어 소프트웨어 아키텍트이자 TDD 코치입니다. **04.3-user-journey-stories + 02**를 같이 보는 구성이 가장 직접적입니다. Story는 04.3, “무엇을 반환·어떤 코드로 막는지”는 02에 있습니다.
다음 방법론을 적용하여
"Magic Square 4x4 완성 시스템"의 구현용 To-Do 구조를 작성하세요.
적용 방법론:
Concept-to-Code Traceability
Dual-Track UI + Logic TDD
To-Do → Scenario → Test → Code 구조
ECB(Entity / Control / Boundary) 모델
RED → GREEN → REFACTOR
반드시 한국어로 작성하세요.
[시스템 목표]
부분적으로 비어 있는 4x4 Magic Square를 완성하는 시스템의 개발 To-Do를 작성합니다.
[도메인 규칙]
보드는 4x4이다.
숫자는 1~16만 사용한다.
0은 빈칸이다.
정확히 2칸이 비어 있다.
0을 제외한 중복 숫자는 허용되지 않는다.
모든 행, 열, 대각선의 합은 34여야 한다.
해결 가능한 경우 빈칸 값을 찾아 채운다.
유효하지 않은 보드는 거부한다.
[출력 형식]
다음 구조를 반드시 지켜서 작성하세요.
Epic
User Story
Phase별 Task 목록
각 Task에는 반드시 아래 정보를 포함하세요.
Task ID
RED / GREEN / REFACTOR 여부
작업 제목
Scenario Level (L0/L1/L2/L3)
연결되는 Test 이름
연결되는 Code 대상
ECB 스테레오타입 (Entity / Control / Boundary)
필요 시 체크포인트
[표현 스타일]
Markdown 사용
체크박스 형식 사용
실제 Cursor.AI 실습용 개발 보드처럼 작성
식별자는 Epic-001, US-001, TASK-001 형식 사용
유효한 케이스와 실패 케이스를 모두 포함
최소한 다음 작업을 포함
보드 생성
보드 유효성 검사
빈칸 탐지
후보값 필터링
완성 로직
잘못된 입력 처리
테스트 커버리지 체크포인트
[Scenario Level 정의]
L0: 기능 개요
L1: 정상 흐름
L2: 경계 상황
L3: 실패 상황
[추가 제약]
Logic 책임은 명확히 분리할 것
UI/Boundary에는 비즈니스 규칙을 넣지 말 것
Control은 검증과 해결 흐름을 조율할 것
Entity는 보드 상태를 표현할 것
모든 To-Do는 Scenario, Test, Code로 추적 가능해야 함
이제
"Magic Square 4x4 완성 시스템"의 To-Do 구조를 생성하세요.


---

**Cursor**

04.3과 02 문서를 읽어 식별자·시나리오·컴포넌트명을 정합시킵니다.



04.3의 Story ID(US-01~05)와 02의 컴포넌트·TC ID·에러 계약을 맞춰, 요청하신 표·체크리스트·추적 필드를 갖춘 구현용 To-Do 보드를 작성합니다. (요청에 따라 **문서 본문은 한국어**로만 기술합니다.)

---

# Magic Square 4×4 완성 시스템 — 구현용 To-Do 보드

**적용 방법론:** Concept-to-Code Traceability · Dual-Track(UI + Logic) TDD · To-Do → Scenario → Test → Code · ECB · RED → GREEN → REFACTOR  
**정본 Story:** `Report/04.3-user-journey-stories.md`  
**정본 계약·I/O:** `Report/02-4x4-magic-square-tdd-clean-architecture-design.md`  
**듀얼 트랙:** **UI(경계)** = UX Contract·에러코드·검증 순서 RED / **Logic** = Entity·Control·도메인 규칙 RED (서로 내부 구현에 의존하지 않음)

---

## Epic

| ID | 제목 | 추적 (Concept) | 성공 기준(요약) |
|----|------|----------------|-----------------|
| **Epic-001** | 4×4 부분(빈칸 2) 마방진 완성 | INV-01~10, US-01~05 (04.3) | 유효 보드는 6원소 해 또는 명시적 무해; 무효 보드는 경계에서 거부(02 ErrorContract) |

---

## User Story (US-001 ~ US-005)

| ID | 04.3 대응 | 제목 | Logic / Boundary |
|----|-----------|------|------------------|
| **US-001** | US-01 | 부분 격자 **보드 생성**·**구조적 유효성** (4×4, 0=빈칸 2, 범위·중복) | Entity `Matrix4x4` + (선택) 팩터리; **1차 거절**은 Boundary에서 순서대로(02 §2.3) |
| **US-002** | US-02 | **빈칸 탐지** (row-major 2칸) | Entity `BlankLocator` |
| **US-003** | US-03 | **누락 2수·후보 쌍** (오름차순, `MissingPair`) | Entity `MissingNumberDetector` |
| **US-004** | US-04 | **완성 격자 마방진 판정** (행·열·대각·1~16 순열) | Entity `MagicSquareValidator` + `rules` |
| **US-005** | US-05 | **두 조합 시도** + **전체 풀이 오케스트레이션** | Control `CombinationEvaluator`, `MagicSquareSolver` |

---

## Phase 0 — 프로젝트 골격·추적·듀얼 트랙

- [ ] **TASK-001** | **RED** | **L0** | pytest·패키지 골격·`src`/`tests` 분리 | `tests/test_smoke_imports` | `pyproject.toml`, `src/magic_square/` | **Boundary+공통** | **체크포인트:** Logic 테스트와 Boundary 테스트 디렉터리 분리 (`tests/entity/`, `tests/control/`, `tests/boundary/`)
- [ ] **TASK-002** | **GREEN** | **L0** | 위 스모크 통과 | 동일 | 패키지 `__init__` | **—** | —
- [ ] **TASK-003** | **REFACTOR** | **L0** | `black`/`isort`/`mypy` 스크립트 또는 `pyproject` 정렬 | (품질 게이트) | `pyproject.toml` | **—** | **체크포인트:** public API는 타입힌트 (03-cursorrules 정합)

---

## Phase 1 — Epic-001 / US-001: 상수·보드(Entity)·경계 검증( Boundary )

**시나리오 → 테스트 → 코드 (추적)**  
도메인 상수·완성 판정에 쓰일 **MAGIC_SUM=34**는 `entity/constants`에 두고, **비즈니스 판정 로직은 Boundary에 넣지 않음** (02 §2.1 단계 1~5는 스키마 검증만).

- [ ] **TASK-010** | **RED** | **L1** | `MAGIC_SUM` 및 명명 상수 | `test_constants_magic_sum_equals_34` | `src/.../entity/constants.py` | **Entity** | INV-02~04 (Epic) / 02 §1.2
- [ ] **TASK-011** | **GREEN** | **L1** | 상수 구현 | 동일 | `constants.py` | **Entity** | —
- [ ] **TASK-012** | **RED** | **L1** | 유효 **부분 격자**로 `Matrix4x4`/`Cell` 생성 | `test_matrix4x4_from_valid_partial_grid` | `matrix4x4.py`, `cell.py` | **Entity** | **Scenario:** 4×4, 0 정확히 2, 0 제외 1~16·무중복
- [ ] **TASK-013** | **GREEN** | **L1** | VO 최소 구현 | 동일 | `matrix4x4.py` | **Entity** | —
- [ ] **TASK-014** | **RED** | **L2** | 동일 값이 0이 아닌 인접 칸에 있어도 **스키마만** 맞으면 생성 가능(도메인는 “퍼즐 풀 수 있음”을 보장하지 않음) | `test_matrix4x4_accepts_valid_shape_only` | `Matrix4x4` | **Entity** | 04.3: 중복·빈칸 수 틀림은 US-01에서 먼저 막힘
- [ ] **TASK-015** | **RED** | **L3** | Boundary: **크기** 오류 `INVALID_SIZE` (02 UI-SZ-01~06, **검증 순서 1**) | `test_input_validator_invalid_size_ui_sz_01` | `input_validator.py` 또는 `cli/validate.py` | **Boundary** | **Dual-Track UI:** Mock Solver 없이 **에러코드·문구**만
- [ ] **TASK-016** | **GREEN** | **L3** | `4×4`·행 길이 검사 구현 | 동일 | `input_validator.py` | **Boundary** | 메시지 패턴 02 §2.4
- [ ] **TASK-017** | **RED** | **L3** | `INVALID_VALUE_RANGE` (02 UI-VR-01~02, 순서 2) | `test_input_validator_invalid_value_range` | `input_validator.py` | **Boundary** | row-major **첫** 위반만 보고
- [ ] **TASK-018** | **GREEN** | **L3** | 0~16 범위 검사 | 동일 | `input_validator.py` | **Boundary** | —
- [ ] **TASK-019** | **RED** | **L3** | `INVALID_BLANK_COUNT` (02 UI-BC-01~04, 순서 3) | `test_input_validator_invalid_blank_count` | `input_validator.py` | **Boundary** | 0이 0,1,3,16개인 케이스
- [ ] **TASK-020** | **GREEN** | **L3** | 0 개수=2 검사 | 동일 | `input_validator.py` | **Boundary** | —
- [ ] **TASK-021** | **RED** | **L3** | `INVALID_DUPLICATE` (02 UI-DU-01~02, 순서 4) | `test_input_validator_invalid_duplicate` | `input_validator.py` | **Boundary** | 0은 제외
- [ ] **TASK-022** | **GREEN** | **L3** | 중복 검사 | 동일 | `input_validator.py` | **Boundary** | —
- [ ] **TASK-023** | **REFACTOR** | **L2** | 검증 단계 `SIZE → RANGE → BLANK → DUP` 단일 함수로 정리(가독성) | `test_input_validator_order_ui_ord_01_to_03` | `input_validator.py` | **Boundary** | 02 §2.3 `UI-ORD-01`~`03`와 정합
- [ ] **TASK-024** | **RED** | **L1** | 유효 입력 → `Matrix4x4` **변환** API (Control/Boundary **경계**— Entity는 경계 끝에서만 수신) | `test_from_raw_grid_to_matrix_contract` | `app_service.py` 또는 `matrix_factory.py` | **Control(얇은 어댑터)** 또는 **Boundary** | **Constraint:** Entity에 **raw list** 직접 누수 최소화

**US-001 체크포인트 (Concept-to-Code):** 04.3 AC-1.1~1.4 ↔ 위 Boundary TC ↔ `ErrorContract.code` (02 §2.2) ↔ `INVALID_*` 구현

---

## Phase 2 — US-002: 빈칸 탐지 (Logic · Entity)

- [ ] **TASK-030** | **RED** | **L1** | row-major **빈칸 2곳** 좌표 (02 BL-01~04, 1-based `Cell` 가정) | `test_blank_locator_bl_01_to_04` | `blank_locator.py` | **Entity** | 04.3: `BlankFinder` = 본 `BlankLocator`와 동일 역할
- [ ] **TASK-031** | **GREEN** | **L1** | `BlankLocator.find_blanks` | 동일 | `blank_locator.py` | **Entity** | —
- [ ] **TASK-032** | **RED** | **L3** | 선행 위반: 빈칸 0/1/3개 → `IllegalStateException` (02 BL-05~07) | `test_blank_locator_bl_05_to_07` | `blank_locator.py` | **Entity** | **실패 케이스**—보통은 Boundary가 막으나 Logic 단독 테스트用
- [ ] **TASK-033** | **GREEN** | **L3** | 예외 경로 | 동일 | `blank_locator.py` | **Entity** | —

---

## Phase 3 — US-003: 누락 수·후보 쌍(후보값 정의) (Logic · Entity)

- [ ] **TASK-040** | **RED** | **L1** | 1~16에서 **누락 2수**·`MissingPair(smaller,larger)` (02 MD-01~04) | `test_missing_number_detector_md_01_to_04` | `missing_number_detector.py`, `missing_pair.py` | **Entity** | **후보값 필터링:** 2-빈칸 퍼즐에서 후보는 **딱 이 둘**(순열은 US-005에서 2가지만 시도)
- [ ] **TASK-041** | **GREEN** | **L1** | 구현 | 동일 | `missing_pair.py` | **Entity** | —
- [ ] **TASK-042** | **RED** | **L3** | (선행 위반) 누락≠2 → `IllegalStateException` (02 MD-05) | `test_missing_number_detector_md_05` | `missing_number_detector.py` | **Entity** | 실패 케이스

---

## Phase 4 — US-004: 완성 판정·규칙 (Logic · Entity)

- [ ] **TASK-050** | **RED** | **L1** | 알려진 **완성 4×4** 마방진 `validate()==True` (02 MV-01) | `test_magic_square_validator_mv_01` | `rules.py` / `magic_square_validator.py` | **Entity** | 0이 없는 완성 격자만
- [ ] **TASK-051** | **RED** | **L3** | 행/열/대각/순열 위반 `False` (02 MV-02~06) | `test_magic_square_validator_mv_02_to_06` | `magic_square_validator.py` | **Entity** | **유효/실패** 모두
- [ ] **TASK-052** | **GREEN** | **L1** | `row_sum`/`col_sum`/대각/순열 검사 | 동일 | `magic_square_validator.py` | **Entity** | `MAGIC_SUM`은 constants 참조(매직 넘버 금지)
- [ ] **TASK-053** | **RED** | **L3** | **부분 격자(0 남음)** 는 판정 거부: `False` 또는 예외 (04.3 AC-4.4 — 팀 계약에 맞게 하나로 고정) | `test_validator_rejects_partial_grid` | `magic_square_validator.py` | **Entity** | **체크:** 문서 한 가지로 통일
- [ ] **TASK-054** | **REFACTOR** | **L2** | 보조 합수 함수·이름 정리(Track B 영향 없게 Track A API 유지) | `test_magic_square_validator_mv_07_08` | `magic_square_validator.py` | **Entity** | 02 MV-07~08 경계

---

## Phase 5 — US-005: 두 조합·솔버 (Control · Entity)

**Constraint:** `MagicSquareSolver` = 검증+탐지+조합 **흐름**만; **마방진 정의**는 `MagicSquareValidator` (Control이 규칙을 복붙하지 않음).

- [ ] **TASK-060** | **RED** | **L1** | `CombinationEvaluator`: **조합A** 성공 → `Solution` 6-tuple, **1-based** 좌표 (02 CE-01, INV-10) | `test_combination_evaluator_ce_01` | `combination_evaluator.py`, `solution.py` | **Control** | 04.3 AC-5.1~5.4
- [ ] **TASK-061** | **RED** | **L1** | **조합A 실패·조합B 성공** (02 CE-02) | `test_combination_evaluator_ce_02` | `combination_evaluator.py` | **Control** | **완성 로직** 핵심
- [ ] **TASK-062** | **RED** | **L3** | **둘 다 실패** `NoSolutionException` (02 CE-03) | `test_combination_evaluator_ce_03` | `combination_evaluator.py` | **Control** | 실패 케이스
- [ ] **TASK-063** | **GREEN** | **L2** | 같은 행/대각선 빈칸 등 **엣지** (02 CE-04~05) | `test_combination_evaluator_ce_04_05` | `combination_evaluator.py` | **Control** | —
- [ ] **TASK-064** | **RED** | **L1** | `MagicSquareSolver.solve`: UC-01→02→04 오케스트레이션 (02 MS-01) | `test_magic_square_solver_ms_01` | `magic_square_solver.py` | **Control** | `CombinationEvaluator` 주입
- [ ] **TASK-065** | **RED** | **L1** | 조합B만 해 가능 (02 MS-02) | `test_magic_square_solver_ms_02` | `magic_square_solver.py` | **Control** | —
- [ ] **TASK-066** | **RED** | **L3** | **무해** (02 MS-03) | `test_magic_square_solver_ms_03` | `magic_square_solver.py` | **Control** | —
- [ ] **TASK-067** | **GREEN** | **L1~L3** | 솔버 구현 | `test_magic_square_solver_ms_01_to_03` | `magic_square_solver.py` | **Control** | **체크포인트:** `solve`의 **사전조건**=INV-06,7,8 (02 §1.4) — **입력은 Boundary가 보장**하는 경로와 단위테스트 direct 호출 경로 모두 문서화

---

## Phase 6 — Dual-Track 통합: Boundary + Solver (UI 트랙 + Logic 트랙)

- [ ] **TASK-070** | **RED** | **L1** | Boundary: `MagicSquareSolver` **Mock** — 성공 시 6원소 직렬화 (02 UI-FMT-01~03) | `test_cli_or_handler_success_format` | `result_formatter.py` / `cli.py` | **Boundary** | **UI 트랙** RED
- [ ] **TASK-071** | **RED** | **L3** | Mock이 `NoSolutionException` → `NO_SOLUTION` (02 UI-FMT-04) | `test_cli_no_solution_mapping` | `cli.py` | **Boundary** | 메시지 02 §2.4 고정문구
- [ ] **TASK-072** | **GREEN** | **L1** | 실제 Solver로 **엔투엔** “유효 보드 → 해” | `test_e2e_solve_happy_path` | `main.py` + `cli.py` | **Boundary+Control** | L1
- [ ] **TASK-073** | **RED** | **L3** | **무효 입력**은 Domain 호출 전 **중단** (04.3·02 UI 트랙) | `test_e2e_invalid_stops_before_domain` | `cli.py` | **Boundary** | 스파이로 `solve` **미호출** 검증
- [ ] **TASK-074** | **REFACTOR** | **L0** | ECB 의존 방향 점검: Boundary → Control → Entity, Entity는 Boundary 미참조 | (아키텍처 테스트 또는 import-linter) | 패키지 구조 | **—** | **체크포인트:** 02 §1 Entity 테이블 준수

---

## Phase 7 — NFR: 테스트 커버리지·리팩터 (REFACTOR·L0)

- [ ] **TASK-080** | **RED** | **L0** | `pytest-cov` `fail_under=80` (PRD NFR) | (CI 또는 로컬) | `pyproject.toml` | **—** | **테스트 커버리지 체크포인트 1**
- [ ] **TASK-081** | **REFACTOR** | **L0** | 도메인 패키지 **≥95%** 목표(가능한 서브폴더로 측정) | `coverage` 리포트 | `entity/`, `control/` | **—** | **체크포인트 2 (PRD §8)**
- [ ] **TASK-082** | **REFACTOR** | **L1** | `@pytest.mark.contract` (04.3 힌트) — Boundary+주요 Entity 계약 스위트 | `tests/test_contract_markers` | `pytest` 설정 | **—** | 04.3: 입력 검증만 먼저 GREEN였던 루틴과 alignment
- [ ] **TASK-083** | **GREEN** | **L0** | 중복 `MagicNumber`·`print`·bare `except` 루프 점검(03) | `ruff`/`flake8` | 전체 | **—** | 리팩터 완료 Definition of Done

---

## 추적 표 (To-Do → Scenario → Test → Code)

| US | 대표 To-Do | 시나리오(요지) | 대표 Test | Code (ECB) |
|----|------------|---------------|-----------|------------|
| US-001 | TASK-010~024 | L1 유효 보드 / L3 검증 위반·순서 | `test_input_validator_*`, `test_matrix4x4_*` | `constants`, `Matrix4x4`, `input_validator` (B), 어댑터 (C/B) |
| US-002 | TASK-030~033 | L1 row-major 2빈칸 / L3 잘못된 빈칸 수 | `test_blank_locator_bl_*` | `BlankLocator` (E) |
| US-003 | TASK-040~042 | L1 누락 2수 / L3 비결정 | `test_missing_number_detector_md_*` | `MissingNumberDetector` (E) |
| US-004 | TASK-050~054 | L1 정상 판정 / L3 틀린 합·부분 격자 | `test_magic_square_validator_mv_*` | `MagicSquareValidator` (E) |
| US-005 | TASK-060~067 | L1 순·역 성공 / L3 무해 | `test_combination_evaluator_*`, `test_magic_square_solver_ms_*` | `CombinationEvaluator` (C), `MagicSquareSolver` (C) |
| (Dual) | TASK-070~073 | L1~L3 경계·형식·무해 | `test_cli_*`, `test_e2e_*` | `cli` / `result_formatter` (B) |

---

## Scenario Level 사용 안내 (작업에 이미 기입)

| Level | 의미 | 이 보드에서의 쓰임 |
|-------|------|---------------------|
| **L0** | 기능 개요·인프라·DoD | 스모크, coverage, 품질 게이트 |
| **L1** | 정상 흐름 | Green path, 기본 마방진·기본 퍼즐 |
| **L2** | 경계 | 검증 순서, 인접 빈칸, 리팩터·엣지 |
| **L3** | 실패 | 무효 입력, 무해, IllegalState, Validator False |

---

## Role 분리 (추가 제약 준수)

| 층 | 역할 (이 To-Do 기준) |
|----|------------------------|
| **Entity** | `Matrix4x4`/`Cell`/`MissingPair`/`Solution`, `BlankLocator`, `MissingNumberDetector`, `MagicSquareValidator`, `rules` — **상태·규칙·불변조건** |
| **Control** | `CombinationEvaluator`, `MagicSquareSolver` — **검증된 행렬**에 대해 **탐지→후보→두 조합** **흐름 조율**; 경계/CLI 몰라야 함 |
| **Boundary** | `input_validator`, CLI/핸들러, 포맷터 — **02 입력 스키마**·**에러 직렬화**만; **행/열/마방진 “34” 판정 로직** 없음 |
| **RED / GREEN / REFACTOR** | 작업 ID에 붙은 페이즈마다 1) 실패하는 테스트(RED) 2) 최소 구현(GREEN) 3) 구조/중복 제거(REFACTOR) 순을 유지(동일 US 내에서 뒤섞이면 **시나리오 ID**로 추적) |

이 보드는 **04.3의 US·AC**를 **US-001~005**로 옮기고, **02의 TC ID·에러·검증 순서·이름(BlankLocator 등)** 을 **Test 이름·Code 대상**에 그대로 연결해 두었습니다. 파일로 저장이 필요하면 원하시는 경로(예: `docs/implementation-todo-board.md`)를 지정해 주시면 그에 맞춰 repository에 쓰는 작업도 할 수 있습니다.

---

**User**

Ｔｏ－Ｄｏ　리스트를  포함해 READMD.md 파일을 만들고 싶습니다. 무슨 문서를 참조하면 좋을까요?

---

**Cursor**

`README.md`에 **프로젝트 소개**와 **To-Do(개발 로드맵)** 를 같이 넣을 때는 아래처럼 **역할이 나뉜 문서**를 참조하는 것이 좋습니다.

## README 본문(무엇을 하는 프로젝트인가)

| 참고 문서 | README에서 쓰기 좋은 내용 |
|-----------|---------------------------|
| **`docs/PRD.md`** | 비전·In/Out of Scope·US 요약·NFR·용어·`Report/` 링크 표 |
| **`Report/01-4x4-magic-square-problem-definition.md`** | 문제 정의 한 단락(코드 없이 “왜 이걸 푸는가”) |
| **`Report/04.1-user-journey-epic.md`** (또는 Epic에 해당하는 파일) | Epic·성공 기준의 짧은 인용 |

## 개발자용(실행·구조·계약)

| 참고 문서 | README에서 쓰기 좋은 내용 |
|-----------|---------------------------|
| **`Report/02-4x4-magic-square-tdd-clean-architecture-design.md`** | ECB·에러코드·입력 검증 순서·도메인 컴포넌트 이름·Python/품질 규칙 요지 |
| **`Report/03-cursorrules-setup.md`** | `.cursorrules`/TDD·스타일을 README의 “개발 규칙”에 한 줄로 연결할 때 |

## To-Do 리스트(할 일·우선순위)

| 참고 문서 | README에서 쓰기 좋은 내용 |
|-----------|---------------------------|
| **`Report/04.3-user-journey-stories.md`** | **US-01~05** 순서·AC → README의 **체크리스트/로드맵** 골격 |
| **`docs/PRD.md` §5** | US가 압축 정리되어 있어 **한 페이지 요약**에 적합 |
| (직접 만든 경우) **`docs/implementation-todo-board.md` 등** | 상세 To-Do는 별도 파일로 두고 README에는 **요약 + 링크**만 두는 구성이 가장 읽기 좋음 |

## 한 번에 훑는 용도

| 참고 문서 | 용도 |
|-----------|------|
| **`Report/04-magic-square-user-journey-Levels-1-5-Export-Report.md`** | L1~L5 병합본 — README에 길게 붙이기보다 **“전체 여정은 여기”** 링크용 |

---

**정리:** README는 **`docs/PRD.md`**로 범위·스토리를 잡고, To-Do는 **`Report/04.3-user-journey-stories.md`**(및 PRD §5)를 **정본**으로 두며, 구현·CLI·에러는 **`Report/02`**를 보면 됩니다. 상세 To-Do 보드는 README에 전부 넣지 말고 **별도 Markdown에 두고 README에서 링크**하는 방식을 권장합니다.

---

**User**

README는 **docs/PRD.md**로 범위·스토리를 잡고, To-Do는 Report/04.3-user-journey-stories.md(및 PRD §5)를 정본으로 두며, 구현·CLI·에러는 **Report/02**를 보면 됩니다. 상세 To-Do 보드는 README에 전부 넣지 말고 별도 Markdown에 두고 README에서 링크하는 방식을 권장합니다.
위 내용을 참조해서 To-Do 리스트를 포함한 MagicSquare를 만들기 위한 README.md 파일을 만들어줘.

---

**Cursor**

PRD·04.3·02를 확인한 뒤 `README.md`와 상세 To-Do를 담을 별도 문서를 작성합니다.



프로젝트에 소스 트리가 아직 없어 README는 문서 기준으로 작성하고, 상세 To-Do는 `docs/IMPLEMENTATION-TODO.md`에 둡니다.



다음 두 파일을 추가·정리했습니다.

### 1. [`README.md`](c:\DEV\MagicSquare_07\README.md)
- **프로젝트 한 줄·범위** — `docs/PRD.md`와 맞춤  
- **문서 지도** — PRD, `Report/04.3`, `Report/02`, Epic·Level2·Gherkin·`03` 등  
- **아키텍처 요약** — ECB·Dual-Track (PRD §6·§2.4 링크)  
- **User Story 표** — PRD §5 + 04.3와 동일한 US-01~05  
- **To-Do 체크리스트** — 스토리·Boundary·NFR만 요약  
- **상세 보드 링크** — `docs/IMPLEMENTATION-TODO.md`  
- PRD에 나온 `06-user-journey-stories`와 실제 파일명 **`04.3-user-journey-stories.md`** 가 다를 수 있다는 **주석** 포함  

### 2. [`docs/IMPLEMENTATION-TODO.md`](c:\DEV\MagicSquare_07\docs\IMPLEMENTATION-TODO.md)
- Phase 0 ~ US-01~05 ~ Dual-Track ~ NFR까지 **체크박스**  
- 각 블록마다 **04.3 / PRD / 02** 상대 경로 링크  
- `BlankFinder` vs 02의 `BlankLocator` 등 **이름 대응** 한 줄씩 표기  

저장소에는 아직 `pyproject.toml`/`src`가 없어, README의 **빠른 시작**은 구현 후 채우라는 문구만 두었습니다. 원하면 다음 단계로 `pyproject.toml` 초안과 패키지 디렉터리까지 맞춰 줄 수 있습니다.

---

**User**

@Report/ 폴더에 이 대화에서 작업한 내용을 보고서로 내보내줘.

---

**Cursor**

Report 폴더의 기존 내보내기 문서 형식을 확인한 뒤, 대화에서 수행한 작업을 정리한 보고서를 작성합니다.



기존 `05-docs-prd-export.md` 형식에 맞춰 `Report/06-...` 보고서를 작성합니다.



`Report` 폴더에 아래 보고서를 추가했습니다.

### 생성 파일

**[`Report/06-cursor-session-readme-todo-board-export.md`](c:\DEV\MagicSquare_07\Report\06-cursor-session-readme-todo-board-export.md)**

### 보고서에 넣은 내용

1. **메타** — 2026-04-28, Cursor 대화 기반 문서 작업  
2. **작업 개요** — To-Do 참조 가이드, 아키텍트용 To-Do 보드(채팅 산출), README 질의, `README.md` / `IMPLEMENTATION-TODO.md` 생성  
3. **문서 참조 합의** — PRD, 04.3, 02, Epic/여정, `04.3` 파일명 주의  
4. **저장소 산출물** — `README.md`, `docs/IMPLEMENTATION-TODO.md` 요약  
5. **Epic / US / Phase / Task 구조** — 대화에서 쓴 보드의 **요약** (전체 TASK 표는 스레드 원문 참조로 안내)  
6. **IMPLEMENTATION-TODO vs 상세 TASK 보드** — 역할 구분  
7. **후속 제안** — `pyproject.toml`, 상세 TASK MD 분리, PRD 문서맵 보강 등  
8. **관련 Report** — `05-docs-prd-export`, 04.3, 02와의 관계

형식은 기존 [`Report/05-docs-prd-export.md`](c:\DEV\MagicSquare_07\Report\05-docs-prd-export.md)와 비슷하게 맞춰 두었습니다.

---

**User**

cursor-session이라는 제목은 안넣어 될 것 같은데, 너 생각은 어때?

---

**Cursor**

‘cursor-session’은 도구 이름에 묶여 보이고, 보고서 본질(README·구현 To-Do 내보내기)과 거리가 있습니다. `05-docs-prd-export.md`처럼 **산출물 중심 파일명**이 더 낫습니다. 파일명과 보고서 제목을 바꿉니다.



**생각:** `cursor-session`은 **도구 브랜드**에 묶이고, 나중에 읽는 사람에게는 “무슨 산출물인지”보다 “어디서 돌렸는지”만 떠올리기 쉽습니다. `05-docs-prd-export.md`처럼 **문서·산출물 이름**이 파일명에 드러나는 편이 Report 폴더 맥락과도 잘 맞습니다.

**조치:** 아래로 바꿨습니다.

| 이전 | 이후 |
|------|------|
| `Report/06-cursor-session-readme-todo-board-export.md` | **`Report/06-readme-implementation-todo-export.md`** |

본문도 제목·메타·각주에서 “Cursor”에만 기대지 않도록 **중립적으로** 다듬었습니다(예: “초안 산출”, “상세 보드 초안”, “한 차례의 문서·설계 대화”).

---

**User**

@README.md 파일 중 TO-DO LIST를 작성해줘. 자세하게 생각해서...

---

**Cursor**

README.md의 To-Do 섹션을 슬라이드의 To-Do → Work Order(판단·검증 단위) 관점과 프로젝트 정본(04.3, 02, PRD)에 맞춰 상세히 작성합니다.



슬라이드의 To-Do → Work Order(판단·1:N) 원칙을 반영하고, PRD 범위( GUI 없음·CLI 경계)에 맞춰 `GridUI` 대신 **입력 파싱·결과 직렬화**로 대응합니다.



반영해 두었습니다. 요지만 정리합니다.

### 반영한 생각 (슬라이드 + 이 저장소)

1. **To-Do → Work Order**  
   - **판단(Decision)** 이 있는 일만 “검증 계약”으로 쪼갠다는 문장을 넣었습니다.  
   - **1 : N** — 스토리 하나에 Work Order가 여러 개 붙을 수 있다고 명시했습니다.  
   - **모든 작업 = 테스트**는 아니라고, 리팩터·구조 정리는 강제로 WO에 맞출 필요 없다고 적었습니다.

2. **GUI vs 이 프로젝트**  
   - PRD상 **Web/GUI는 Out of Scope**이므로, 슬라이드의 «격자 UI»는 **CLI/Boundary**의 **입력 수신 + 성공/실패 출력**에 대응한다고 썼습니다.

3. **README 안의 구조**  
   - **TD-1~TD-7** 상위 체크리스트(무엇을 끝낼지).  
   - 각 TD마다 **WO-1.1 …** 식으로 **ECB + 어떤 조건이면 어떤 코드/결과인지** 표로 적었습니다 (02의 에러 순서·`OutputContract`·`NoSolution` 등과 연결).

4. **링크**  
   - 상세 Phase는 기존처럼 `docs/IMPLEMENTATION-TODO.md`로 두고, 내보내기 보고서는 `Report/06-readme-implementation-todo-export.md`로 연결했습니다.

긴 표라 README가 무거워 보이면, 다음 단계로 **TD별 표만 `docs/README-TODO-DETAIL.md`로 옮기고 README에는 원칙 + TD 체크만** 두는 식으로 줄일 수 있습니다. 원하면 그렇게도 정리해 줄게요.

---

**User**

@Report/  폴더에 보고서 업데이트해줘

---

**Cursor**

README에 반영된 **TD- / WO-** 구조·To-Do → Work Order 방법론·보고서 파일명 변경을 `Report/06-readme-implementation-todo-export.md`에 반영합니다.



`Report/06-readme-implementation-todo-export.md`를 현재 저장소 기준으로 맞춰 두었습니다.

### 반영한 내용

1. **메타** — `최초` / `최종 갱신`(README To-Do 보강일), 예전 파일명 `06-cursor-session-…` → `06-readme-implementation-todo-export.md` **이력**
2. **§1 작업 개요** — TD/WO 반영·README 대폭 보강을 **행 5**로 추가, 산출물 설명 정리
3. **§3 산출 파일** — README에 **Traceability·TD·WO 표**가 들어갔다는 설명으로 갱신
4. **§3.1 (신규)** — 슬라이드 **To-Do → Work Order**, **1:N**, **판단 없는 작업**, **GUI → CLI/Boundary**를 표로 요약
5. **§3.2 (신규)** — **TD-1~7** / **WO-x.y** 식별자 규칙·US 매핑
6. **§4** — README의 WO와 대화의 **TASK** 관계(같은 정본, 단위만 다름) 문장 보강
7. **§5** — `README` vs `IMPLEMENTATION-TODO` vs **TASK 전면표(미작성)** 역할 비교
8. **§6 후속** — “README에 TD/WO 반영” 항목은 **[x] 완료**로 표시
9. **오타** — `무염` → `무엇을`, `TD-\**` 깨짐 → `TD-1~7`·`WO-1.1~7.3`로 수정

이제 이 보고서는 **README의 To-Do List(§)** 와 **동일한 용어·범위**로 맞춰져 있습니다.

