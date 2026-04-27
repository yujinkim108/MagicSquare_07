# Magic Square TDD design and architecture
_Exported on 4/27/2026 at 16:59:05 GMT+9 from Cursor (3.0.16)_

---

**User**

당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.

프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련
제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정

입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지
출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

------------------------------------------------------------
출력 형식 (반드시 이 구조로)
------------------------------------------------------------

# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
- Entities / Value Objects / Domain Services 목록과 책임(SRP)
## 1.2 도메인 불변조건(Invariants)
- 행/열/대각선 합 일치, Magic Constant 등
## 1.3 핵심 유스케이스(도메인 관점)
- 빈칸 찾기, 누락 숫자 찾기, 마방진 판정, 두 조합 시도
## 1.4 Domain API(내부 계약)
- 메서드 시그니처 수준(코드 X) + 입력/출력/실패조건
## 1.5 Domain 단위 테스트 설계(RED 우선)
- 테스트 케이스 목록(정상/비정상/엣지)
- 각 테스트가 보호하는 invariant 명시

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)
## 2.1 사용자/호출자 관점 시나리오
- “행렬 입력 → 검증 → 결과 출력” 흐름
## 2.2 UI 계약(외부 계약)
- Input schema / Output schema / Error schema
## 2.3 UI 레벨 테스트(Contract-first, RED 우선)
- 잘못된 크기, 빈칸 개수 오류, 값 범위 오류, 중복 오류, 반환 포맷 검증
- Domain은 Mock으로 가정
## 2.4 UX/출력 규칙
- 에러 메시지 표준(정확한 문구 규칙까지)

# 3) Data Layer 설계 (Data Layer)
## 3.1 목적 정의
- “저장/로드”의 필요성과 범위(학습용)
## 3.2 인터페이스 계약
- 예: MatrixRepository.save/load (메서드 수준, 코드 X)
- 저장 대상: 입력 행렬, 실행 결과(선택)
## 3.3 구현 옵션 비교(메모리/파일)
- 옵션 A: InMemory / 옵션 B: File(JSON/CSV)
- 추천안 1개 선택 + 이유
## 3.4 Data 레이어 테스트
- 저장/로드 정합성, 예외(파일 없음/형식 오류), 불변조건(4x4 유지)

# 4) Integration & Verification (통합 및 검증)
## 4.1 통합 경로 정의
- UI → Application(선택) → Domain → Data 흐름(의존성 방향 포함)
## 4.2 통합 테스트 시나리오
- 정상 시나리오 2개 이상
- 실패 시나리오 3개 이상(입력 오류, 도메인 실패, 데이터 실패)
## 4.3 회귀 보호 규칙
- 기존 테스트 유지 정책
- 변경 금지 규칙(계약/출력 포맷)
## 4.4 커버리지 목표
- Domain Logic 95%+
- UI Boundary 85%+
- Data 80%+
## 4.5 Traceability Matrix (필수)
- Concept(Invariant) → Rule → Use Case → Contract → Test → Component

------------------------------------------------------------
추가 조건
------------------------------------------------------------
- 모호한 표현 금지(“적절히/충분히” 금지)
- 모든 규칙은 검증 가능해야 함(테스트로 확인 가능)
- 구현 코드 작성 금지
- 표/체크리스트를 적극 사용


---

**Cursor**

# Magic Square (4×4) — TDD 설계 문서

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

### Entities

| 이름 | 종류 | 책임(SRP) | 가변/불변 |
|---|---|---|---|
| `Matrix4x4` | Value Object | 4×4 정수 행렬의 구조적 표현 및 셀 접근 | 불변 |
| `Cell` | Value Object | 1-indexed (row, col) 위치 표현 | 불변 |
| `MissingPair` | Value Object | 두 누락 숫자(smaller, larger) 쌍 표현 | 불변 |
| `Solution` | Value Object | 출력 계약의 6-tuple [r1,c1,n1,r2,c2,n2] 표현 | 불변 |

### Domain Services

| 이름 | 책임(SRP) | 의존 대상 |
|---|---|---|
| `BlankLocator` | `Matrix4x4`에서 값이 0인 셀 2개의 위치를 탐색 | `Matrix4x4` |
| `MissingNumberDetector` | 1~16 중 행렬에 없는 숫자 2개를 탐색 | `Matrix4x4` |
| `MagicSquareValidator` | 완성 행렬의 모든 행/열/대각선 합이 34인지 검증 | `Matrix4x4` |
| `CombinationEvaluator` | 두 빈칸에 두 숫자를 배치하는 두 조합을 시도하고 유효 조합을 선택 | `MagicSquareValidator` |
| `MagicSquareSolver` | 위 모든 서비스를 오케스트레이션하여 `Solution` 반환 | 위 모든 서비스 |

---

## 1.2 도메인 불변조건(Invariants)

