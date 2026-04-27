# Magic Square — 사용자 여정·구현 시나리오 보고서 (Level 1~5 통합 내보내기)

**보고서 유형:** Work package 내보내기 (싱글 파일)  
**작성(병합)일:** 2026-04-27  
**경로:** `Report/04-magic-square-user-journey-Levels-1-5-Export-Report.md`  
**범위:** Invariant·Epic, Journey(5 Step), User Stories(US-01~05), Gherkin·Technical, 시나리오 검증

---

## 머리말: 목적과 사용

- **목적:** Level 1(Epic)부터 Level 5(검증)까지, 생산한 산출물을 **하나의 Markdown**으로 아카이브·제출·인쇄에 쓴다.
- **원본:** 아래 *부록*에 각 `Report/*.md` **전문**을 2026-04-27 기준으로 합쳤다. **개별 문서**가 *source of truth*이며, 본 파일은 *스냅샷*이다.
- **관련(본 보고에 미포함):** `01-4x4-magic-square-problem-definition.md`, `02-4x4-magic-square-tdd-clean-architecture-design.md`, `03-cursorrules-setup.md`.

## 요약: 문서·레벨 map

| Level | 파일명(원본) | 다루는 것 |
|------|----------------|------------|
| 1 | `04-user-journey-epic.md` | Epic, Invariant(INV-01~10), 성공 기준, ECB 책임 |
| 2 | `05-user-journey-level2.md` | Persona, Step 1~5, Pitfall, Dual-Track, 회귀 |
| 3 | `06-user-journey-stories.md` | US-01~05, AC, 컴포넌트 |
| 4 | `08-level4-implementation-scenario-technical.md` | Gherkin Feature, 시나리오, 기술 약속, 검산 메모 |
| 5 | `09-level5-scenario-verification.md` | 일관성·엣지·구현가능·갭, Sign-off |

> **Note:** `07-user-journey-tasks.md`는 선택 Task일 뿐이며, `05` 하단 T-01~T-09와 연동될 수 있다.

## 부록: 원문 전체 (순서대로)



---

<!-- SNAPSHOT FROM: 04-user-journey-epic.md -->

# 사용자 여정 — Level 1: Epic (비즈니스 목표)

**작성일:** 2026-04-27  
**범위:** Epic 정의, 목적, 성공 기준, Invariant 목록, 추적 구조

---

## EPIC — Business Goal

### Epic: "Invariant(불변조건) 기반 사고 훈련 시스템 구축"

---

## 1. 목적

4×4 Magic Square 문제를 활용하여 다음 네 가지 역량을 체계적으로 훈련한다.

| # | 훈련 영역 | 핵심 질문 |
|---|-----------|-----------|
| 1 | **Invariant 중심 설계 사고** | "이 규칙은 언제, 누가, 어느 범위에서 반드시 참인가?" |
| 2 | **Dual-Track TDD 적용** | "계약(Contract) 테스트와 알고리즘 테스트를 어떻게 분리하는가?" |
| 3 | **입력/출력 계약 명확화** | "함수의 사전조건·사후조건·불변조건이 테스트로 표현되어 있는가?" |
| 4 | **설계 → 테스트 → 구현 → 리팩토링 흐름 체화** | "RED를 보기 전에 구현한 코드가 없는가?" |

---

## 2. 배경 및 맥락

### 왜 4×4 Magic Square인가

- **880가지 본질해(Essentially Different Solutions):** 3×3(1가지)보다 탐색·설계 결정이 의미를 가지며, 5×5 이상처럼 해 공간이 폭발하지 않는다.
- **동시 제약(Simultaneous Constraints):** 4행 + 4열 + 2대각선 = 10개의 합 조건이 독립이 아닌 채로 동시 충족되어야 한다. **여러 Invariant가 얽힌 시스템**을 다루는 연습에 최적이다.
- **검증 가능성:** 정답이 명확(Magic Sum = 34)하여 테스트 작성 후 **즉각 피드백**이 가능하다.

### Dual-Track TDD란

```
Track A — Contract Tests (계약 테스트)
  : 입력 조건(사전조건)과 출력 조건(사후조건)이 Invariant와 일치하는지 검증
  : 구현 알고리즘이 바뀌어도 계약 테스트는 항상 GREEN이어야 한다

Track B — Algorithm Tests (알고리즘 테스트)
  : 특정 구현 전략(백트래킹, CSP 등)의 동작을 단계별로 검증
  : 리팩토링 시 삭제·수정 대상이 될 수 있음
```

두 트랙을 분리하면 **"계약을 깨지 않고 내부를 바꾼다"** 는 리팩토링의 안전망이 명확해진다.

---

## 3. 범위(Scope)

### In Scope

