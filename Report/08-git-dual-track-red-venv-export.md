# 08 · Git 전략·develop·Dual-Track RED 설계·실행 환경 내보내기

**최초:** 2026-04-28  
**최종 갱신:** 2026-04-28 (pytest RED 스켈레톤·실행 결과·§7·§8 정렬)  
**작업 유형:** **문서·저장소 작업** — 브랜치 전략 정리, `develop` 생성·원격 반영, Dual-Track UI/Logic **RED 테스트 설계** 기록, **pytest RED 스켈레톤(파일·클래스·`pytest.fail`)**·JUnit 5 **참고 스켈레톤**, 로컬 **pytest 실행** 결과, **가상환경 실행 방법** 정리  
**워크스페이스:** `c:\DEV\MagicSquare_07` (MagicSquare_07)

**관련 보고서:** [`07-test-case-specification-export.md`](./07-test-case-specification-export.md) (TC 명세 이미지→표), [`06-readme-implementation-todo-export.md`](./06-readme-implementation-todo-export.md) (README·TD/WO 보드)

---

## 1. 작업 개요

| # | 내용 | 결과 |
|---|------|------|
| 1 | **Git 브랜치 전략** (Dual-Track TDD, RED → GREEN → Dual-Track Refactor 순서와 정렬) | 본 보고서 §2 — `main` + `feature/us-XX-…`, 커밋 규칙 `test`(RED) → `feat`(GREEN) → `refactor` |
| 2 | **`develop` 브랜치** 생성·`origin` 푸시, 문서 커밋 반영 | `develop` = `red`와 동일 시점 커밋에서 생성; 원격 `https://github.com/yujinkim108/MagicSquare_07`에 `develop` 존재 |
| 3 | **Dual-Track RED** (구현·GREEN·REFACTOR 없음) — UI/Boundary 6건 + Logic 4그룹 설계 | 본 보고서 §4 — Test ID·시나리오·Invariant |
| 4 | **pytest RED 스켈레톤** — Dual-Track에 맞춘 `test_*.py` / `Test*` 클래스, 본문은 `pytest.fail("RED: not implemented")` 한 줄 | 본 보고서 §4.3, §7 — `pytest.ini` + `tests/boundary`·`tests/logic` |
| 5 | **JUnit 5** (참고) — 프레임워크 명명만 동일 ID로 맞춘 `.java` 스켈레톤, 빌드 미연결 | `docs/test-skeletons/junit5/*.java` (§7) |
| 6 | **`pytest` 실행** | venv + `pip install pytest` 후 `python -m pytest` → **10 failed** (의도적 RED) (§5) |
| 7 | **가상환경에서 실행** 절차 (Windows PowerShell) | 본 보고서 §6 |

**도메인·Boundary 구현 코드**(`entity` / `control` / `boundary` 패키지)는 **아직 없음**. **RED 테스트 스켈레톤만** 추가되어 GREEN 이전 단계를 고정한다.

---

## 2. Git 브랜치 전략 (요약)

| 항목 | 권장 |
|------|------|
| **trunk** | `main` — CI 통과 기준선, PR로 병합 |
| **통합 브랜치** | `develop` — 진행 중 작업 통합(본 저장소에 생성됨) |
| **기능 브랜치** | `feature/us-01-input-validation` 등 **US·TD 단위**; Work Order가 크면 `feature/us-01-wo-1-…` |
| **Dual-Track과의 대응** | 브랜치를 UI/Logic으로 쪼개기보다 **같은 feature 안**에서 커밋으로 트랙 구분 |
| **커밋 순서** | `test` (UI RED) → `test` (Logic RED) → `feat` (GREEN) → `refactor` (Dual-Track 리팩터) |
| **PR** | 본문에 UI/Logic RED·GREEN·Refactor 체크, 계약(`Report/02`) 변동 명시 |

---

## 3. 저장소·원격 상태 (이 세션 기준)