| ID | 불변조건 | 수식/기준 | 검증 시점 |
|---|---|---|---|
| INV-01 | **Magic Constant**: 모든 행의 합 = 34 | `∀ r ∈ {1..4}: Σ matrix[r][c] = 34` | 완성 행렬 검증 시 |
| INV-02 | **Magic Constant**: 모든 열의 합 = 34 | `∀ c ∈ {1..4}: Σ matrix[r][c] = 34` | 완성 행렬 검증 시 |
| INV-03 | **Magic Constant**: 주대각선 합 = 34 | `Σ matrix[i][i] = 34, i∈{1..4}` | 완성 행렬 검증 시 |
| INV-04 | **Magic Constant**: 반대각선 합 = 34 | `Σ matrix[i][5-i] = 34, i∈{1..4}` | 완성 행렬 검증 시 |
| INV-05 | **Completeness**: 완성 행렬은 1~16을 각각 정확히 1회 포함 | `sorted(all cells) == [1..16]` | 완성 행렬 검증 시 |
| INV-06 | **Blank Count**: 입력 행렬의 0의 개수 = 2 | `count(0) == 2` | 입력 수신 즉시 |
| INV-07 | **Value Range**: 모든 셀 값 ∈ {0} ∪ {1..16} | `∀ cell: 0 ≤ val ≤ 16` | 입력 수신 즉시 |
| INV-08 | **Uniqueness**: 0을 제외한 값은 중복 불가 | `non-zero values: no duplicates` | 입력 수신 즉시 |
| INV-09 | **Blank Order**: 빈칸은 행 우선(row-major) 탐색 순서로 blank1 < blank2 | 탐색 순서 정의 | 빈칸 탐색 시 |
| INV-10 | **Output Ordering**: n1<n2일 때, (n1→blank1, n2→blank2)가 마방진이면 그 순서, 아니면 역순 | 조합 시도 우선순위 규칙 | 조합 평가 시 |

---

## 1.3 핵심 유스케이스 (도메인 관점)

### UC-01: 빈칸 위치 찾기

- **행위자**: `MagicSquareSolver`
- **입력**: `Matrix4x4`
- **처리**: 행 우선(row 1→4, col 1→4) 순서로 값이 0인 셀을 탐색하여 순서대로 blank1, blank2로 지정
- **출력**: `Cell[2]` (INV-09 보장)
- **실패조건**: 0의 개수 ≠ 2 → 도달 불가(UI에서 사전 차단)

### UC-02: 누락 숫자 찾기

- **행위자**: `MagicSquareSolver`
- **입력**: `Matrix4x4`
- **처리**: {1..16} 집합에서 행렬에 없는 숫자를 탐색, 오름차순 정렬하여 (smaller, larger) 지정
- **출력**: `MissingPair(smaller, larger)` where `smaller < larger`
- **실패조건**: 누락 숫자 수 ≠ 2 → 도달 불가(INV-06, INV-08 보장)

### UC-03: 마방진 판정

- **행위자**: `MagicSquareValidator`
- **입력**: 완성된 `Matrix4x4` (0 없음)
- **처리**: INV-01~INV-04 검증 (4행 + 4열 + 2대각선 = 10개 합 확인)
- **출력**: `boolean` (true = 마방진)
- **실패조건**: 없음 (순수 계산)

### UC-04: 두 조합 시도

- **행위자**: `CombinationEvaluator`
- **입력**: `Matrix4x4`, `Cell[2]`, `MissingPair`
- **처리**:
  1. 조합A: blank1 ← smaller, blank2 ← larger → `MagicSquareValidator` 호출
  2. 조합A가 마방진 → `Solution(r1,c1,smaller,r2,c2,larger)` 반환
  3. 조합A 실패 → 조합B: blank1 ← larger, blank2 ← smaller → `MagicSquareValidator` 호출
  4. 조합B가 마방진 → `Solution(r1,c1,larger,r2,c2,smaller)` 반환
  5. 둘 다 실패 → `NoSolutionException` 발생
- **출력**: `Solution`
- **실패조건**: 어떤 조합도 마방진을 만족하지 않음

### UC-05: 전체 풀이 오케스트레이션

- **행위자**: `MagicSquareSolver`
- **입력**: `Matrix4x4`
- **처리**: UC-01 → UC-02 → UC-04 순서로 호출
- **출력**: `Solution`
- **실패조건**: UC-04에서 `NoSolutionException` 전파

---

## 1.4 Domain API (내부 계약)

### `BlankLocator`

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `findBlanks(matrix: Matrix4x4) → Cell[2]` | 검증된 `Matrix4x4` | 행 우선 순서의 빈칸 좌표 2개 | INV-06 위반 시 `IllegalStateException` |

**사전조건**: 입력 행렬은 INV-06, INV-07, INV-08을 만족  
**사후조건**: 반환된 `Cell[0].row ≤ Cell[1].row`, 같은 행이면 `Cell[0].col < Cell[1].col`

---

### `MissingNumberDetector`

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `findMissing(matrix: Matrix4x4) → MissingPair` | 검증된 `Matrix4x4` | `MissingPair(smaller, larger)` where smaller < larger | 누락 수 ≠ 2이면 `IllegalStateException` |

**사전조건**: INV-06, INV-07, INV-08 만족  
**사후조건**: `smaller ∈ {1..16}`, `larger ∈ {1..16}`, `smaller < larger`

---

### `MagicSquareValidator`

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `validate(matrix: Matrix4x4) → boolean` | 0이 없는 완성 `Matrix4x4` | true/false | 없음 (순수함수) |
| `rowSum(matrix: Matrix4x4, row: int) → int` | 행렬, 1-indexed row | 해당 행의 합 | `row ∉ {1..4}` 이면 `IndexOutOfBoundsException` |
| `colSum(matrix: Matrix4x4, col: int) → int` | 행렬, 1-indexed col | 해당 열의 합 | `col ∉ {1..4}` 이면 `IndexOutOfBoundsException` |
| `mainDiagSum(matrix: Matrix4x4) → int` | 완성 행렬 | 주대각선 합 | 없음 |
| `antiDiagSum(matrix: Matrix4x4) → int` | 완성 행렬 | 반대각선 합 | 없음 |