- 4×4 Magic Square 도메인 엔티티(Entity) 및 불변조건 정의
- 입력 검증(Validation) 계약 — 사전조건 테스트
- 마방진 판정기(Validator) — 사후조건 테스트
- 마방진 생성기(Generator) — 알고리즘 테스트
- ECB 레이어(Boundary / Control / Entity) 전체 구현
- CLI 경계(Boundary) — 입출력 인터페이스
- 80% 이상 테스트 커버리지(도메인 로직 95% 목표)

### Out of Scope

- GUI / Web UI
- 데이터베이스 영속성(Persistence)
- 5×5 이상 Magic Square
- 분산·비동기 처리

---

## 4. 핵심 Invariant 목록

> Invariant는 **"언제나 참이어야 하는 조건"** 이다.
> 각 Invariant는 반드시 하나 이상의 테스트와 1:1로 추적 가능해야 한다.

| ID | Invariant | 적용 범위 | 위반 시 결과 |
|----|-----------|-----------|-------------|
| **INV-01** | 격자는 정확히 4×4 = 16칸이다 | 전체 생애주기 | `ValueError` |
| **INV-02** | 숫자는 1 이상 16 이하의 정수만 허용된다 | 전체 생애주기 | `ValueError` |
| **INV-03** | 16개 숫자는 중복 없이 정확히 한 번씩 등장한다 | 완성(Complete) 상태 | `ValueError` |
| **INV-04** | Magic Sum = 34 (= 4 × (4² + 1) / 2) | 완성(Complete) 상태 | 검증 실패 |
| **INV-05** | 4개의 행 합이 모두 34이다 | 완성(Complete) 상태 | 검증 실패 |
| **INV-06** | 4개의 열 합이 모두 34이다 | 완성(Complete) 상태 | 검증 실패 |
| **INV-07** | 2개의 대각선 합이 모두 34이다 | 완성(Complete) 상태 | 검증 실패 |
| **INV-08** | 부분 배치(Partial)는 완성 규칙과 이름(계약)이 달라야 한다 | 탐색(Search) 상태 | 설계 위반 |
| **INV-09** | Magic Sum 상수는 코드에 하드코딩하지 않는다 | 구현 전체 | 규칙 위반 |
| **INV-10** | Invariant → Test 추적 링크가 모든 검증 코드에 존재한다 | 테스트 스위트 전체 | 추적 불가 |

---

## 5. 성공 기준

| 기준 | 목표값 | 측정 방법 |
|------|--------|-----------|
| Domain Logic 테스트 커버리지 | **95% 이상** | `pytest --cov=magic_square/entity --cov=magic_square/control` |
| 입력 검증 계약 테스트 통과율 | **100%** | Contract Test 전용 마커(`@pytest.mark.contract`) 실행 |
| 하드코딩 상수 | **0건** | `entity/constants.py` 외 매직 넘버 부재 |
| 매직 넘버 | **0건** | 코드 리뷰 + linter 검사 |
| Invariant → Test 추적 가능성 | **INV-01~10 전부** | 테스트 docstring 내 `Invariant: INV-XX` 태그 존재 |

---

## 6. Invariant → Test 추적 구조

각 테스트 함수는 다음 docstring 형식으로 Invariant를 명시한다.

```python
def test_grid_must_be_4x4():
    """
    Invariant: INV-01
    격자가 4×4가 아닐 경우 ValueError를 발생시킨다.
    """
    # Arrange
    invalid_grid = [[1, 2], [3, 4]]
    # Act / Assert
    with pytest.raises(ValueError):
        MagicSquare(invalid_grid)
```

추적 매트릭스는 `tests/` 디렉터리 내 `conftest.py` 또는 별도 `TRACEABILITY.md`로 관리한다.

---

## 7. ECB 레이어별 Epic 책임

```
Boundary (경계)
  └─ CLI 입력 파싱 및 1차 유효성 검사 (INV-01, INV-02)
  └─ 결과 포맷 출력

Control (제어)
  └─ 생성 유스케이스: GeneratorController (INV-03~07)
  └─ 검증 유스케이스: ValidatorController (INV-04~07)
  └─ 탐색 상태·완성 상태 흐름 조율 (INV-08)

Entity (도메인)
  └─ MagicSquare 값 객체: 도메인 불변식 보관 (INV-01~08)
  └─ constants.py: GRID_SIZE = 4, MAGIC_SUM = 34, NUMBER_RANGE = range(1, 17) (INV-09)
  └─ rules.py: 합 조건 순수 함수 (INV-04~07)
```

---

## 8. 다음 단계 (Level 2: User Story)

이 Epic은 다음 User Story로 분해된다.

