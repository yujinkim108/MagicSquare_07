# 05 · `docs/PRD.md` 작성 및 보고서 내보내기

**최초 날짜:** 2026-04-27  
**최종 갱신:** 2026-04-28  
**산출물:** `c:\DEV\MagicSquare_07\docs\PRD.md`  
**작업 유형:** `Report/` · `Prompting/` 전체 Markdown을 원천으로 한 **제품 요구사항 문서(PRD)** 통합 작성·개정

---

## 1. 작업 개요

`Report/` 및 `Prompting/`에 흩어진 산출물(문제 정의, TDD·ECB 설계, 사용자 여정 Level 1~5, Gherkin, 시나리오 검증, `.cursorrules` 설명, Prompt 내보내기 대화)을 **한 문서**에서 **목표·범위·계약·성공 기준**을 파악할 수 있도록 정리했다.  
**상세 TC ID·Gherkin 전문·스냅샷**은 기존 `Report/*.md`를 **source of truth**로 두고, PRD는 **요구사항 계층** 역할만 한다.

### 1.1 2026-04-28 개정 요지 (Dual-Track UI · Logic · MLOps)

| 항목 | 내용 |
|------|------|
| **상위 이원** | **UI 트랙**(경계·**UX Contract**·현재 CLI)과 **Logic 트랙**(Entity+Control)을 명시; Logic **내부**는 기존과 같이 **Track A(Contract) / Track B(Algorithm)** |
| **§2.4** | UI / Logic / **MLOps** 역할 표, 테스트 **독립성**; MLOps는 **본 제품 필수 아님** |
| **§3.1** | UX Contract 어휘(Visible·Possible·Active·Include 등), TDD로 옮길 “**결정**” 우선 |
| **§5** | 시나리오 | UX Contract | Logic Rule **3단 매핑 표**(요약, G1 정책 행 포함) |
| **§6.1** | “Dual-Track” **두 층** 용어 정리(UI\|Logic vs A/B), GUI는 **같은 control·다른 boundary** |
| **§6.4 (신규)** | MLOps **확장 시** Logic / MLOps / UI / 비결정성 원칙(스키마·버전·관측 분리) |
| **§8 NFR** | **UI(확장 시)**, **MLOps(확장 시)** 행 추가 |
| **§10 용어** | UI·Logic 이원, Track A/B, **UX Contract**, **Logic Rule**, 구 “Dual-Track” 표기 주의, MLOps 항목 |

**맺음말(각주):** PRD 하단에 **UI·Logic·MLOps** 정렬·용어는 §2.4·§3.1·§6.4·§10을 본다는 문장을 추가함.

---

## 2. 입력 범위 (읽은 파일)

### Report (9개)

| 파일 | 용도(요약) |
|------|------------|
| `01-4x4-magic-square-problem-definition.md` | STEP1~5 문제 정의 |
| `02-4x4-magic-square-tdd-clean-architecture-design.md` | Domain·UI·Data·통합, 계약·Invariant(설계 측 ID) |
| `03-cursorrules-setup.md` | `.cursorrules` 8섹션 설계 |
| `04-user-journey-epic.md` | Level 1 Epic, INV-01~10(Epic) |
| `05-user-journey-level2.md` | Level 2 Journey 5 Step |
| `06-user-journey-stories.md` | US-01~05 |
| `04-magic-square-user-journey-Levels-1-5-Export-Report.md` | L1~L5 병합 **스냅샷** (타 문서와 중복 다수) |
| `08-level4-implementation-scenario-technical.md` | Gherkin·기술 약속·검산 주의 |
| `09-level5-scenario-verification.md` | 검증·갭(G1~G3)·Sign-off |

### Prompting (4개)

| 파일 | 용도(요약) |
|------|------------|
| `01-4x4-magic-square-problem-definition-prompt.md` | `01` Report 생성 맥락 |
| `02-4x4-magic-square-tdd-clean-architecture-design-prompt.md` | `02` Report 생성 맥락 |
| `03-cursorrules-setup-prompt.md` | `03` Report·`.cursorrules` 맥락 |
| `04-magic-square-user-journey-Levels-1-5-Export-Report-prompt.md` | L1~L5·통합 `04` 내보내기 맥락 |

**중복 처리:** `04-magic-square-user-journey-Levels-1-5-Export-Report.md`는 `04`~`09` **전문 병합**이므로 PRD 본문에는 **요약·출처**만 반영하고, **Epic/INV/US**는 개별 `04`·`05`·`06`·`08`·`09` 기준으로 통합했다.

---

## 3. 산출 파일 구조 (`docs/PRD.md`)

