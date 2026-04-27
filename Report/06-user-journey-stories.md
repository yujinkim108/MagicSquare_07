# 사용자 여정 — Level 3: User Stories

**작성일:** 2026-04-27  
**상위 문서:** `04-user-journey-epic.md` (Epic) · `05-user-journey-level2.md` (Journey)  
**범위:** Story 1~5 — 사용자 문장(As a / I want / So that), 수용 기준, 관련 Invariant, 담당 컴포넌트, Journey 단계 매핑

---

## 개요

| Story ID | 제목 | 담당 컴포넌트(주) | Journey Step |
|----------|------|-------------------|--------------|
| **US-01** | 입력 검증 | `MagicSquare` / Boundary | Step 2, 5 |
| **US-02** | 빈칸 탐색 | `BlankFinder` | Step 3, 4 |
| **US-03** | 누락 숫자 탐색 | `MissingNumberFinder` | Step 3, 4 |
| **US-04** | 마방진 판정 | `MagicSquareValidator` / `rules` | Step 2~5 |
| **US-05** | 두 조합 시도 | `Solver` (Control) | Step 4, 5 |

---

## Story 1 — 입력 검증 (US-01)

### User Story

**As a** 학습자  
**I want to** 입력이 **정확히 4×4**이고, **빈칸이 정확히 2개**이며, **1~16 범위·중복·타입** 규칙을 만족하는지 검증되길 원한다  
**So that** 잘못된 데이터가 **Domain(엔티티·제어)** 으로 전달되지 않도록 한다

### 맥락

- 이 Story는 **“부분 배치(Partial) 편집 퍼즐”** 계약을 가정한다: 4×4 격자에 `0`은 “아직 정해지지 않은 칸”을 뜻한다.
- **빈칸은 반드시 2개**여야 하며, 그때 **14칸**은 1~16 중 **누락 2개**를 제외한 값으로 채워져 있어야 한다(Story 2·3과 짝).
- **완성(Complete) 마방진** 입력(0 없음)은 **별 User Story/계약**에서 다루거나, `MagicSquare` 생성자에서 `partial` / `complete` 팩토리로 분리한다(§ INV-08).

### Acceptance Criteria

| # | 수용 기준 | 검증 방법(예) |
|---|-----------|---------------|
| AC-1.1 | 격자가 4×4가 **아니면** 예외(`ValueError` 또는 `TypeError` — 타입·구조) | 3×4, `[]`, 비정방 격자 |
| AC-1.2 | 빈칸(`0`)이 **2개가 아니면** 예외 | 0이 0개, 1개, 3개, 16개인 격자 |
| AC-1.3 | **0 외**에 1~16 **밖의 값**이 있으면 예외 | 17, -1 등 |
| AC-1.4 | **0을 제외한 14칸**에 **중복 숫자**가 있으면 예외 | 동일 수 두 번 |
| AC-1.5 | (선택) `0` **이외** 칸이 **0**이면 안 됨 — 0은 빈칸 전용 | 이미 AC-1.2·범위와 겹칠 수 있으면 합쳐 기술 |

**예외 정책(권장):** `ValueError` + 메시지에 위반 유형(크기, 빈칸 개수, 중복, 범위)을 구분.

### 관련 Invariant (Epic)

| ID | 연결 |
|----|------|
| INV-01 | 4×4 |
| INV-02, INV-03 | 1~16(빈칸 제외 시)·중복 없음 — 부분 격자에서는 “0이 아닌 칸”에 대해 |
| INV-08 | **부분 배치**는 완성 규칙과 **이름(계약)**이 다름; 빈칸 2개·빈칸=0는 이 Story의 **명시적 계약** |

### TDD 힌트 (계약 먼저)

1. `tests/entity/test_square.py` (또는 `test_validation.py`)에 `Invariant: INV-01`… 태그.
2. `@pytest.mark.contract` 로 입력 검증만 먼저 RED → 최소 구현으로 GREEN.
3. 구현은 **Entity** `MagicSquare` / 팩터리, 또는 **Boundary+Control** 1차 검사 후 Entity — **프로젝트에 맞는 한 곳**에만 두고 중복 검증을 피한다.