**사후조건 (validate=true)**: 10개(4행+4열+2대각선) 모두 = 34

---

### `CombinationEvaluator`

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `evaluate(matrix: Matrix4x4, blanks: Cell[2], pair: MissingPair) → Solution` | 기본 행렬, 빈칸 위치, 누락 쌍 | `Solution` | 두 조합 모두 실패 시 `NoSolutionException` |

**사후조건**: 반환된 `Solution`의 값을 행렬에 적용하면 `MagicSquareValidator.validate() == true`

---

### `MagicSquareSolver`

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `solve(matrix: Matrix4x4) → Solution` | 검증된 `Matrix4x4` | `Solution([r1,c1,n1,r2,c2,n2])` | 해 없음: `NoSolutionException` |

**사전조건**: INV-06, INV-07, INV-08 모두 만족 (UI에서 보장)  
**사후조건**: 반환된 Solution을 행렬에 적용 시 INV-01~INV-05 모두 만족

---

### 예외 정의

| 예외 클래스 | 발생 조건 | 도메인/UI 경계 |
|---|---|---|
| `NoSolutionException` | 두 조합 모두 마방진 불만족 | Domain |
| `IllegalStateException` | 도메인 내부 상태 위반(blank ≠ 2 등) | Domain |

---

## 1.5 Domain 단위 테스트 설계 (RED 우선)

### BlankLocator 테스트

| TC ID | 시나리오 | 입력 특징 | 기대 출력 | 보호 Invariant |
|---|---|---|---|---|
| BL-01 | 정상: 빈칸 2개 (첫행, 마지막행) | `[0,_,_,_]`, `[_,_,_,0]` | `[Cell(1,1), Cell(4,4)]` | INV-09 |
| BL-02 | 정상: 빈칸 2개 (같은 행) | row1에 col2, col4가 0 | `[Cell(1,2), Cell(1,4)]` | INV-09 |
| BL-03 | 정상: 빈칸 2개 (대각선) | `(1,1)=0`, `(4,4)=0` | `[Cell(1,1), Cell(4,4)]` | INV-09 |
| BL-04 | 엣지: 빈칸이 인접한 셀 | `(2,3)=0`, `(2,4)=0` | `[Cell(2,3), Cell(2,4)]` | INV-09 |
| BL-05 | 비정상: 빈칸 0개 | 0 없음 | `IllegalStateException` | INV-06 |
| BL-06 | 비정상: 빈칸 1개 | 0 하나 | `IllegalStateException` | INV-06 |
| BL-07 | 비정상: 빈칸 3개 | 0 세 개 | `IllegalStateException` | INV-06 |

### MissingNumberDetector 테스트

| TC ID | 시나리오 | 입력 특징 | 기대 출력 | 보호 Invariant |
|---|---|---|---|---|
| MD-01 | 정상: 가운데 숫자 누락 | 8, 9 누락 | `MissingPair(8, 9)` | INV-05 |
| MD-02 | 엣지: 경계 숫자 누락 (1, 16) | 1, 16 누락 | `MissingPair(1, 16)` | INV-05 |
| MD-03 | 엣지: 인접 숫자 누락 (7, 8) | 7, 8 누락 | `MissingPair(7, 8)` | INV-05 |
| MD-04 | 정상: 비연속 숫자 누락 (3, 14) | 3, 14 누락 | `MissingPair(3, 14)` | INV-05 |
| MD-05 | 비정상: 누락 1개(INV-06 위반 선행) | — | `IllegalStateException` | INV-06 |

### MagicSquareValidator 테스트

| TC ID | 시나리오 | 입력 특징 | 기대 출력 | 보호 Invariant |
|---|---|---|---|---|
| MV-01 | 정상: 알려진 완성 마방진 | 두뇨 4×4 표준 마방진 | `true` | INV-01~04 |
| MV-02 | 비정상: 1행 합 ≠ 34 | row1 합 = 33 | `false` | INV-01 |
| MV-03 | 비정상: 2열 합 ≠ 34 | col2 합 = 35 | `false` | INV-02 |
| MV-04 | 비정상: 주대각선 합 ≠ 34 | main diag = 32 | `false` | INV-03 |
| MV-05 | 비정상: 반대각선 합 ≠ 34 | anti diag = 36 | `false` | INV-04 |
| MV-06 | 엣지: 행/열은 맞지만 대각선 틀림 | row/col OK, diag fail | `false` | INV-03 or INV-04 |
| MV-07 | rowSum 경계: row=1, row=4 | 유효 행 | 정수 합 반환 | INV-01 |
| MV-08 | rowSum 범위 초과: row=0, row=5 | 범위 외 | `IndexOutOfBoundsException` | INV-01 |

### CombinationEvaluator 테스트

| TC ID | 시나리오 | 조합A 결과 | 기대 출력 | 보호 Invariant |
|---|---|---|---|---|
| CE-01 | 조합A 성공 (smaller→blank1) | 마방진 | `Solution([r1,c1,smaller,r2,c2,larger])` | INV-10 |
| CE-02 | 조합A 실패, 조합B 성공 (larger→blank1) | 마방진 아님 | `Solution([r1,c1,larger,r2,c2,smaller])` | INV-10 |
| CE-03 | 두 조합 모두 실패 | 둘 다 아님 | `NoSolutionException` | INV-10 |
| CE-04 | 엣지: 빈칸이 같은 행에 있는 경우 조합A 성공 | 마방진 | `Solution` (INV-10 순서) | INV-01, INV-10 |
| CE-05 | 엣지: 빈칸이 대각선 상에 있는 경우 | — | `Solution` or `NoSolutionException` | INV-03, INV-10 |

