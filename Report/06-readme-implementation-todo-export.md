# 06 · README·구현 To-Do·아키텍트 보드 내보내기

**최초:** 2026-04-28  
**최종 갱신:** 2026-04-28 (README `To-Do List` 대폭 보강·본 보고서 정렬)  
**작업 유형:** **문서 작업** — To-Do 참조 가이드, TDD/ECB·To-Do→Work Order 구조, `README.md`, `docs/IMPLEMENTATION-TODO.md` 생성·정리  
**워크스페이스:** `c:\DEV\MagicSquare_07` (MagicSquare_07)

**파일명 이력:** 초안 파일명 `06-cursor-session-readme-todo-board-export.md` 는 **도구 중심 표현**을 피하기 위해 **`06-readme-implementation-todo-export.md`** 로 변경되었다.

---

## 1. 작업 개요

문서·설계 대화에서 수행한 내용을 한 보고서로 묶는다.

| # | 내용 | 결과 |
|---|------|------|
| 1 | **To-Do 리스트를 무엇을 보고 쓸지** 안내 | 정본: `docs/PRD.md` + `Report/04.3-user-journey-stories.md` + `Report/02-...` ; 상세 Phase 보드는 `docs/IMPLEMENTATION-TODO.md` |
| 2 | **시니어 아키텍트·TDD 코치** 관점 **구현용 To-Do 구조** (Epic-001, US-001~005, TASK-xxx, RED/GREEN/REFACTOR, Scenario L0~L3, ECB, Dual-Track) | **초안** — 본 보고서 §4·과거 대화; 전체 TASK 표는 저장소에 **별도 파일로 미작성** (필요 시 `docs/` 분할) |
| 3 | **README.md에 To-Do 포함** 시 어떤 문서를 볼지·슬라이드 **To-Do → Work Order** 개념 반영 | PRD / 04.3 / 02 / **판단(Decision) 기반** WO — 아래 §3·§5 |
| 4 | **`README.md` + `docs/IMPLEMENTATION-TODO.md`** | 루트·`docs/`에 유지; README **§ To-Do List**에 **TD-1~7**·**WO-1.1~7.3** 전개 |
| 5 | **README To-Do 대폭 보강** | `Traceability`, 상위 **TD-1~7**·**WO-1.1~7.3** 테이블(1:N), GUI Out of scope → CLI/Boundary 대응 명시 |

**구현 코드(Python 패키지)** 는 이 문서 범위에서 **추가하지 않음** (문서·보드만).

---

## 2. To-Do 작성 시 참조 문서 (합의)

| 목적 | 권장 문서 | 비고 |
|------|-----------|------|
| 범위·스토리·NFR 한눈에 | `docs/PRD.md` | §2 범위, §5 US-01~05, §8 NFR |
| User Story·AC·컴포넌트 **정본** | `Report/04.3-user-journey-stories.md` | US-01~05, 담당 컴포넌트 |
| 도메인·CLI·에러코드·검증 순서 | `Report/02-4x4-magic-square-tdd-clean-architecture-design.md` | ErrorContract, Input/Output, UI 검증 순서, TC ID |
| Epic·여정 | `Report/04.1-user-journey-epic.md`, `04.2-user-journey-level2.md` | |
| L1~L5 통합 읽기 | `Report/04-magic-square-user-journey-Levels-1-5-Export-Report.md` | 개별 `Report`가 **정본** |
| 프롬프트 흔적만 | `Prompting/*.md` | 요구사항 본문으로 쓰지 않음 |

**파일명 정리:** PRD·옛 표에는 `06-user-journey-stories.md` 등이 나올 수 있다. 본 저장소의 Level 3 User Stories **실제 경로**는 **`Report/04.3-user-journey-stories.md`** 이다.

---

## 3. 산출 파일 (저장소, 최종 갱신 기준)