| Story ID | 제목 | 담당 레이어 |
|----------|------|-------------|
| US-01 | Invariant를 상수와 값 객체로 표현한다 | Entity |
| US-02 | 완성된 배치가 마방진인지 판정한다 | Entity / Control |
| US-03 | 마방진 배치를 자동으로 생성한다 | Control |
| US-04 | 잘못된 입력을 거부하는 계약을 정의한다 | Entity / Boundary |
| US-05 | CLI로 마방진을 생성하고 결과를 확인한다 | Boundary |

> User Story 상세는 `06-user-journey-stories.md`에서 작성한다.

---

*본 문서는 사용자 여정 Level 1 (Epic) 산출물이며, Level 2 (User Story) 및 Level 3 (Task) 작업은 별도 문서에서 이어진다.*


---

<!-- SNAPSHOT FROM: 05-user-journey-level2.md -->

# 사용자 여정 — Level 2: User Journey (사용자 여정)

**작성일:** 2026-04-27  
**상위 문서:** `04-user-journey-epic.md` — Epic: "Invariant 기반 사고 훈련 시스템 구축"  
**범위:** Persona 정의, Step 1~5 여정 상세, 각 Step의 출입 조건·산출물·함정

---

## Persona

| 항목 | 내용 |
|------|------|
| **역할** | 소프트웨어 개발 학습자 |
| **현재 상태** | TDD 훈련 중 / Clean Architecture(ECB) 이해 중 |
| **핵심 불안** | "테스트를 먼저 짜야 한다는 건 알겠는데, 무엇을 테스트해야 하는지 모르겠다" |
| **핵심 목표** | 설계 → 테스트 → 구현 → 리팩토링 흐름을 **몸으로** 익힌다 |
| **성공 신호** | Invariant를 먼저 찾고, 그것이 테스트로 표현되며, 구현이 나중에 따라오는 순서가 자연스러워진다 |

---

## Journey Overview

```
Step 1 ─ 문제 인식          : "무엇을 만드는가"가 아니라 "무엇이 항상 참인가"를 먼저 묻는다
Step 2 ─ 계약 정의          : 입력·출력·예외를 코드 전에 문서로 고정한다
Step 3 ─ Domain 분리        : 역할별 컴포넌트로 책임을 나눈다
Step 4 ─ Dual-Track 진행    : UI와 Logic을 병렬 RED로 출발, 독립적으로 GREEN·REFACTOR
Step 5 ─ 회귀 보호          : 엣지·오류·조합 실패 케이스로 안전망을 완성한다
```

---

## Step 1 — 문제 인식

### 핵심 전환

> "마방진을 구현한다"가 아니라,  
> **"마방진이 마방진이기 위해 언제나 참이어야 하는 것은 무엇인가"** 를 먼저 묻는다.

### 왜 이 전환이 필요한가

| 잘못된 출발점 | 올바른 출발점 |
|---------------|---------------|
| "4×4 격자에 1~16을 채운다" | "16칸에 1~16이 중복 없이 들어가야 한다 (INV-03)" |
| "행·열·대각을 같게 만든다" | "10개의 합 조건이 모두 34여야 한다 (INV-04~07)" |
| "알고리즘을 설계한다" | "Invariant가 먼저, 알고리즘은 그것을 만족시키는 수단이다" |

### 이 단계의 산출물

- [ ] Invariant 목록 (INV-01~10) 초안 작성 → `04-user-journey-epic.md § 4` 참조
- [ ] "완성(Complete) 상태"와 "부분(Partial) 상태"의 이름·계약 분리 결정 (INV-08)
- [ ] Magic Sum 공식 확인: `MAGIC_SUM = GRID_SIZE * (GRID_SIZE ** 2 + 1) // 2` (INV-09)

### 입장 조건 (Entry Condition)

- 없음 — 이 Step이 여정의 시작점이다.

### 완료 조건 (Exit Condition)

- Invariant 목록이 문서화되어 있다.
- "구현"보다 "계약"이 먼저라는 사고 전환이 완료됐다.
- 코드가 단 한 줄도 없는 상태에서 다음 Step으로 넘어간다.

### 함정 (Pitfall)

> **함정:** "일단 코드를 짜고 테스트를 나중에 추가한다."  
> **결과:** 테스트가 구현을 검증하는 게 아니라 구현을 설명하는 문서가 된다. Invariant가 누락되어도 발견되지 않는다.

---

## Step 2 — 계약 정의

### 핵심 원칙

> 구현이 시작되기 전에 **입력 스키마, 출력 스키마, 예외 정책**을 고정한다.  
> 계약이 흐리면 RED가 의미를 잃는다.

### 2-1. 입력 스키마 정의

| 항목 | 타입 | 제약 | 관련 Invariant |
|------|------|------|----------------|
| `grid` | `list[list[int]]` | 외부 행 4개, 내부 열 4개 | INV-01 |
| 각 원소 | `int` | `1 ≤ value ≤ 16` | INV-02 |
| 전체 원소 집합 | `set[int]` | `{1, 2, …, 16}` (완성 상태) | INV-03 |

