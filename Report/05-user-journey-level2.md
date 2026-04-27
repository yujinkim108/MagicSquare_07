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