---

## Story 2 — 빈칸 탐색 (US-02)

### User Story

**As a** 학습자  
**I want to** `0`이 들어간 칸의 **좌표를 row-major 순서**로 정확히 얻고 싶다  
**So that** 두 칸에 대해 **조합(순열) 시도**를 안정적으로 할 수 있다

### Acceptance Criteria

| # | 수용 기준 |
|---|-----------|
| AC-2.1 | `0`인 칸의 (row, col) 목록을 **row-major**(행 우선, 열 증가) 순서로 반환한다 |
| AC-2.2 | 반환 개수는 **정확히 2**이다(입력이 US-01을 통과했다는 전제) |
| AC-2.3 | (Story 1과 맞을 때) 빈칸 0·1·3개 등은 **US-01에서** 예외; 본 Story는 “유효한 2빈칸 격자”에 한정 |

### 관련 컴포넌트

- `BlankFinder` (Entity): `find_blanks(grid) -> list[tuple[int, int]]`

### 관련 Invariant

- INV-08(부분 배치 의미) · Story 1과 **동일한 `0` 표기** 전제

---

## Story 3 — 누락 숫자 탐색 (US-03)

### User Story

**As a** 학습자  
**I want to** 격자에 **아직 나타나지 않은 1~16의 숫자 두 개**를 정확히 알고 싶다  
**So that** 그 두 수를 **두 빈칸에 넣는 조합**을 시도할 수 있다

### Acceptance Criteria

| # | 수용 기준 |
|---|-----------|
| AC-3.1 | `0`(빈칸)을 제외한 칸에 등장한 숫자의 집합이 **1~16의 부분집합**이어야 하며, **누락**은 **정확히 2개** |
| AC-3.2 | 누락 2개를 **오름차순** `list[int]` 로 반환한다(예: `[5, 11]`) |
| AC-3.3 | (Story 1) 중복·범위 위반은 입력 단계에서 거절; 본 Story는 “유효 14+2빈칸” 전제에서 결정적(deterministic)으로 동작 |

### 관련 컴포넌트

- `MissingNumberFinder` (Entity): `find_missing(grid) -> list[int]`

### 관련 Invariant

- INV-02, INV-03(부분 격자에서: 0이 아닌 값에 대해)

---

## Story 4 — 마방진 판정 (US-04)

### User Story

**As a** 학습자  
**I want to** **완성된** 4×4 격자(빈칸 없음)에 대해 **정규 마방진(행·열·대각** 합이 모두 `MAGIC_SUM`**)인지**를 판별하고 싶다  
**So that** **Solver**가 **후보를 선택·백트래킹**할 때 “목표에 도달했는가”를 한 함수로 맡길 수 있다

### Acceptance Criteria

| # | 수용 기준 |
|---|-----------|
| AC-4.1 | **4개의 행 합**이 **모두** 동일하다(그때 **Magic Sum** = 4 · (4²+1)/2 = **34** — `constants`에서) |
| AC-4.2 | **4개의 열 합**이 **모두** 동일하다 |
| AC-4.3 | **주대각**·**부대각** 두 대각 합이 **같다**(그리고 **행/열**과 **같은 값**이어야 “마방진”) |
| AC-4.4 | `0`이 **남아 있으면** `False` 또는 `ValueError`(“완성 격자만” 계약) — **사전**에 둔 계약에 따름 |
| AC-4.5 | 1~16 **한 번씩** + 합 조건: Story 1의 **complete** 격자와 연계 시 `True` / `False` 는 **합+집합** 둘 다로 결정(프로젝트가 **합만** 맞을 때 True를 쓰면 INV-03과 모순되므로 **둘 다** 검사 권장) |

### 관련 컴포넌트