```python
# 유효한 입력 예시
grid: list[list[int]] = [
    [ 1,  2, 15, 16],
    [12, 14,  3,  5],
    [13,  7, 10,  4],
    [ 8, 11,  6,  9],
]

# 무효한 입력 예시 — 계약 위반 유형
grid_wrong_size   = [[1, 2], [3, 4]]          # INV-01 위반: 2×2
grid_out_of_range = [[0, 2, 3, ...], ...]      # INV-02 위반: 0 포함
grid_duplicate    = [[1, 1, 2, 3], ...]        # INV-03 위반: 중복
```

### 2-2. 출력 스키마 정의

| 컴포넌트 | 함수 | 반환 타입 | 의미 |
|----------|------|-----------|------|
| `MagicSquareValidator` | `is_valid(grid)` | `bool` | 완성 마방진 여부 |
| `BlankFinder` | `find_blanks(grid)` | `list[tuple[int, int]]` | 빈 칸 좌표 목록 |
| `MissingNumberFinder` | `find_missing(grid)` | `list[int]` | 미사용 숫자 목록 |
| `Solver` | `solve(grid)` | `list[list[int]] \| None` | 완성 배치 또는 해 없음 |

### 2-3. 예외 정책 정의

| 위반 상황 | 예외 타입 | 발생 시점 | 메시지 형식 |
|-----------|-----------|-----------|-------------|
| 격자 크기 불일치 | `ValueError` | 객체 생성 시 | `"Grid must be 4×4, got {rows}×{cols}"` |
| 범위 초과 값 | `ValueError` | 객체 생성 시 | `"Values must be in 1..16, got {invalid}"` |
| 중복 값 존재 | `ValueError` | 완성 검증 시 | `"Duplicate values found: {duplicates}"` |
| 타입 불일치 | `TypeError` | 객체 생성 시 | `"Expected list[list[int]], got {type}"` |

> **원칙:** 예외는 `except Exception` 으로 묵살하지 않는다. 구체적 예외만 처리한다 (`.cursorrules` forbidden 규칙).

### 이 단계의 산출물

- [ ] 입력 스키마 문서 (이 문서 § 2-1)
- [ ] 출력 스키마 문서 (이 문서 § 2-2)
- [ ] 예외 정책 표 (이 단계 § 2-3)
- [ ] `entity/constants.py` 상수 목록 초안

### 완료 조건 (Exit Condition)

- 모든 공개 함수의 시그니처와 반환 타입이 문서로 확정됐다.
- 예외 발생 조건이 Invariant ID와 연결됐다.
- 코드가 단 한 줄도 없다.

### 함정 (Pitfall)

> **함정:** "일단 만들고 계약은 나중에 정한다."  
> **결과:** 계약이 구현에 종속된다. 리팩토링 시 "무엇을 지켜야 하는지"를 알 수 없어진다.

---

## Step 3 — Domain 분리

### 핵심 원칙

> 하나의 클래스에 "찾기 + 검증 + 탐색"을 섞지 않는다.  
> **단일 책임(Single Responsibility)** 으로 쪼개면, 각 컴포넌트를 독립적으로 테스트할 수 있다.

### 컴포넌트 책임 정의

#### BlankFinder
```
책임  : 격자에서 빈 칸(미결정 위치)을 찾는다
입력  : 부분 배치 grid (0 또는 None 으로 빈 칸 표시)
출력  : list[tuple[int, int]] — 빈 칸의 (row, col) 좌표 목록
레이어: Entity
Invariant: INV-08 (부분 배치의 계약은 완성과 분리)
```

#### MissingNumberFinder
```
책임  : 격자에서 아직 사용되지 않은 숫자를 찾는다
입력  : 부분 배치 grid
출력  : list[int] — 1~16 중 미사용 숫자 목록 (정렬)
레이어: Entity
Invariant: INV-02, INV-03
```

#### MagicSquareValidator
```
책임  : 완성된 격자가 마방진 조건을 모두 만족하는지 판정한다
입력  : 완성 배치 grid (16칸 모두 채워진 상태)
출력  : bool
레이어: Entity / Control 경계
Invariant: INV-04, INV-05, INV-06, INV-07
```

#### Solver
```
책임  : 부분 배치를 받아 마방진 조건을 만족하는 완성 배치를 탐색한다
입력  : 부분 또는 빈 grid
출력  : list[list[int]] | None
레이어: Control
Invariant: INV-03~07 (탐색 과정에서 BlankFinder·MissingNumberFinder·Validator 활용)
```

### ECB 레이어 배치