### MagicSquareSolver 통합 단위 테스트

| TC ID | 시나리오 | 기대 출력 | 보호 Invariant |
|---|---|---|---|
| MS-01 | 정상: 조합A 순서 풀이 가능 | `int[6]` (작은수 먼저) | INV-01~10 |
| MS-02 | 정상: 조합B 순서로만 풀이 가능 | `int[6]` (큰수 먼저 at blank1) | INV-10 |
| MS-03 | 실패: 해 없음 | `NoSolutionException` | INV-01~04 |

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오

```
호출자 → [입력 행렬 제출]
           ↓
        [UI Boundary: 입력 스키마 검증]
           ↓ 검증 실패
        [에러 응답 반환] ──────────────→ 호출자
           ↓ 검증 성공
        [Domain: MagicSquareSolver.solve()]
           ↓ NoSolutionException
        [에러 응답 반환] ──────────────→ 호출자
           ↓ 성공
        [출력 스키마 직렬화]
           ↓
        [성공 응답 반환] ──────────────→ 호출자
```

### 흐름 단계 정의

| 단계 | 책임자 | 성공 조건 |
|---|---|---|
| 1. 입력 수신 | UI Boundary | 4×4 int[][] 형태로 파싱 가능 |
| 2. 크기 검증 | UI Boundary | 행 수 = 4, 각 행의 열 수 = 4 |
| 3. 값 범위 검증 | UI Boundary | 모든 값 ∈ {0..16} |
| 4. 빈칸 수 검증 | UI Boundary | 0의 개수 = 2 |
| 5. 중복 검증 | UI Boundary | 0 제외 중복 없음 |
| 6. 도메인 호출 | UI Boundary | `MagicSquareSolver.solve()` 호출 |
| 7. 결과 직렬화 | UI Boundary | `int[6]` 포맷 보장 |

---

## 2.2 UI 계약 (외부 계약)

### Input Schema

```
InputContract:
  type: int[][]
  dimensions:
    rows: exactly 4
    cols_per_row: exactly 4
  cell_value:
    type: int
    range: [0, 16] (inclusive)
  zero_count: exactly 2
  uniqueness:
    rule: non-zero values must be distinct
    scope: all 16 cells
```

### Output Schema (성공)

```
OutputContract:
  type: int[6]
  indices:
    [0] = r1  : int, range [1,4], 첫 번째 빈칸의 행 (1-indexed)
    [1] = c1  : int, range [1,4], 첫 번째 빈칸의 열 (1-indexed)
    [2] = n1  : int, range [1,16], 첫 번째 빈칸에 채울 숫자
    [3] = r2  : int, range [1,4], 두 번째 빈칸의 행 (1-indexed)
    [4] = c2  : int, range [1,4], 두 번째 빈칸의 열 (1-indexed)
    [5] = n2  : int, range [1,16], 두 번째 빈칸에 채울 숫자
  ordering_rule:
    let smaller = min(n1,n2), larger = max(n1,n2)
    if (smaller→blank1, larger→blank2) is magic: n1=smaller, n2=larger
    else: n1=larger, n2=smaller
```

### Error Schema

```
ErrorContract:
  type: ErrorResponse
  fields:
    code: ErrorCode (enum)
    message: string (정확한 문구 규칙은 2.4 참조)
  codes:
    INVALID_SIZE        : 행렬이 4×4가 아님
    INVALID_BLANK_COUNT : 0의 개수가 2가 아님
    INVALID_VALUE_RANGE : 값이 0 이상 16 이하가 아닌 셀 존재
    INVALID_DUPLICATE   : 0을 제외한 중복 값 존재
    NO_SOLUTION         : 유효한 마방진 배치 없음
```

---

## 2.3 UI 레벨 테스트 (Contract-first, RED 우선)

> Domain은 Mock으로 대체. `MockMagicSquareSolver`는 호출 시 고정 `Solution` 또는 `NoSolutionException`을 반환하도록 설정.

### 입력 크기 오류

| TC ID | 시나리오 | 입력 | 기대 에러코드 | 기대 에러 메시지 |
|---|---|---|---|---|
| UI-SZ-01 | 행 수 부족 (3행) | `int[3][4]` | `INVALID_SIZE` | 규칙 참조 (2.4) |
| UI-SZ-02 | 행 수 초과 (5행) | `int[5][4]` | `INVALID_SIZE` | 규칙 참조 (2.4) |
| UI-SZ-03 | 열 수 부족 (col=3) | `int[4][3]` | `INVALID_SIZE` | 규칙 참조 (2.4) |
| UI-SZ-04 | 열 수 초과 (col=5) | `int[4][5]` | `INVALID_SIZE` | 규칙 참조 (2.4) |
| UI-SZ-05 | null 입력 | `null` | `INVALID_SIZE` | 규칙 참조 (2.4) |
| UI-SZ-06 | 빈 배열 | `int[0][0]` | `INVALID_SIZE` | 규칙 참조 (2.4) |

### 빈칸 개수 오류

| TC ID | 시나리오 | 0의 개수 | 기대 에러코드 |
|---|---|---|---|
| UI-BC-01 | 0개 | 0 | `INVALID_BLANK_COUNT` |
| UI-BC-02 | 1개 | 1 | `INVALID_BLANK_COUNT` |
| UI-BC-03 | 3개 | 3 | `INVALID_BLANK_COUNT` |
| UI-BC-04 | 16개 (전부 0) | 16 | `INVALID_BLANK_COUNT` |

