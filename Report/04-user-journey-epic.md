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
