# MagicSquare — Product Requirements Document (PRD)

**문서 유형:** 제품·프로젝트 요구사항 통합  
**최종 정리:** 2026-04-27  
**원천:** `Report/` · `Prompting/` 산출물(문제 정의, TDD·ECB 설계, 사용자 여정, Gherkin, 검증, `.cursorrules` 가이드)

이 문서는 **구현을 대체하는 스펙**이 아니라, **목표·범위·계약·성공 기준**을 한곳에 모은 **요구사항 계층**이다. 상세한 테스트 ID·스냅샷 전문은 개별 `Report/*.md`를 **source of truth**로 둔다.

---

## 1. 제품 개요

### 1.1 비전 (Epic)

| 항목 | 내용 |
|------|------|
| **Epic** | Invariant(불변조건) 기반 사고 훈련 시스템 구축 |
| **핵심** | 4×4 Magic Square를 도구로, **규정을 쪼개고 이름을 붙이고 누락 없이 적용**하는 사고·**Dual-Track TDD**·**ECB**·**계약 명확화**를 훈련한다. |

### 1.2 문제 정의(요지)

- **표면(부적절):** “4×4에 1~16을 넣어 행·열·대각 합이 같게 **만든다**”만으로는 행위자, 종료 조건, 부분 vs 완성, 검증 vs 탐색이 구분되지 않는다.  
- **정식:** (1) 1~16·4×4 **배치**가 **마방진 규칙을 만족하는지 판정**하는 규칙을 **반복 가능**하게 둔다. (2) 그 위에서 “만족하는 배치를 **약속한 수**만큼 찾는 **절차**”는 **끝나는 기준·중간 의미**를 **미리** 정한 뒤 다룬다.

**훈련에 쓰는 사고(한 줄):** 규정을 쪼개고, 약속을 밖에 두고, 누락 없이 적용한다.

### 1.3 왜 4×4인가

- 3×3: 본질해가 거의 하나라 설계·탐색의 여지가 작다.  
- 4×4: 본질해 다양(예: 880) — **탐색·가지치기·알고리즘 선택**이 의미 있다.  
- 5×5 이상: 해 공간이 커 **완전 탐색·제약 비교** 실험대로는 4×4가 적절하다.

### 1.4 왜 프로그램·TDD인가

- **프로그램:** 절차의 **재현성**, **검증 자동화**, 실수·누락의 조기 발견, **규칙을 실행 가능한 형태**로 고정.  
- **TDD:** **정확성 정의**, **모듈·계약 경계**, “유효하다” vs “해를 찾는다” **분리**, 리팩터 후 **의미 유지**. **입·출력이 분명해야** RED가 **의미 있는 실패**를 남긴다.

---

## 2. 범위 (Scope)

### 2.1 In Scope