### 값 범위 오류

| TC ID | 시나리오 | 위반 값 | 기대 에러코드 |
|---|---|---|---|
| UI-VR-01 | 음수 값 | -1 | `INVALID_VALUE_RANGE` |
| UI-VR-02 | 17 초과 | 17 | `INVALID_VALUE_RANGE` |
| UI-VR-03 | 경계: 0 (허용) | 0 | 정상 처리 (다음 검증 단계) |
| UI-VR-04 | 경계: 16 (허용) | 16 | 정상 처리 |
| UI-VR-05 | 경계: 1 (허용) | 1 | 정상 처리 |

### 중복 오류

| TC ID | 시나리오 | 위반 내용 | 기대 에러코드 |
|---|---|---|---|
| UI-DU-01 | 같은 숫자 2개 | 두 셀에 값 5 | `INVALID_DUPLICATE` |
| UI-DU-02 | 같은 숫자 3개 | 세 셀에 값 3 | `INVALID_DUPLICATE` |
| UI-DU-03 | 0은 2개여도 중복 아님 | 0이 2개 | 중복 아님 (정상 처리) |

### 반환 포맷 검증 (Domain Mock 사용)

| TC ID | 시나리오 | Mock 반환값 | 검증 항목 |
|---|---|---|---|
| UI-FMT-01 | 정상 성공 | `Solution([2,1,9,3,4,7])` | 길이=6, 타입=int[] |
| UI-FMT-02 | 좌표 1-indexed 확인 | `Solution([1,1,x,4,4,y])` | r1,c1,r2,c2 ∈ {1..4} |
| UI-FMT-03 | n1,n2 ∈ {1..16} 확인 | `Solution([_,_,1,_,_,16])` | n1,n2 ∈ {1..16} |
| UI-FMT-04 | 도메인 `NoSolutionException` | Mock이 예외 발생 | `NO_SOLUTION` 에러 반환 |

### 검증 순서 테스트

| TC ID | 목적 | 검증 내용 |
|---|---|---|
| UI-ORD-01 | INVALID_SIZE가 다른 에러보다 먼저 | 5×4 배열에 0이 3개 있어도 `INVALID_SIZE` 반환 |
| UI-ORD-02 | INVALID_VALUE_RANGE가 BLANK_COUNT보다 먼저 | 범위 초과 값 + 0 개수 오류 → `INVALID_VALUE_RANGE` |
| UI-ORD-03 | INVALID_BLANK_COUNT가 DUPLICATE보다 먼저 | 0 1개 + 중복 있음 → `INVALID_BLANK_COUNT` |

**검증 순서 정의**: `INVALID_SIZE` → `INVALID_VALUE_RANGE` → `INVALID_BLANK_COUNT` → `INVALID_DUPLICATE`

---

## 2.4 UX/출력 규칙

### 에러 메시지 표준 문구

| 에러코드 | 정확한 메시지 패턴 | 예시 |
|---|---|---|
| `INVALID_SIZE` | `"Input must be a 4x4 matrix. Got: {rows}x{cols}"` | `"Input must be a 4x4 matrix. Got: 3x4"` |
| `INVALID_BLANK_COUNT` | `"Matrix must have exactly 2 blank cells (0). Found: {count}"` | `"Matrix must have exactly 2 blank cells (0). Found: 3"` |
| `INVALID_VALUE_RANGE` | `"All values must be in range [0, 16]. Invalid value: {value} at [{row}][{col}]"` | `"All values must be in range [0, 16]. Invalid value: -1 at [2][3]"` |
| `INVALID_DUPLICATE` | `"Duplicate value {value} found at [{r1}][{c1}] and [{r2}][{c2}]"` | `"Duplicate value 5 found at [1][2] and [3][4]"` |
| `NO_SOLUTION` | `"No valid magic square solution exists for the given matrix."` | (고정 문구) |

### 문구 규칙 체크리스트

- [ ] 모든 메시지는 영어로 작성
- [ ] `{value}`, `{row}`, `{col}`, `{count}`, `{rows}`, `{cols}` 플레이스홀더를 실제 값으로 치환
- [ ] INVALID_VALUE_RANGE: 복수 위반 시 첫 번째 발견된 위반만 보고 (탐색 순서: row-major)
- [ ] INVALID_DUPLICATE: 복수 중복 쌍 발생 시 첫 번째 발견된 쌍만 보고
- [ ] NO_SOLUTION: 동적 값 없음, 고정 문구

---

# 3) Data Layer 설계

## 3.1 목적 정의

| 항목 | 내용 |
|---|---|
| 학습 목적 | Repository 패턴 + 인터페이스 분리 원칙(ISP) 훈련 |
| 저장 대상 | 입력 행렬(`Matrix4x4`), 풀이 결과(`Solution`) |
| 적용 범위 | 메모리 또는 파일 교체 가능한 수준 (DB 연동 없음) |
| 비기능 요구사항 | 구현체 교체 시 상위 레이어 코드 변경 없음 (DIP 준수) |

---

## 3.2 인터페이스 계약

### `MatrixRepository`

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `save(id: String, matrix: Matrix4x4) → void` | 식별자, 행렬 | 없음 | `id`가 null → `IllegalArgumentException` |
| `load(id: String) → Matrix4x4` | 식별자 | `Matrix4x4` | 존재하지 않는 id → `MatrixNotFoundException` |
| `exists(id: String) → boolean` | 식별자 | true/false | 없음 |
| `delete(id: String) → void` | 식별자 | 없음 | 존재하지 않는 id → `MatrixNotFoundException` |

