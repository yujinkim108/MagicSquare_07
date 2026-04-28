# Magic Square 4×4 — 구현 To-Do

이 문서는 **구현 작업 보드**이다. 요구사항·수용 기준의 **정본**은 아래를 따른다.

| 정본 | 경로 |
|------|------|
| 범위·스토리 요약 | [`PRD.md`](./PRD.md) (특히 §2, §5) |
| User Story·AC·컴포넌트 | [`Report/04.3-user-journey-stories.md`](../Report/04.3-user-journey-stories.md) |
| 도메인·CLI·에러코드·검증 순서 | [`Report/02-4x4-magic-square-tdd-clean-architecture-design.md`](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md) |

**권장 구현 순서:** US-01 → US-02 / US-03 (병행 가능) → US-04 → US-05.

---

## Phase 0 — 저장소·품질 게이트

- [ ] Python 3.10+, `pyproject.toml`, pytest·coverage·formatter·linter 정렬 ([`Report/03-cursorrules-setup.md`](../Report/03-cursorrules-setup.md) 참고)
- [ ] 소스 패키지 구조 (예: `entity` / `control` / `boundary`) 및 `tests/` 분리

---

## US-01 — 입력 검증·보드 표현

- [ ] 4×4, `0` 정확히 2개, 셀 값 `0..16`, 0 제외 중복 없음 (04.3 AC-1.1~1.4)
- [ ] Boundary: 검증 순서 `INVALID_SIZE` → `INVALID_VALUE_RANGE` → `INVALID_BLANK_COUNT` → `INVALID_DUPLICATE` ([02 §2.3](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))
- [ ] Entity: 부분 격자 표현 (`Matrix4x4` 등) — 도메인으로 넘기기 전 스키마 통과

---

## US-02 — 빈칸 탐색

- [ ] `0` 칸 좌표를 row-major 순으로 2개 반환 (04.3 AC-2.1~2.2)
- [ ] `BlankFinder` / 설계서 상 `BlankLocator` 역할 정합 ([02 §1.4 BlankLocator](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))

---

## US-03 — 누락 숫자

- [ ] 1~16 중 나타나지 않은 수 **2개**, **오름차순** (04.3 AC-3.1~3.2)
- [ ] `MissingNumberFinder` / `MissingNumberDetector` 역할 정합 ([02 §1.4](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))

---

## US-04 — 마방진 판정 (완성 격자)

- [ ] 행·열·두 대각선 Magic sum(34)·1~16 순열 (04.3 AC-4.1~4.5, PRD §5 US-04)
- [ ] `MagicSquareValidator` / `rules` — 완성 격자만 판정 (0 없음)

---

## US-05 — 두 조합 시도·풀이

- [ ] 작은 수→첫 row-major 빈칸, 큰 수→둘째; 실패 시 역순 (04.3 AC-5.1~5.5)
- [ ] 성공 시 6원소 `[r,c,v,r,c,v]`, 좌표 **1-index** ([02 OutputContract](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))
- [ ] 두 조합 모두 실패 시 `NO_SOLUTION` 등 계약에 맞는 실패 표현 ([02 ErrorContract](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))
- [ ] Control: `Solver` / `CombinationEvaluator` + `MagicSquareSolver` 오케스트레이션 ([02 §1.1](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))

---

## Dual-Track·통합

- [ ] **UI(경계):** CLI에서 에러 메시지 패턴·종료 코드 RED ([02 §2.4](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))
- [ ] **Logic:** Entity·Control 단위 테스트 — Solver Mock으로 Boundary 분리 ([02 §2.1 흐름](../Report/02-4x4-magic-square-tdd-clean-architecture-design.md))
- [ ] ECB 의존 방향: Boundary → Control → Entity ([`PRD.md` §6.1](./PRD.md))

---

## 비기능 (NFR)

- [ ] 테스트 커버리지: 전체 **≥80%**, 도메인 목표 **95%** ([`PRD.md` §8](./PRD.md))
- [ ] 매직 넘버 금지 — `entity/constants` 등 ([PRD §4 INV-09](./PRD.md))

---

*상위 Epic·여정: [`Report/04.1-user-journey-epic.md`](../Report/04.1-user-journey-epic.md), [`Report/04.2-user-journey-level2.md`](../Report/04.2-user-journey-level2.md). Gherkin·검증: [`Report/04.4-level4-implementation-scenario-technical.md`](../Report/04.4-level4-implementation-scenario-technical.md), [`Report/04.5-level5-scenario-verification.md`](../Report/04.5-level5-scenario-verification.md).*