```
Entity (도메인 순수 함수)
  ├── BlankFinder          ← 부분 배치 상태 질의
  ├── MissingNumberFinder  ← 숫자 집합 상태 질의
  ├── MagicSquareValidator ← 완성 배치 판정
  └── constants.py / rules.py

Control (유스케이스 조율)
  └── Solver               ← BlankFinder + MissingNumberFinder + Validator 조합

Boundary (입출력)
  └── CLI                  ← Solver 결과를 사람이 읽을 수 있게 출력
```

### 의존성 방향 검증

```
Solver (Control)
  → MagicSquareValidator (Entity)  ✔ 허용
  → BlankFinder (Entity)           ✔ 허용
  → MissingNumberFinder (Entity)   ✔ 허용

MagicSquareValidator (Entity)
  → Solver (Control)               ✘ 금지 (역방향)
  → CLI (Boundary)                 ✘ 금지 (역방향)
```

### 이 단계의 산출물

- [ ] 4개 컴포넌트의 책임·입출력·레이어가 문서로 확정됐다
- [ ] 의존성 방향이 `boundary → control → entity` 를 지킨다
- [ ] 각 컴포넌트가 독립적으로 인스턴스화 가능한 구조임을 설계로 보인다
- [ ] 아직 코드 없음

### 함정 (Pitfall)

> **함정:** `MagicSquareValidator` 안에서 `Solver`를 호출한다.  
> **결과:** Entity → Control 역방향 의존이 발생하고, Validator 단독 테스트가 불가능해진다.

---

## Step 4 — Dual-Track 진행

### 핵심 원칙

> UI 계약(Boundary)과 Domain Logic(Entity/Control)의 RED는 **동시에 출발**할 수 있다.  
> 두 트랙은 서로의 구현을 기다리지 않는다.

### Track A — Contract Track (계약 테스트)

```
목표  : 입력·출력·예외 계약이 Invariant와 일치하는지 검증
특성  : 알고리즘이 바뀌어도 이 트랙은 항상 GREEN이어야 한다
마커  : @pytest.mark.contract
위치  : tests/entity/, tests/boundary/
```

**RED 예시 — 계약 테스트 (아직 구현 없음)**

```python
@pytest.mark.contract
def test_validator_rejects_grid_smaller_than_4x4():
    """
    Invariant: INV-01
    격자가 4×4 미만이면 ValueError를 발생시킨다.
    """
    # Arrange
    small_grid = [[1, 2], [3, 4]]
    # Act / Assert
    with pytest.raises(ValueError, match="4×4"):
        MagicSquareValidator(small_grid)
```

### Track B — Algorithm Track (알고리즘 테스트)

```
목표  : 탐색 전략(백트래킹)의 단계별 동작을 검증
특성  : 리팩토링 시 수정·삭제 가능
마커  : @pytest.mark.unit
위치  : tests/control/
```

**RED 예시 — 알고리즘 테스트 (아직 구현 없음)**

```python
@pytest.mark.unit
def test_solver_finds_solution_for_empty_grid():
    """
    Invariant: INV-04, INV-05, INV-06, INV-07
    빈 격자에 대해 Solver는 유효한 마방진을 반환한다.
    """
    # Arrange
    empty_grid = [[0] * 4 for _ in range(4)]
    solver = Solver()
    # Act
    result = solver.solve(empty_grid)
    # Assert
    assert result is not None
    assert MagicSquareValidator(result).is_valid()
```

### GREEN — 최소 구현 원칙

> 테스트를 통과시키는 **가장 단순한 코드**만 작성한다.  
> 이 단계에서 추상화·최적화·패턴 적용은 금지한다.

| 단계 | 허용 | 금지 |
|------|------|------|
| GREEN | 하드코딩 반환, 단순 분기 | 클래스 설계 변경, 알고리즘 최적화 |
| GREEN | 기존 테스트 유지 | 기존 테스트 수정으로 통과율 올리기 |

### REFACTOR — 통합 정리

> 두 트랙 모두 GREEN인 상태에서만 리팩토링을 시작한다.

```
정리 순서
  1. 중복 제거 (DRY): 반복 로직을 helper 또는 rules.py 순수 함수로 추출
  2. 이름 정리: 변수·함수명이 Invariant 언어와 일치하는지 확인
  3. 레이어 경계 정리: Control ↔ Entity 의존성이 올바른 방향인지 재검사
  4. 전체 테스트 재실행: Track A + Track B 모두 GREEN 확인
  5. 커버리지 확인: domain 95% 이상 유지
```

### 이 단계의 산출물

- [ ] Track A: 계약 테스트 전체 GREEN (`@pytest.mark.contract`)
- [ ] Track B: 알고리즘 테스트 전체 GREEN (`@pytest.mark.unit`)
- [ ] 리팩토링 후 전체 테스트 GREEN
- [ ] `pytest --cov` 리포트 — domain 95% 이상