| 항목 | 내용 |
|------|------|
| **원격** | `origin` → `https://github.com/yujinkim108/MagicSquare_07.git` |
| **브랜치** | `main`, `red`, `develop` (로컬·원격 `develop` 생성·푸시) |
| **문서 커밋(예시)** | 테스트 케이스 정본 `docs/TEST-CASE-SPECIFICATION.md` 이동, `Report/07-test-case-specification-export.md`, `Prompting/07-test-case-specification-export-prompt.md` 반영 |

**PR 링크(참고):** `https://github.com/yujinkim108/MagicSquare_07/pull/new/develop`

---

## 4. Dual-Track RED 테스트 설계 (구현 없음)

개발 방법론: **Dual-Track UI + Logic TDD** — 본 절은 **RED만**; GREEN·REFACTOR는 범위 밖.

**프로젝트 조건(알려진 계약):** 입력 `4x4 int[][]`, `0` = 빈칸·정확히 2개, 값 `1~16`, 0 제외 중복 없음. 출력 `int[6]`, 좌표 1-index `[r1,c1,n1,r2,c2,n2]`. 4×4 magic sum **34**.

### 4.1 Track A — UI / Boundary RED

| Test ID | Scenario(요지) | Invariant / 보호 계약 |
|---------|----------------|------------------------|
| **UI-RED-01** | 4×4가 아닌 입력 → 예외 | 입력 크기·형태: 항상 4×4 |
| **UI-RED-02** | 빈칸(`0`) 개수 ≠ 2 → 예외 | 정확히 두 빈칸 전제 |
| **UI-RED-03** | 0이 아닌 셀 값이 범위 위반 → 예외 | 비어 있지 않은 셀 ∈ 1~16 |
| **UI-RED-04** | 0 제외 중복 → 예외 | 1~16 각각 한 번(부분 격자) |
| **UI-RED-05** | 성공 응답(또는 직렬화) 배열 길이 6 | 출력 스키마 `[r1,c1,n1,r2,c2,n2]` |
| **UI-RED-06** | 성공 시 좌표 1-index(1~4) | UI·CLI·문구와 동일한 좌표 체계 |

### 4.2 Track B — Logic RED

| Test ID | Scenario(요지) | Invariant / 보호 계약 |
|---------|----------------|------------------------|
| **LOGIC-RED-01** | `find_blank_coords()` — `0` 위치 2개, **row-major** | US-02 빈칸 순서 |
| **LOGIC-RED-02** | `find_not_exist_nums()` — 1~16 중 누락 2개, **오름차순** | US-03 |
| **LOGIC-RED-03** | `is_magic_square()` — 행·열·대각 합 동일, **34** | US-04, magic sum |
| **LOGIC-RED-04** | `solution()` — 작은 누락→첫 빈칸·큰 누락→둘째 빈칸 우선, 실패 시 **reverse**, 길이 6·1-index | US-05, 최대 2시도 |

각 항목은 **구현 부재 시 의도적으로 실패(RED)** 해야 하며, 이후 GREEN에서만 통과로 바꾼다.

### 4.3 pytest 스켈레톤 ↔ Test ID (프레임워크 명명)

| Test ID (§4.1·§4.2) | pytest 모듈 | 클래스 | 메서드 (`test_*`) |
|----------------------|-------------|--------|-------------------|
| UI-RED-01 .. 06 | `tests/boundary/test_ui_boundary_red.py` | `TestUiBoundaryRed` | `test_ui_red_01_not_4x4_raises` … `test_ui_red_06_success_coordinates_are_one_indexed` |
| LOGIC-RED-01 .. 04 | `tests/logic/test_logic_red.py` | `TestLogicRed` | `test_logic_red_01_find_blank_coords_row_major_two_cells` … `test_logic_red_04_solution_small_first_blank_then_reverse_six_tuple_one_based` |

- 수집 규칙: 루트 `pytest.ini` — `testpaths = tests`, `python_files = test_*.py`, `python_classes = Test*`, `python_functions = test_*`.

---