**불변조건**: `load(id)`로 반환된 `Matrix4x4`는 `save(id, matrix)` 호출 시의 행렬과 동일해야 함

### `SolutionRepository` (선택적)

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `save(id: String, solution: Solution) → void` | 식별자, 풀이 | 없음 | `id`가 null → `IllegalArgumentException` |
| `load(id: String) → Solution` | 식별자 | `Solution` | 존재하지 않는 id → `SolutionNotFoundException` |

---

## 3.3 구현 옵션 비교

| 항목 | 옵션 A: InMemory | 옵션 B: File (JSON) |
|---|---|---|
| 저장 매체 | JVM Heap (`Map<String, Matrix4x4>`) | 로컬 파일시스템 (`.json`) |
| 영속성 | 프로세스 종료 시 소멸 | 프로세스 종료 후 유지 |
| 설정 복잡도 | 없음 | 파일 경로, 직렬화 설정 필요 |
| 테스트 격리성 | 완전 (각 테스트에서 new 인스턴스) | 테스트 후 파일 정리 필요 |
| 동시성 안전성 | `ConcurrentHashMap` 사용 시 안전 | 파일 락 처리 필요 |
| 학습 포인트 | Repository 패턴, DIP | 직렬화, IOException 처리 |
| 교체 용이성 | 인터페이스만 구현하면 즉시 교체 | 동일 |

### 추천안: **옵션 A (InMemory)**

**이유**:
1. TDD 연습 목적에서 테스트 격리성이 핵심이며, InMemory는 `setUp/tearDown` 없이 완전한 격리 보장
2. 파일 경로, IOException, 직렬화 설정 등 부수적 복잡도 없이 Repository 패턴과 DIP 훈련에 집중 가능
3. 나중에 File 구현체로 교체 시 상위 레이어 코드 무변경 검증(DIP 실습)이 가능

---

## 3.4 Data 레이어 테스트

### MatrixRepository 저장/로드 정합성

| TC ID | 시나리오 | 입력 | 기대 결과 | 보호 조건 |
|---|---|---|---|---|
| DR-01 | 저장 후 로드 동일성 | 임의 유효 행렬 저장 → 같은 id로 로드 | 행렬 값 16개 모두 일치 | 정합성 불변조건 |
| DR-02 | 같은 id 덮어쓰기 | id="A"로 행렬1 저장 → 행렬2 저장 → 로드 | 행렬2 반환 | 덮어쓰기 의미론 |
| DR-03 | exists: 저장 후 true | save 후 exists("A") | `true` | — |
| DR-04 | exists: 저장 전 false | 저장 없이 exists("X") | `false` | — |
| DR-05 | delete 후 load | save → delete → load | `MatrixNotFoundException` | — |

### 예외 처리

| TC ID | 시나리오 | 기대 예외 | 보호 조건 |
|---|---|---|---|
| DR-06 | 존재하지 않는 id로 load | `MatrixNotFoundException` | — |
| DR-07 | null id로 save | `IllegalArgumentException` | — |
| DR-08 | null id로 load | `IllegalArgumentException` | — |
| DR-09 | null matrix로 save | `IllegalArgumentException` | — |

### 불변조건 (4×4 구조 유지)

| TC ID | 시나리오 | 기대 결과 | 보호 조건 |
|---|---|---|---|
| DR-10 | 로드된 행렬의 차원 확인 | rows=4, 각 row length=4 | 4×4 불변 |
| DR-11 | 로드된 행렬은 저장 시 행렬과 동일 객체가 아님 (방어적 복사) | 참조 ≠, 값 = | 불변성 보호 |

---

# 4) Integration & Verification (통합 및 검증)

## 4.1 통합 경로 정의

```
호출자
  │
  ▼ (외부 계약: InputContract)
[UI Boundary Layer]
  │  검증 통과
  ▼ (내부 계약: Matrix4x4)
[Domain Layer: MagicSquareSolver]
  │  solve() 결과
  ▼ (내부 계약: Solution)
[UI Boundary Layer]
  │  직렬화
  ▼ (외부 계약: int[6])
호출자

              ↕ (선택적)
       [Data Layer: MatrixRepository]
         save(id, matrix) / load(id)
```

### 의존성 방향 규칙

| 규칙 | 내용 |
|---|---|
| UI → Domain | UI는 Domain 인터페이스에 의존 (구현체 X) |
| Domain → Data | Domain은 `MatrixRepository` 인터페이스에 의존 (구현체 X) |
| Data ← UI | Data는 UI를 모름 (역방향 의존 금지) |
| Domain ← UI | Domain은 UI를 모름 (역방향 의존 금지) |

---

## 4.2 통합 테스트 시나리오

### 정상 시나리오

#### IT-S-01: 조합A 순서로 풀리는 마방진

- **설명**: 작은 누락 숫자를 첫 번째 빈칸에, 큰 숫자를 두 번째 빈칸에 배치하면 마방진이 되는 경우
- **경로**: 유효 입력 → UI 검증 통과 → Domain solve() → 조합A 성공 → `int[6]` 반환
- **전제조건**: 입력 행렬은 INV-06, INV-07, INV-08 만족, 실제 마방진에서 두 수를 제거한 것
- **검증 항목**:
  - [ ] 반환 배열 길이 = 6
  - [ ] r1, c1, r2, c2 ∈ {1..4}
  - [ ] n1 < n2
  - [ ] 결과를 원래 행렬에 적용 시 `MagicSquareValidator.validate() == true`