### 함정 (Pitfall)

> **함정:** GREEN 단계에서 "어차피 리팩토링할 거니까 지금 잘 만들자"는 충동.  
> **결과:** 리팩토링 범위가 불분명해지고, 테스트 없이 설계가 변경된다.

---

## Step 5 — 회귀 보호

### 핵심 원칙

> 행복한 경로(Happy Path)만 테스트하면 Invariant의 절반이 보호되지 않는다.  
> 엣지·오류·조합 실패 케이스가 **안전망**을 완성한다.

### 5-1. 엣지 케이스 추가

| 케이스 | 설명 | 관련 Invariant |
|--------|------|----------------|
| 유일하게 유효한 부분 배치 | 15칸이 채워지고 마지막 1칸만 결정 | INV-03 |
| 이미 완성된 격자를 Solver에 전달 | 재탐색 없이 즉시 반환 | INV-08 |
| Magic Sum 경계값 확인 | 행 합이 33 또는 35인 경우 False | INV-05 |
| 대각선만 틀린 경우 | 행·열은 맞고 대각만 34가 아닌 경우 | INV-07 |

### 5-2. 입력 오류 케이스 추가

| 케이스 | 예시 입력 | 기대 예외 | 관련 Invariant |
|--------|-----------|-----------|----------------|
| 빈 리스트 | `[]` | `ValueError` | INV-01 |
| 비정방형 격자 | `[[1,2,3],[4,5]]` | `ValueError` | INV-01 |
| 0 포함 (완성 상태) | `[[0,2,3,...],...]` | `ValueError` | INV-02 |
| 17 포함 | `[[17,2,3,...],...]` | `ValueError` | INV-02 |
| 문자열 원소 | `[["a",2,3,...],...]` | `TypeError` | INV-02 |
| 중복 포함 (완성 상태) | `[[1,1,2,...],...]` | `ValueError` | INV-03 |
| None 입력 | `None` | `TypeError` | INV-01 |

### 5-3. 조합 실패 케이스 추가

> 단일 Invariant 위반이 아니라, **여러 Invariant가 동시에 연관된** 실패 시나리오를 추가한다.

| 케이스 | 설명 | 연관 Invariant |
|--------|------|----------------|
| 크기는 맞으나 합 조건 불만족 | 4×4, 1~16 한 번씩이지만 행 합이 34가 아님 | INV-03 + INV-05 |
| 합은 맞으나 숫자 범위 위반 | 행 합이 34이지만 원소에 0과 17 혼합 | INV-02 + INV-04 |
| 해가 없는 부분 배치 | 제약을 만족하는 완성이 불가능한 초기 배치 | INV-08 + INV-03~07 |
| Solver 결과 Validator 재검증 | `solve()` 반환값을 `is_valid()`로 다시 검증 | INV-04~07 전체 |

### 5-4. 회귀 보호 실행 명령

```bash
# 계약 테스트만 실행
pytest -m contract -v

# 단위 테스트만 실행
pytest -m unit -v

# 전체 실행 + 커버리지
pytest --cov=magic_square/entity --cov=magic_square/control \
       --cov-report=term-missing --cov-fail-under=80

# Invariant 추적 태그 누락 검사 (docstring 내 "Invariant:" 없는 테스트 탐지)
grep -rn "def test_" tests/ | grep -v "Invariant:"
```

### 이 단계의 산출물

- [ ] 엣지 케이스 테스트 추가 완료
- [ ] 입력 오류 케이스 테스트 추가 완료
- [ ] 조합 실패 케이스 테스트 추가 완료
- [ ] 전체 테스트 GREEN + domain 커버리지 95% 이상
- [ ] `Invariant: INV-XX` 태그 누락 테스트 0건

### 함정 (Pitfall)

> **함정:** 회귀 테스트를 "완성 후 추가"가 아니라 "나중에 언젠가"로 미룬다.  
> **결과:** 리팩토링이 기존 계약을 무너뜨려도 발견되지 않는다.

---

## Journey 완료 기준 (Definition of Done)

| 항목 | 기준 |
|------|------|
| Step 1 | Invariant 목록 문서화, 코드 0줄 |
| Step 2 | 입력·출력·예외 계약 문서화, 코드 0줄 |
| Step 3 | 4개 컴포넌트 책임·레이어 확정, 의존성 방향 검증 완료 |
| Step 4 | Track A + Track B 모두 GREEN, 리팩토링 완료 |
| Step 5 | 엣지·오류·조합 케이스 추가, 전체 GREEN, 커버리지 95% |

---

## 다음 단계 (Level 3: Task)

각 Step은 구체적인 Task로 분해된다.