| 경로 | 설명 |
|------|------|
| **`README.md`** | 프로젝트 소개, 범위, 문서 지도, ECB·Dual-Track, US-01~05 표, **`## To-Do List`**(§ Traceability, **TD-1~7** 상위 체크, **WO-1.1~7.3** 검증 계약 표), `docs/IMPLEMENTATION-TODO.md`·본 `Report/06-…` 링크, 빠른 시작(placeholder) |
| **`docs/IMPLEMENTATION-TODO.md`** | Phase 0, US-01~05, Dual-Track, NFR **체크리스트** (04.3·02·PRD 링크) — README의 TD/WO와 **역할이 다름**([§5](#5-readmemd-vs-그-밖의-문서-역할-정리)) |

**README 링크 주의:** `README.md`는 **저장소 루트**이므로 `docs/PRD.md` 등은 `docs/...` 상대 경로로 기술한다.

### 3.1 `README.md` To-Do List에 반영된 방법론 (슬라이드·PRD 정합)

| 개념 | README에 적힌 요지 | 출처/근거 |
|------|--------------------|-----------|
| **To-Do → Work Order** | **판단(Decision)**(허용/거부·반환·에러코드)이 있는 단위만 **검증 계약**으로 쪼갬 | 협업 슬라이드「1.1 To-Do → Work Order」; PRD §3.1(결정·UX Contract) |
| **1 : N** | 상위 To-Do 하나에 Work Order·테스트·RED가 **여러 개** 붙을 수 있음 | 동 슬라이드 |
| **비판정 작업** | 명명·폴더 정리·순수 리팩터 등 **판단이 없는** 일은 WO/테스트에 **억지 매핑하지 않아도** 됨 | 대화 합의 |
| **GUI vs 본 프로젝트** | **GUI/Web Out of scope**(PRD §2.2); «격자 UI」에 해당하는 표현은 **CLI/Boundary**(입력 수신·성공/실패·6원자 출력)로 **Dual-Track UI** 측에 둠 | PRD, README 본문 |

### 3.2 식별자 체계 (README)

| 식별자 | 의미 | 04.3/PRD 매핑 |
|--------|------|---------------|
| **TD-1 ~ TD-7** | **상위 To-Do** — 무엇을 “완료”로 볼지(마일스톤) | US-01~05 + Boundary(TD-6) + NFR(TD-7) |
| **WO-1.1 ~ WO-1.4** 등 | **Work Order** — ECB별 **검증·판단** 한 덩이 | 02 `INVALID_*` 순서, `OutputContract`, TC 그룹(UI-SZ, BL, MD, …) |
| (과거 대화) **TASK-0xx** | 미세 TDD 사이클(RED/GREEN/REFACTOR) | 별도 파일에 두지 않으면 **대화·본 보고서 §4**만 참고 |

**WO 번호 규칙:** `WO-{TD번호}.{일련}` — 예: `WO-1.2` = TD-1(US-01)의 두 번째 Work Order.

---

## 4. «구현용 To-Do 보드» 구조 (TASK·Phase — 대화상 요약)

다음은 시니어 아키텍트 응답에서 정의한 **Epic / US / Phase / Task** 골격이다. **TASK-001~** 전문 표는 길어 **README에는 TD/WO로 이식**되었고, **전체 Task 번호대**는 아래·대화를 본다.

| 항목 | 내용 |
|------|------|
| **Epic** | `Epic-001` — 4×4 부분(빈칸 2) 마방진 완성 (04.3·PRD·INV) |
| **User Story** | `US-001`~`US-005` ↔ 04.3 `US-01`~`US-05` |
| **방법론** | Concept-to-Code Traceability, Dual-Track UI+Logic, To-Do→Scenario→Test→Code, ECB, RED→GREEN→REFACTOR |
| **Task 메타(대화안)** | Task ID, RED/GREEN/REFACTOR, 제목, Scenario L0~L3, Test 이름, Code 대상, ECB, 체크포인트 |
| **Phase (대화안)** | 0: 골격·품질 / 1: US-01·Boundary / 2: US-02 / 3: US-03 / 4: US-04 / 5: US-05 / 6: Dual-Track 통합 / 7: 커버리지·NFR |
| **경계(02)** | `INVALID_SIZE` → `INVALID_VALUE_RANGE` → `INVALID_BLANK_COUNT` → `INVALID_DUPLICATE` ; `NO_SOLUTION` |
| **코드(02 명명)** | `Matrix4x4`, `BlankLocator`, `MissingNumberDetector`, `MagicSquareValidator`, `CombinationEvaluator`, `MagicSquareSolver` 등 (04.3 `BlankFinder` 등과 **역할 대응**) |

**L0~L3 (대화 정의):** L0 기능·인프라, L1 정상, L2 경계, L3 실패.

**README `WO-*`와의 관계:** 같은 02·04.3 근거를 쓰되, README **WO**는 “**RED로 고정할 판단**” 단위이고, 대화 **TASK** 는 “**구현 스텝·사이클**” 단위 — 필요 시 한 WO에 Task 여러 개가 매핑될 수 있다(1:N).

---

## 5. `README.md` vs 그 밖의 문서 (역할 정리)

| 문서 | 역할 | 비고 |
|------|------|------|
| **`README.md` `## To-Do List`** | **TD-1~7** 마일스톤 + **WO** 검증 계약(표) — **Concept-to-Code**·**AI/인간 협업**에 맞는 “무엇을 판정할지” | 저장소 **첫 화면**·온보딩 |
| **`docs/IMPLEMENTATION-TODO.md`** | **Phase**·**US-0x** 단위 **체크리스트** — **맵(04.3·02 링크)** | 유지보수·스프린트 태스크 |
| **TASK-001~… (미파일)** | TDD **RED/GREEN** 쪼개기 | 필요 시 `docs/implementation-todo-tasks.md` 등으로 추가 |
| **본 보고서** | 위 문서·식별자·파일명 변경·**방법론**의 **감사 추적(export)** | `Report/06-readme-implementation-todo-export.md` |

---

## 6. 후속 작업 제안 (선택)

- [ ] `pyproject.toml`·`src/`·`tests/` 생성 후 `README` «빠른 시작» 갱신  
- [x] README에 **TD/WO 상세** 반영됨 (2026-04-28)  
- [ ] (선택) `docs/PRD.md` §2.3 문서 맵에 `04.3-user-journey-stories` 파일명 **한 줄 주석**  
- [ ] (선택) TASK-xxx 전면표를 `docs/*.md`로 옮기고 README·보고서에서 **링크만** 유지

---

## 7. 관련 기존 Report (참고)

| 파일 | 관계 |
|------|------|
| `05-docs-prd-export.md` | `docs/PRD.md` 작성·내보내기 (본 보고서와 **별도** 날짜·범위) |
| `04.3-user-journey-stories.md` | US·AC **정본** (TD·WO Story 근거) |
| `02-4x4-magic-square-tdd-clean-architecture-design.md` | 계약·TC·컴포넌트·에러순서 **정본** (WO 근거) |

---

*본 문서는 README·구현 To-Do·To-Do→Work Order·TD/WO 식별에 대한 **작업과 산출물**을 `Report/`에 남기는 **내보내기(export)** 이다. 구현·TC 커밋은 포함하지 않는다.*