#### IT-S-02: 조합B 순서로만 풀리는 마방진

- **설명**: 조합A는 마방진 불만족, 조합B(큰 수 → 첫 번째 빈칸)만 마방진이 되는 경우
- **경로**: 유효 입력 → UI 검증 통과 → Domain solve() → 조합A 실패 → 조합B 성공 → `int[6]` 반환
- **검증 항목**:
  - [ ] n1 > n2 (큰 수가 첫 번째 빈칸)
  - [ ] 결과를 원래 행렬에 적용 시 `MagicSquareValidator.validate() == true`

#### IT-S-03: Data Layer 저장 후 로드 재풀이

- **설명**: 입력 행렬을 저장 → 로드 → 재풀이 결과가 최초 풀이와 동일한 경우
- **경로**: 유효 입력 → Domain solve() → Data save() → Data load() → Domain solve()
- **검증 항목**:
  - [ ] 두 번의 solve() 결과 `int[6]` 값이 완전히 동일

### 실패 시나리오

#### IT-F-01: 입력 크기 오류 (UI 차단)

- **설명**: 3×4 행렬 제출
- **경로**: 입력 → UI `INVALID_SIZE` 에러 반환, Domain 미호출
- **검증 항목**:
  - [ ] 에러코드 = `INVALID_SIZE`
  - [ ] 메시지 = `"Input must be a 4x4 matrix. Got: 3x4"`
  - [ ] Domain `solve()` 호출 횟수 = 0 (Mock 검증)

#### IT-F-02: 빈칸 개수 오류 (UI 차단)

- **설명**: 0이 3개인 4×4 행렬 제출
- **경로**: 입력 → UI `INVALID_BLANK_COUNT` 에러 반환, Domain 미호출
- **검증 항목**:
  - [ ] 에러코드 = `INVALID_BLANK_COUNT`
  - [ ] 메시지 = `"Matrix must have exactly 2 blank cells (0). Found: 3"`

#### IT-F-03: 중복 값 오류 (UI 차단)

- **설명**: 0 제외 값 중 5가 2곳에 있는 4×4 행렬 제출
- **경로**: 입력 → UI `INVALID_DUPLICATE` 에러 반환, Domain 미호출
- **검증 항목**:
  - [ ] 에러코드 = `INVALID_DUPLICATE`
  - [ ] 메시지에 위반 값(5)과 좌표 포함

#### IT-F-04: 도메인 해 없음

- **설명**: 형식은 유효하나 어떤 조합도 마방진을 만들지 못하는 입력
- **경로**: 유효 입력 → UI 검증 통과 → Domain `NoSolutionException` → UI `NO_SOLUTION` 반환
- **검증 항목**:
  - [ ] 에러코드 = `NO_SOLUTION`
  - [ ] 메시지 = `"No valid magic square solution exists for the given matrix."`

#### IT-F-05: Data Layer 로드 실패

- **설명**: 존재하지 않는 id로 load 시도
- **경로**: Data `load("nonexistent")` → `MatrixNotFoundException` 발생
- **검증 항목**:
  - [ ] `MatrixNotFoundException` 전파
  - [ ] 상위 레이어로 예외 전파 방식 확인

---

## 4.3 회귀 보호 규칙

### 기존 테스트 유지 정책

| 규칙 ID | 규칙 내용 | 위반 시 처리 |
|---|---|---|
| REG-01 | 모든 기존 단위 테스트는 리팩토링 후에도 통과해야 함 | CI 빌드 실패 |
| REG-02 | 기존 테스트를 삭제하려면 대체 테스트를 먼저 추가해야 함 | PR 리뷰 차단 |
| REG-03 | 테스트 더블(Mock/Stub) 교체 시 계약 동작은 동일하게 유지 | 계약 테스트로 검증 |

### 변경 금지 규칙

| 항목 | 변경 금지 내용 |
|---|---|
| 입력 계약 | `int[][]` 4×4, 0 정확히 2개, 값 0 또는 1~16, 중복 금지 |
| 출력 계약 | `int[6]`, 1-indexed 좌표, INV-10 순서 규칙 |
| 에러 메시지 패턴 | 2.4의 정확한 문구 규칙 (플레이스홀더 포함) |
| 에러코드 enum 값 | `INVALID_SIZE`, `INVALID_BLANK_COUNT`, `INVALID_VALUE_RANGE`, `INVALID_DUPLICATE`, `NO_SOLUTION` |
| Magic Constant | 34 (변경 불가) |
| 검증 순서 | `SIZE` → `VALUE_RANGE` → `BLANK_COUNT` → `DUPLICATE` |

---

## 4.4 커버리지 목표

| 레이어 | 커버리지 목표 | 측정 대상 |
|---|---|---|
| Domain Logic | **95% 이상** | `BlankLocator`, `MissingNumberDetector`, `MagicSquareValidator`, `CombinationEvaluator`, `MagicSquareSolver` |
| UI Boundary | **85% 이상** | 검증 로직, 에러 생성, 출력 직렬화 |
| Data Layer | **80% 이상** | `MatrixRepository` 구현체 (InMemory) |

### 커버리지 측정 기준

| 기준 | 내용 |
|---|---|
| 커버리지 종류 | Line Coverage + Branch Coverage 모두 충족 |
| 예외 경로 | `catch` 블록, 예외 생성 코드도 커버리지에 포함 |
| 제외 대상 | 순수 Value Object getter, `toString`, `equals`, `hashCode` |