| Task ID | 설명 | 부모 Step |
|---------|------|-----------|
| T-01 | `entity/constants.py` 작성 (GRID_SIZE, MAGIC_SUM, NUMBER_RANGE) | Step 1 |
| T-02 | `entity/square.py` — `MagicSquare` 값 객체 + 입력 검증 | Step 2 |
| T-03 | `entity/rules.py` — 합 조건 순수 함수 | Step 3 |
| T-04 | `entity/blank_finder.py` — `BlankFinder` 구현 | Step 3 |
| T-05 | `entity/missing_number_finder.py` — `MissingNumberFinder` 구현 | Step 3 |
| T-06 | `entity/validator.py` — `MagicSquareValidator` 구현 | Step 3 |
| T-07 | `control/solver.py` — `Solver` 백트래킹 구현 | Step 4 |
| T-08 | `boundary/cli.py` — CLI 진입점 구현 | Step 4 |
| T-09 | 회귀 테스트 스위트 완성 | Step 5 |

> User Story 상세는 `06-user-journey-stories.md`에서, Task는 `07-user-journey-tasks.md`에서 작성한다.

---

*본 문서는 사용자 여정 Level 2 (User Journey) 산출물이며, Level 3 (Task) 작업은 별도 문서에서 이어진다.*


---

<!-- SNAPSHOT FROM: 06-user-journey-stories.md -->

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


---

<!-- SNAPSHOT FROM: 08-level4-implementation-scenario-technical.md -->

# Level 4: 구현 시나리오 — Technical (Gherkin)

**작성일:** 2026-04-27  
**상위 문서:** `04-user-journey-epic.md` · `05-user-journey-level2.md` · `06-user-journey-stories.md`  
**범위:** 4×4 부분 마방진 완성 유스케이스 — BDD 시나리오, 공통 배경(Given), 오류 케이스

---

## 문서 목적