- 4×4 Magic Square **도메인** 엔티티·불변조건, **입력 검증** 계약, **마방진 판정**, **부분 격자(빈칸 2개·`0`) 완성** 흐름(아래 [§5 User Stories](#5-기능-요구사항-user-stories) 및 설계서와 정합).  
- **ECB**(Entity–Control–Boundary) 기반 구조, **CLI** 등 경계 입출력.  
- **테스트:** pytest, AAA, 커버리지 하한(프로젝트 규칙: **최소 80%**, 도메인 목표 **95%**).  
- **`.cursorrules`**에 따른 **TDD 3페이즈**, 코딩·금지 패턴·구조 규율.

### 2.2 Out of Scope

- GUI / Web UI(학습용 범위 밖).  
- **DB 영속** — 별도 `Report`는 **Repository 인터페이스 + InMemory** 수준의 학습 옵션만 언급(ECB `Report/02`…).  
- 5×5 이상, 분산·비동기(명시적 범위 밖).

### 2.3 소스 문서 맵 (Level 1~5)

| Level | 주요 파일 | 요약 |
|------|-----------|------|
| 1 | `04-user-journey-epic.md` | Epic, INV-01~10(Epic), 성공 기준, ECB 역할 |
| 2 | `05-user-journey-level2.md` | Persona, Step 1~5, Pitfall, Dual-Track, 회귀 |
| 3 | `06-user-journey-stories.md` | US-01~05, AC, 컴포넌트·의존 |
| 4 | `08-level4-implementation-scenario-technical.md` | Gherkin Feature, 기술 약속, 시나리오·검산 주의 |
| 5 | `09-level5-scenario-verification.md` | 일관성·엣지·갭, Sign-off |

통합 **스냅샷:** `04-magic-square-user-journey-Levels-1-5-Export-Report.md` (개별 파일이 **정본**).  
**문제 정의·TDD 설계·cursorrules 보고:** `01`~`03` — `PRD`의 [§1](#1-제품-개요)·[§6](#6-아키텍처·의존성)과 연동.

**Prompting** 폴더(`*_prompt.md`)는 위 Report를 생성·내보내는 데 쓰인 **대화/지시 흔적**이며, 요구사항 본문은 **Report**와 동일 선상의 내용을 반영한다.

---

## 3. 사용자·페르소나 (요약)

| 항목 | 내용 |
|------|------|
| **역할** | 소프트웨어 개발 **학습자** |
| **맥락** | TDD·Clean/ECB 학습 중 |
| **불안** | “무엇을 테스트해야 할지” 모호함 |
| **성공** | Invariant·계약이 **먼저** 오고 구현·테스트가 **뒤따르는** 순서가 **자연스럽**게 된다. |

**여정(고수준):** 문제 인식(Invariant) → **계약** 정의 → **도메인 분리** → **Dual-Track** RED→GREEN→REFACTOR → **회귀**(엣지·오류·조합 실패).  
— 상세: `05-user-journey-level2.md`.

---

## 4. 핵심 Invariant (Epic 기준, INV-01~10)

Epic 문서(`04-user-journey-epic.md`)의 **Inv**는 **훈련·추적**에 초점을 둔다(격자·숫자·완성 시 합·부분/완성 구분·상수·테스트 링크).

| ID | 요지 |
|----|------|
| INV-01 | 격자 **4×4**, 16칸 |
| INV-02 | 값 **1~16** (완성 맥락; **부분 격자**는 `0`·계약에 따라 `Report/06`·`02`와 병기) |
| INV-03 | **완성** 시 1~16 **순열** |
| INV-04~07 | Magic sum **34**, 행·열·**두** 대각 |
| INV-08 | **부분(Partial)** vs **완성(Complete)** — 이름·계약 분리 |
| INV-09 | Magic sum 등 **하드코딩 금지** — `entity/constants` 등 **명명 상수** |
| INV-10 | Invariant → Test **추적**(docstring `Invariant: INV-XX` 등) |

> **주의:** `02-4x4-magic-square-tdd-clean-architecture-design.md`의 **INV-01~10**은 *도메인/경계 implementation* 쪽 **별도 ID 체계**(행열합·빈칸 수·범위 등)로, Epic INV와 **번호가 1:1로 동일하지 않을 수 있다**. 구현·트레이싱 시 **문서별 표를 대조**할 것.

---

## 5. 기능 요구사항 (User Stories, US-01~05)

`06-user-journey-stories.md`가 **수용 기준**의 **정본**에 가깝다. 아래는 PRD용 압축.

### US-01 — 입력 검증

- **As a** 학습자, **I want** 4×4, **빈칸(0) 2개**, 1~16(빈칸 제외) **범위·중복** 규칙 검증, **so that** 잘못된 데이터가 도메인으로 **넘어가지 않**게.  
- **AC 요지:** 크기, 빈칸 개수, 0이 아닌 값의 범위·중복(부분 퍼즐 **명시**와 INV-08 정합).

### US-02 — 빈칸 탐색

- `0` 위치를 **row-major**로 **2개** 반환.

### US-03 — 누락 숫자

- 1~16 중 **누락 2개**, **오름차순**.

### US-04 — 마방진 판정

- **완성** 격자에 대해 행·열·대각 **Magic sum**, 및 **1~16 순열**(권장·INV-03 정합).

### US-05 — 두 조합(순·역) 시도

- 작은 수→**첫** row-major 빈칸, 큰 수→**둘째**; 실패 시 **역**.  
- 성공 응답: **6원소** `[r,c,v,r,c,v]`, **좌표 1-index** (`02`·`08` 기술 약속과 정합). **최대 2번** 완성 시도(이 Story 범위).

**의존(권장):** US-01 → US-02/US-03 → US-04 → US-05.

---

## 6. 아키텍처·의존성

### 6.1 ECB (프로젝트 규칙)

- **entity:** 도메인 모델·불변·순수 규칙. **entity는 control/boundary에 의존하지 않는다.**  
- **control:** 유스케이스(생성·검증·풀이 등 **흐름**). **boundary에 의존하지 않는다.**  
- **boundary:** CLI, 포맷, **1차 입력 검사**, 결과 직렬화. **entity를 직접 참조하지 말고 control을 경유**하는 것이 `.cursorrules` / `03-cursorrules-setup` 정신이다.

**Dual-Track TDD (요지):**  
- **Track A (Contract):** 입출력·예외가 Invariant와 **일치**; 알고리즘 변경 후에도 유지.  
- **Track B (Algorithm):** 백트래킹·CSP 등 **내부** 전략; 리팩터 시 **바뀌어도 되는** 층.

### 6.2 설계서의 핵심 I/O (2-blank 퍼즐, `02`)

- **입력:** `4×4` `int[][]`, **0 정확히 2**, 셀 값 `0..16`, 0 제외 **중복 없음**.  
- **출력(성공):** `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 1-based 좌표, **조합A(작·큰 순)**이 해이면 `n1 < n2` 정렬, 아니면 **역** — `INV-10`/`OutputContract.ordering_rule` (`02` §1.2, 2.2).  
- **에러코드(예):** `INVALID_SIZE`, `INVALID_BLANK_COUNT`, `INVALID_VALUE_RANGE`, `INVALID_DUPLICATE`, `NO_SOLUTION` + **고정/패턴** 메시지(`02` §2.4).  
- **검증 순서(경계):** `SIZE` → `VALUE_RANGE` → `BLANK_COUNT` → `DUPLICATE` (`02` §2.3).  
- **Data (선택):** `MatrixRepository` 등 — **InMemory** 추천(테스트 격리·DIP 학습) (`02` §3).

**도메인 컴포넌트(이름 예):** `Matrix4x4`, `Cell`, `MissingPair`, `Solution`; `BlankLocator`, `MissingNumberDetector`, `MagicSquareValidator`, `CombinationEvaluator`, `MagicSquareSolver` (`02` §1.1).

### 6.3 코드·품질 규칙 (`.cursorrules` 요지, `03`)

- **Python 3.10+**, **Black(88)**, **PEP8**, **타입힌트 전면**, **Google docstring**(public).  
- **TDD:** `red` / `green` / `refactor`, 각 **must_not** 준수.  
- **금지:** `print` (대신 `logging`), **bare** `except`, **매직 넘버/문자열**, ECB **역의존**, **타입 없는** public API 등.  
- **테스트:** pytest, **최소 커버 80%**, `fail_under` 등 `pyproject`·규칙에 따름.

---

## 7. BDD / Level 4 (Gherkin)

- **Feature:** 4×4 **부분** 마방진 **완성** (`08-level4-implementation-scenario-technical.md`).  
- **Background:** 4×4, `0`=빈칸, **빈칸 2**, 1~16, 중복·범위, magic **34** — 상수는 코드에서 **명명** (`08` § 기술 약속).  
- **시나리오:** 1차(작→큰) **성공**, **역** 성공, 빈칸/중복/범위 **검증 실패** 등.

**알려진 갭 (Level 5, G1):** `08`에 쓰인 **동일 예시 격자**는 수식상 **(작은→첫 빈칸, 큰→둘째) 성공**과 **역 성공**을 **한 표**로 **동시에** 만족시키지 못할 수 있음. **시나리오 1/2**는 **서로 다른 Given**·**Scenario Outline**·검산된 **픽스처**로 분리할 것 (`08`·`09`).

---

## 8. 비기능 요구 (NFR) · 품질 목표

| 항목 | 목표(문서 기준) |
|------|------------------|
| 커버리지 | **전체 ≥80%**; **도메인 로직 95%** (Epic·`02` 정합) |
| 계약 테스트 | 입력 검증 100% 통과(마커 `@pytest.mark.contract` 등, Epic) |
| 상수 | 매직 넘버 0(명명·`constants`) |
| 추적 | INV-01~10 ↔ 테스트(문서화) |
| 회귀 | 기존 삭제·대체·스킵 금지 정책 (`02` REG, `05` Step 5) |
| BDD/CI | pytest-bdd·black·mypy·isort — **도입은 선택/미체크**(`09` §1.3~1.4) |

---

## 9. Level 5 검증 요약 (오픈 이슈)

| ID | 내용 | 조치(권장) |
|----|------|------------|
| G1 | Gherkin `08` **동일 Given**·시나리오 1·2 **검산 불일치** | Given **분리**, Outline, 확인된 **데이터** 파일 |
| G2 | 멘토/동료 **리뷰** 미이행 | 일정 1회 |
| G3 | BDD **자동 러너** 미연동 | Step Def 구현 시 **자동화** 체크 [x] |

**Sign-off** (선택): Story·Gherkin / 엣지·테스트 / ECB·TDD (`09` §4).

---

## 10. 용어

| 용어 | 설명 |
|------|------|
| **Dual-Track TDD** | Contract 테스트 트랙 + Algorithm 트랙 |
| **Invariant** | 주어진 범위·단계에서 **항상** 만족해야 할 조건 |
| **ECB** | Entity–Control–Boundary |
| **2-blank 퍼즐** | 0 **2칸**·나머지 14칸 + 누락 2수·**순·역** 2회 시도 (`02`·`06`·`08`) |

---

## 11. 원천 인덱스 (Report + Prompting)

| 경로 | 역할 |
|------|------|
| `Report/01-4x4-magic-square-problem-definition.md` | STEP1~5 문제 정의(구현·알고리즘 없음) |
| `Report/02-4x4-magic-square-tdd-clean-architecture-design.md` | Domain·UI·Data·통합, INV/API/TC ID, **계약** |
| `Report/03-cursorrules-setup.md` | `.cursorrules` 8섹션 설계 메모 |
| `Report/04-user-journey-epic.md` | Level 1 Epic |
| `Report/05-user-journey-level2.md` | Level 2 Journey 5 Step |
| `Report/06-user-journey-stories.md` | Level 3 **US-01~05** |
| `Report/08-level4-implementation-scenario-technical.md` | Level 4 Gherkin |
| `Report/09-level5-scenario-verification.md` | Level 5 체크리스트·갭 |
| `Report/04-magic-square-user-journey-Levels-1-5-Export-Report.md` | L1~L5 **병합 스냅샷** (머리말+부록) |
| `Prompting/01-4x4-magic-square-problem-definition-prompt.md` | `01` Report 대화·내보내기 |
| `Prompting/02-4x4-magic-square-tdd-clean-architecture-design-prompt.md` | `02` Report 대화·내보내기 |
| `Prompting/03-cursorrules-setup-prompt.md` | `03` Report 대화·내보내기 |
| `Prompting/04-magic-square-user-journey-Levels-1-5-Export-Report-prompt.md` | Epic~Level5+통합 `04` 내보내기 대화 |

---

*이 PRD는 `Report/`, `Prompting/`에 있는 `*.md`를 읽고 요약·정렬한 것이며, 수치·ID·에러문구·검산은 **최신 원문**을 우선한다.*