---

## 4.5 Traceability Matrix (추적성 행렬)

| Concept (Invariant) | Rule | Use Case | Contract (API) | Test | Component |
|---|---|---|---|---|---|
| **INV-01** 행 합 = 34 | 4개 행 각각 검사 | UC-03 마방진 판정 | `MagicSquareValidator.rowSum()`, `validate()` | MV-01, MV-02, MV-07, MV-08 | `MagicSquareValidator` |
| **INV-02** 열 합 = 34 | 4개 열 각각 검사 | UC-03 마방진 판정 | `MagicSquareValidator.colSum()`, `validate()` | MV-01, MV-03 | `MagicSquareValidator` |
| **INV-03** 주대각선 합 = 34 | (1,1),(2,2),(3,3),(4,4) 합 | UC-03 마방진 판정 | `MagicSquareValidator.mainDiagSum()`, `validate()` | MV-01, MV-04, MV-06 | `MagicSquareValidator` |
| **INV-04** 반대각선 합 = 34 | (1,4),(2,3),(3,2),(4,1) 합 | UC-03 마방진 판정 | `MagicSquareValidator.antiDiagSum()`, `validate()` | MV-01, MV-05, MV-06 | `MagicSquareValidator` |
| **INV-05** 1~16 완전성 | 완성 행렬에 1~16 각 1회 | UC-02 누락 숫자 찾기 | `MissingNumberDetector.findMissing()` | MD-01~05 | `MissingNumberDetector` |
| **INV-06** 빈칸 수 = 2 | 0의 개수 정확히 2 | UC-01 빈칸 찾기 | UI: `InputContract.zero_count` / Domain: `BlankLocator.findBlanks()` | BL-05,06,07 / UI-BC-01~04 | `UI Boundary`, `BlankLocator` |
| **INV-07** 값 범위 [0,16] | 각 셀 값 0≤v≤16 | — | UI: `InputContract.cell_value` | UI-VR-01~05 | `UI Boundary` |
| **INV-08** 비중복 | 0 제외 값 유일 | — | UI: `InputContract.uniqueness` | UI-DU-01~03 | `UI Boundary` |
| **INV-09** 빈칸 탐색 순서 | 행 우선, 좌→우 | UC-01 빈칸 찾기 | `BlankLocator.findBlanks()` 사후조건 | BL-01~04 | `BlankLocator` |
| **INV-10** 출력 순서 규칙 | 조합A 우선 시도, 실패 시 조합B | UC-04 두 조합 시도 | `CombinationEvaluator.evaluate()`, `OutputContract.ordering_rule` | CE-01,02 / UI-FMT-01~03 | `CombinationEvaluator`, `UI Boundary` |
| **Data 정합성** | save→load 동일성 | UC-05 (선택) | `MatrixRepository.save/load` | DR-01,02,10,11 | `MatrixRepository` |
| **검증 순서** | SIZE→VR→BC→DUP 순 | — | UI 에러 우선순위 규칙 | UI-ORD-01~03 | `UI Boundary` |
| **에러 문구** | 정확한 패턴+플레이스홀더 | — | `ErrorContract.message` | IT-F-01~04 | `UI Boundary` |

---

### 설계 완결성 체크리스트

**Domain Layer**
- [ ] 모든 Domain API가 메서드 시그니처 + 사전/사후조건 + 실패조건을 가짐
- [ ] 모든 Invariant(INV-01~10)에 대응하는 테스트 케이스가 존재함
- [ ] 모든 테스트 케이스가 보호하는 Invariant가 명시됨
- [ ] 구현 코드 없음

**UI Layer**
- [ ] 모든 에러코드가 정확한 메시지 패턴을 가짐
- [ ] 검증 순서가 명시되고 테스트로 검증됨
- [ ] Domain을 Mock으로 대체한 테스트 케이스가 존재함
- [ ] 반환 포맷 검증 테스트가 존재함

**Data Layer**
- [ ] 인터페이스 계약이 구현체 기술 중립적임
- [ ] 방어적 복사(DR-11) 테스트가 존재함
- [ ] 추천 구현 옵션에 선택 이유가 명시됨

**Integration**
- [ ] 정상 시나리오 3개, 실패 시나리오 5개 정의됨
- [ ] 모든 변경 금지 항목이 명시됨
- [ ] Traceability Matrix가 Invariant → Test → Component까지 연결됨
- [ ] 커버리지 목표가 레이어별로 수치로 명시됨

---

**User**

Report 폴더에 "02"로 시작하는 이름으로 지금 작업한 내용을 보고서로 내보내줘

---

**Cursor**

`Report\02-4x4-magic-square-tdd-clean-architecture-design.md` 파일로 내보냈습니다.

기존 `01-...` 파일과 같은 폴더에 저장되었으며, 이번 대화에서 설계한 전체 내용이 포함되어 있습니다:

| 섹션 | 주요 산출물 |
|---|---|
| 1) Domain Layer | Invariants(INV-01~10), Domain API 계약, 단위 테스트 30개 |
| 2) UI Boundary Layer | Input/Output/Error Schema, UI 테스트 26개, 에러 문구 표준 |
| 3) Data Layer | `MatrixRepository` 인터페이스 계약, InMemory 추천 근거, 테스트 11개 |
| 4) Integration | 통합 경로, 정상 3 / 실패 5 시나리오, 회귀 보호 규칙, 커버리지 목표, Traceability Matrix |