- **TDD/BDD**로 구현·검증을 연동할 때, **불변조건**과 **Story US-01~US-05**를 그대로 실행 가능한 **시나리오**로 고정한다.
- 아래 `Feature`는 [Gherkin](https://cucumber.io/docs/gherkin/) 문법이며, `pytest-bdd` / `behave` / 수동 `Given-When-Then` 테스트에 매핑할 수 있다.

### 기술적 약속 (이 Feature 전제)

| 항목 | 약속 |
|------|------|
| **격자 표기** | 4×4, `0` = 빈칸 |
| **빈칸** | **정확히 2개** |
| **값** | 1~16, `0`은 범위 제외(빈칸) |
| **중복** | `0`을 제외한 칸끼리 **중복 불가** |
| **Magic Sum** | 34 — `entity/constants.py`에 **명명 상수**로 둔다 (매직 넘버 금지) |
| **빈칸 순서** | row-major(행·열) |
| **누락 2수 배치** | 1차: (작은 수, 큰 수) = (첫 번째 빈칸, 두 번째 빈칸) · 2차(역): (큰 수, 작은 수) |
| **성공 응답** | **길이 6** 배열: `[r1, c1, v1, r2, c2, v2]` — **행·열 좌표는 1-indexed** (사용자 관점) |

> 구현에서 내부 API는 0-index를 써도 되되, **공개 API/최종 반환**이 위 약속과 맞는지 시나리오 `Then`으로 잠근다.

---

## Feature: 4×4 마방진 완성

```gherkin
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
```

> `Background`의 "정확히 2개의 0" 등은 **성공 시나리오(Scenario 1, 2)**에 적용됩니다. **실패 시나리오(Scenario 3~5)**는 의도적으로 조건을 깨는 입력이므로, 구현 시에는 **Background를 Scenario별로 오버라이드**하거나, `Scenario`-전용 `Given`만 사용하도록 BDD 러너 설정을 맞추세요.

---

### Scenario: 작은 수 → 큰 수 순서로 마방진이 완성되는 경우

**연결:** `06-user-journey-stories.md` — US-02, US-03, US-04, US-05(1차 시도 성공)

**매트릭스 (입력, 0-index 내부 구현용):**

| r\c | 0  | 1  | 2  | 3  |
|-----|----|----|----|----|
| 0   | 16 | 2  | 3  | 13 |
| 1   | 5  | 11 | 10 | 8  |
| 2   | 9  | 7  | 0  | 12 |
| 3   | 4  | 14 | 15 | 0  |

- 빈칸 (0-index): `(2,2)`, `(3,3)` → 1-based: (3,3), (4,4)
- 누락 2수: **1**과 **6** (오름차순: **1, 6**)
- **검산:** 1·6을 **(첫 빈칸, 둘째 빈칸)** = (1,6)로 두면 3행·4행 합이 34가 되지 **않음**. **(6,1)**이면 34(마방진)로 맞는다. 즉, **동일 `Given` 표**에 대해 **US-05의 1차(작·큰 순) 시도는 실패**하고 **2차(역) 시도가 성공**한다.
- 따라서 **아래 Gherkin을 TDD에 그대로 쓰려면:** (1) **Scenario 1**용으로는 `Given` **다른** 행렬(1·6 **순**으로 완성되는 케이스)을 쓰거나, (2) **Scenario 1**을 *“1차 시도의 결과*가* 마방진이면 그걸 반환”*로 구현·검정하고, **이 표**는 **Scenario: 역순** 쪽 `Given`에 맞긴다.

```gherkin
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
```

**1차 성공 전용 `Given` 예(개념, 별도 픽스처로 검산할 것):** 1·6 **순**이 첫/둘째 빈칸에 들어갔을 때만 **Then**을 만족하는 **다른 4×4(0 두 칸)**을 Scenario Outline/테이블로 둔다. **위에 인용한 표**만으로 **Scenario: 작은→큰** **Then**을 맞추는 것은 수식상 불가하므로(위 검산), 문서/테스트 **일치**를 꼭 확인할 것.

---

### Scenario: 역순 배치 시 마방진이 완성되는 경우

**연결:** US-05 — 1차 실패, 2차(역) 성공

> **이 표(동일 `Given`)** 는 수식상 (1,6) 순이 실패·(6,1)이 성공하므로, **“역순” 시나리오의 자연한 예**이며, “작→큰으로 완성” **성공** 시나리오와 **한 표를 공유하면 모순**이 생긴다(위 **검산**). Step Definition에서는 **다른** 성공 `Given`을 쓰거나, Scenario 1/2 **Examples** 를 분리한다.

```gherkin
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
```

**구현 메모 (일관성):**  
"역순 전용" 시나리오는 **1차=실패·2차=성공**을 보장하는 **다른** `Given` 격자를 쓰거나, `When`을 **훅**으로 “1차는 일부러 스킵/실패”로 가정한 **테스트 더블**이 필요할 수 있다. TDD로는 **역배치만** 성공하는 **확인된 샘플** 1개를 `features/data/`에 두는 것이 안전하다.

---

### Scenario: 빈칸 개수가 올바르지 않은 경우

**연결:** US-01, INV-01 + “빈칸 2개” 확장 계약

```gherkin
  Scenario: 빈칸 개수가 올바르지 않은 경우
    Given 행렬에 빈칸이 1개만 존재할 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다
```

**예 (빈칸 1개, 개략):** 15칸이 채워지고 0이 한 칸뿐 — `ValueError` (또는 팀이 정한 도메인 예외)

---

### Scenario: 중복 숫자가 존재하는 경우

**연결:** US-01, INV-03

```gherkin
  Scenario: 중복 숫자가 존재하는 경우
    Given 0을 제외한 중복 숫자가 포함된 행렬일 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다
```

**예 (개략):** 4×4, 0은 2칸, 나머지 14칸에 동일한 수 2회 등

---

### Scenario: 값의 범위를 벗어난 경우

**연결:** US-01, INV-02

```gherkin
  Scenario: 값의 범위를 벗어난 경우
    Given 행렬에 16을 초과하는 숫자가 포함되어 있을 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다
```

**예 (개략):** 17, 0, 또는 1 미만 정수

---

## Invariant 매핑 (요약)

| 시나리오 | Invariant (Epic) |
|----------|------------------|
| Success (작→큰) | INV-02~07, US-02~05 |
| Success (역) | 동일 + US-05 |
| 오류 3~5 | INV-01, INV-02, INV-03, “빈칸 2개” 계약 |

---

## pytest-bdd / Step 템플릿 (참고)

- `Given "다음과 같은 행렬이 주어졌을 때"` — 테이블 → `list[list[int]]` 파싱
- `Then "길이 6의 배열"` — `len(result) == 6`
- `Then "1-index"` — `result[0], result[1] in {1,2,3,4}` 등

```python
# tests/boundary/ 또는 tests/features/ (프로젝트 규칙에 맞게)
from pytest_bdd import then, parsers

@then("결과는 길이 6의 배열로 반환되어야 하며")
def result_length_6(complete_puzzle) -> None:
    assert len(complete_puzzle.result_vector) == 6
```

---

## 다음 문서 (선택)

- 작업 쪼개기: `07-user-journey-tasks.md` (Task 목록, 없으면 생성)
- Gherkin 파일: `tests/features/complete_4x4.feature` (저장 시 `.feature`로 분리)

---

*본 문서는 Level 4 (Technical — 구현 시나리오) 산출물이다.*


---

<!-- SNAPSHOT FROM: 09-level5-scenario-verification.md -->

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