## 5. 테스트 실행 (로컬)

| 항목 | 결과 |
|------|------|
| **이전(초기)** | `*.py`·`tests/` 없음, `pytest` 미설치 → 실행 불가 |
| **현재** | `pytest.ini`, `tests/boundary/`, `tests/logic/` 추가 |
| **의존성** | `pyproject.toml` 없이도 `pip install pytest` 만으로 실행 가능 |
| **실행 예** | `python -m pytest` 또는 `python -m pytest tests -q` |
| **기대** | **10 failed** — 각 테스트가 `pytest.fail("RED: not implemented")` 로 **의도적 RED** (구현·Assertion 교체 시 GREEN으로 이행) |

**결론:** **가상환경**에서 `pytest` 설치 후(§6) 루트에서 실행하면 스켈레톤이 **전부 실패(RED)** 하는지 확인할 수 있다.

---

## 6. 가상환경에서 실행하는 방법 (Windows·PowerShell)

| 단계 | 명령(예) |
|------|----------|
| 1. 프로젝트 이동 | `cd C:\DEV\MagicSquare_07` |
| 2. venv 생성 | `python -m venv .venv` (또는 `py -3.10 -m venv .venv`) |
| 3. 활성화 | `.\.venv\Scripts\Activate.ps1` |
| 4. pip 갱신 | `python -m pip install --upgrade pip` |
| 5. `pytest` 설치 (현재) | `pip install pytest` (또는 향후 `pyproject.toml`의 `[project.optional-dependencies] dev`에 정의 시 `pip install -e ".[dev]"`) |
| 6. 테스트 | `python -m pytest` (RED 스켈레톤 10건 **실패**가 정상) |
| 7. 비활성화 | `deactivate` |

**참고:** `Activate.ps1` 실행 정책 오류 시 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` (사용자 환경에 한함).

---

## 7. 산출·갱신 파일 (본 내보내기)

| 경로 | 설명 |
|------|------|
| **`Report/08-git-dual-track-red-venv-export.md`** | **본 문서** — Git·develop·RED 설계·pytest·venv 감사 추적 |
| **`pytest.ini`** | `testpaths = tests`, pytest 수집 규칙 |
| **`tests/boundary/test_ui_boundary_red.py`** | `TestUiBoundaryRed` — UI-RED-01~06 (RED) |
| **`tests/logic/test_logic_red.py`** | `TestLogicRed` — LOGIC-RED-01~04 (RED) |
| **`tests/boundary/__init__.py`**, **`tests/logic/__init__.py`** | 패키지 구분(선택) |
| **`docs/test-skeletons/junit5/UiBoundaryRedTest.java`** | JUnit 5 **참고** — `UiBoundaryRedTest`, `fail("RED: not implemented")` |
| **`docs/test-skeletons/junit5/LogicRedTest.java`** | JUnit 5 **참고** — `LogicRedTest` (Gradle/Maven **미연결**) |

`docs/TEST-CASE-SPECIFICATION.md`·`docs/PRD.md`·`Report/02-…`·`Report/04.3-…` 는 **요구·TC·설계 정본**으로, 본 보고서는 **2026-04-28 세션의 작업 이력**에 해당한다.

---

## 8. 권장 다음 작업 (참고)

- [x] §4 Test ID에 대응하는 **RED 스켈레톤** `tests/` (`pytest.fail`, §4.3) — 2026-04-28 갱신
- [ ] Phase 0: `pyproject.toml`(선택)에서 `dev`에 `pytest`·포매터·린터·커버리지 고정; **`entity` / `control` / `boundary`** 소스 패키지 골대
- [ ] GREEN: §4.3 메서드에서 `pytest.fail` 제거 후 실제 호출·Assertion으로 교체(구현은 Boundary / Entity `Report/02` 정본에 맞게)
- [ ] Dual-Track **REFACTOR** (계약·테스트 유지)
- [ ] `main` ↔ `develop` 병합 정책·PR 템플릿 합의

---

*끝.*