- `entity/rules.py` (순수 함수)
- `MagicSquareValidator` / `rules.is_magic_square_complete(grid) -> bool`

### 관련 Invariant

- INV-04, INV-05, INV-06, INV-07, INV-03(완성)

---

## Story 5 — 두 조합 시도 (US-05)

### User Story

**As a** 학습자  
**I want to** **빈칸 2개**에 **누락 2수**를 넣는 **두 가지 정렬(순서) 시도**—작은 수를 **row-major 첫 번째** 빈칸에, 실패 시 **역순**—을 **제한된 탐색**으로 수행하길 원한다  
**So that** “Dual-Track TDD의 **알고리즘 트랙**”에서 **탐색**을 과하지 않으면서 **성공/실패**를 테스트로 고정할 수 있다

### Acceptance Criteria

| # | 수용 기준 |
|---|-----------|
| AC-5.1 | `MissingNumberFinder`의 **오름차순** `missing = [a, b]`(a < b)에 대해, **1차 시도**는 `a` → **첫 번째(row-major) 빈칸**, `b` → **두 번째 빈칸** |
| AC-5.2 | 1차 시도로 **US-04를 만족**하면 그 격자를 **해**로 사용한다 |
| AC-5.3 | 1차가 **실패**하면 **2차 시도**는 **reverse**: `b` → 첫 번째 빈칸, `a` → 두 번째 빈칸 |
| AC-5.4 | **정답(해)** 를 **길이 6의 `list`**, `[r0, c0, v0, r1, c1, v1]`, **row-major 빈칸** 순에 대응(각 (row, col)에 **할당한 값** 기록)으로 표현한다. 해가 없으면 **빈 배열** 또는 `None` 등 **한 가지** 계약에 고정 |
| AC-5.5 | 최대 **2번의 완성 시도**만(순·역); 그 이상 백트래킹/추가 순열은 **이 Story의 범위 밖** (`Solver` 확장 Story로 분리 가능) |

### 이해를 돕는 예 (형식만, 값은 퍼즐에 맞게 바뀜)

- 빈칸: `(0,0)`, `(3,3)`; 누락: `3, 7`
- 1차: (0,0)←3, (3,3)←7 → `is_magic`?
- 2차: (0,0)←7, (3,3)←3 → `is_magic`?
- 둘 중 **처음** 만족하는 쪽의 **6원소** 벡터가 “정답 배열”

### 관련 컴포넌트

- `Solver` (Control): `try_two_combinations(grid) -> list[int]` (또는 `tuple[...] | None` — **길이 0 vs None** 팀에서 통일)
- `MagicSquareValidator` / `rules` — 완성 검사

### 관련 Invariant

- INV-03~07(완성), INV-08(2빈칸 부분)

---

## Story 의존성(권장 순서)

```text
US-01(입력 검증)
  → US-02(빈칸) — 병행 가능 US-01 GREEN 후
  → US-03(누락) — US-01 GREEN 후
  → US-04(판정) — `constants` + `rules` (완성 격자) 먼저
  → US-05(두 조합) — US-02, US-03, US-04에 의존
```

---

## 수용 기준 — 추적(요약)

| AC 그룹 | Invariant (대표) |
|---------|-----------------|
| Story 1 | INV-01, INV-02, INV-03(부분), + **“빈칸 2개”** 명시 계약 |
| Story 2, 3 | INV-08, INV-02/03 |
| Story 4 | INV-04~07, INV-03(완성) |
| Story 5 | INV-03~07(완성), INV-08(부분→완성) |

---

## 다음 문서 (Level 4: Technical 시나리오, Task, 선택)

- **Gherkin / BDD 구현 시나리오:** `08-level4-implementation-scenario-technical.md`
- 세부 **Task(작업 쪼개기)**·테스트 케이스 ID: `07-user-journey-tasks.md` (없으면 생성)

---

*본 문서는 사용자 여정 Level 3 (User Stories) 산출물이며, Epic `04`·Journey `05`와 함께 읽는다.*