| 섹션 | 내용 |
|------|------|
| (서문) | Dual-Track: **UI·Logic 이원** + Logic **내부** Contract/Algorithm, §2.4·§6.1 링크 |
| §1 제품 개요 | Epic(**UI·Logic 이원 TDD**·Logic **내부** Contract/Algorithm), 문제 정의 요지, 4×4 이유, 프로그램·TDD 이유 |
| §2 범위 | In/Out of Scope, **§2.4** UI·Logic·MLOps 정렬, Level 1~5·Prompting **문서 맵** |
| §3 사용자 | Persona, **UI·Logic** 여정(한 줄), **§3.1** UX Contract 요약·어휘 |
| §4 Invariant | Epic **INV-01~10** + 설계서 INV와 **번호·체계 차이** 주의 |
| §5 기능 | **US-01~05** 압축(정본: `06`), **3단 매핑 표**(UX Contract · Logic Rule) |
| §6 아키텍처 | ECB, **상위/Logic 내부 Dual-Track** 용어, `02` I/O·에러·검증순서·Data, `03`/`.cursorrules`, **§6.4** MLOps(확장 시) |
| §7 BDD | Level 4·G1 갭 |
| §8 NFR | 커버리지, 계약, 회귀, 선택 도구, **UI(확장 시)**, **MLOps(확장 시)** |
| §9 Level 5 | G1~G3·Sign-off |
| §10 용어 | UI·Logic 이원, Track A/B, UX Contract, Logic Rule, MLOps 등 |
| §11 원천 인덱스 | Report 9 + Prompting 4 **전체 경로** 표 |

**폴더:** `docs/`에 `PRD.md`를 저장. 워크스페이스: **`MagicSquare_07`**.

---

## 4. 설계상 명시한 주의 사항 (PRD 본문 반영)

1. **Invariant ID:** `02` 설계서의 **INV-01~10**(행/열/대각/빈칸/출력 규칙)과 `04` Epic의 **INV-01~10**(훈련·추적)은 **1:1 동일하지 않을 수 있음** — PRD에 **병기·대조** 안내.  
2. **G1:** `08` Gherkin에서 **동일 격자**로 “작→큰 성공”과 “역 성공”을 **동시에** 맞추기 어려운 **검산 이슈** — PRD `§7`·`§9`에 `09`와 맞춰 **Given 분리** 권고. **§5 3단 매핑**에서도 “Given·픽스처 분리”로 **UI·Logic 쌍**이 한 시나리오씩 검증되게 한다고 명시.  
3. **“Dual-Track” 용어:** 구버전이 **Contract+Algorithm만** 가리키던 표현은 **UI 트랙**과 혼동될 수 있어, PRD **§6.1·§10**에서 **UI·Logic 이원** vs **Track A/B(Logic 내부)** 로 구분.  
4. **MLOps:** 현재 In Scope(§2.1)에 **모델 추론/파이프라인/서빙 없음** — **§6.4**는 **확장 시**만 구체 기입.  
5. **PRD는 스펙 대체 아님** — 세부 ID·문구·TC는 `Report/02` 등 **원문**을 우선.

---

## 5. 경로·파일 정보

| 항목 | 값 |
|------|-----|
| **PRD 경로** | `c:\DEV\MagicSquare_07\docs\PRD.md` |
| **이 보고서** | `c:\DEV\MagicSquare_07\Report\05-docs-prd-export.md` |
| **관련 Request** | Report + Prompting 전체 `*.md` → `docs/PRD.md` 생성; 이후 **Dual-Track UI+Logic+MLOps** 기준으로 PRD·보고 **동기화** |

---

## 6. 다음에 할 수 있는 작업 (선택)

- `06-user-journey-stories.md` 하단 “다음 문서”에 **`09` 링크** 추가(이전 `09` 작성 시 미반영).  
- PRD와 구현 **동기화** 시 `pyproject` 커버리지·패키지 경로(`magic_square/…`)를 실제 트리에 맞게 **한 줄** 갱신.  
- Epic US 표(`04` §8)와 `06`의 US-01~05 **제목**이 다르면, **하나**를 기준으로 **문서 정렬**.  
- **GUI In Scope**로 바꾸는 릴리스가 생기면 §2.2·NFR “UI(확장 시)”를 **필수 UX·E2E 목표**로 승격하고, `05` 본 문서에 **UI 트랙 내보내기** 절을 추가.  
- MLOps가 실제로 붙으면 §6.4를 **구체 SLO·아티팩트 ID**로 채우고 이 보고서 **§1.1**에 “MLOps 도입” 한 줄을 남긴다.

---

*본 문서는 `docs/PRD.md` 작성·내보내기·개정 작업의 **보고**이며, PRD 전문은 `docs/PRD.md`를 본다.*
