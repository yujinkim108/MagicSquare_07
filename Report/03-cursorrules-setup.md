# 03 · `.cursorrules` 설계 및 작성

**날짜**: 2026-04-27  
**대상 파일**: `c:\DEV\MagicSquare\.cursorrules`  
**작업 유형**: Cursor AI 행동 규칙 파일 초기 설계 및 전체 작성

---

## 1. 작업 개요

MagicSquare 프로젝트에 Cursor AI가 일관된 코딩 규칙을 따르도록 `.cursorrules` YAML 파일을 설계하고 작성했다.  
ECB(Entity-Control-Boundary) 아키텍처와 TDD 사이클을 AI 수준에서 강제하는 것이 핵심 목표다.

---

## 2. 작업 단계 요약

| 단계 | 내용 |
|---|---|
| 1 | 8개 최상위 키 뼈대 생성 (값 비움, 80자 구분선 주석 추가) |
| 2 | `tdd_rules` 섹션 초안 작성 (red / green / refactor 3페이즈) |
| 3 | 완성 파일 검토 — YAML 문법, 누락 섹션, 충돌, AI 이행 불가 규칙 점검 |
| 4 | 나머지 7개 섹션 전체 작성 완료 |

---

## 3. 파일 구조

```
.cursorrules
├── project          # 프로젝트 메타 정보
├── code_style       # Python 코딩 스타일 규칙
├── architecture     # ECB 레이어 정의 및 의존성 방향
├── tdd_rules        # TDD 3페이즈 규칙 (red / green / refactor)
├── testing          # pytest 설정 및 네이밍 컨벤션
├── forbidden        # 금지 패턴 (pattern / reason / alternative)
├── file_structure   # ECB 기준 디렉터리 트리
└── ai_behavior      # Cursor AI 코드 생성 전·중·후 행동 규칙
```

---

## 4. 섹션별 설계 결정

### 4.1 `project`

```yaml
project:
  name: MagicSquare
  language: Python
  version: "3.10+"
  pattern: ECB (Entity-Control-Boundary)
```

프로젝트 이름, 언어, 버전, 아키텍처 패턴을 첫 섹션에 명시해 AI가 전체 컨텍스트를 즉시 파악하게 했다.

---

### 4.2 `code_style`

- **포매터**: Black (max_line_length: 88)
- **스타일 가이드**: PEP8 엄격 준수
- **타입힌트**: 모든 함수 파라미터·반환값 필수
- **docstring**: Google 스타일, 모든 public 메서드·클래스·모듈에 필수
- **임포트 순서**: isort (stdlib → third-party → local)
- **네이밍**: PascalCase(클래스), snake_case(함수), UPPER_SNAKE_CASE(상수)

`docstring.example` 키에 실제 작성 예시를 인라인으로 삽입해 AI가 구체적인 형식을 참조하도록 했다.

---

### 4.3 `architecture`

ECB 3레이어를 각각 `description`, `responsibilities`, `allowed_dependencies`, `forbidden_dependencies`로 정의했다.

```
boundary → control → entity   (단방향 의존성)
```

| 레이어 | 허용 의존 | 금지 의존 |
|---|---|---|
| boundary | control | entity |
| control | entity | boundary |
| entity | (없음) | control, boundary |

> **핵심 결정**: boundary → entity 직접 참조도 명시적으로 금지했다. boundary는 반드시 control을 통해서만 entity 데이터에 접근해야 한다.

---

### 4.4 `tdd_rules`

각 페이즈를 `description` / `rules` / `must_not` 3-키 구조로 작성했다.

| 페이즈 | 핵심 규칙 | 대표 must_not |
|---|---|---|
| red_phase | 테스트 먼저, 실패 확인 후 진행 | 테스트 없이 구현 코드 작성 |
| green_phase | 최소 코드로만 통과, 리팩터링 금지 | 클래스 구조 재설계, 테스트 수정으로 통과율 상승 |
| refactor_phase | 기능 변경 없이 구조 개선, 커버리지 유지 | 리팩터링 중 새 기능 추가, 테스트 skip으로 커버리지 우회 |

`must_not`을 추가한 이유: 이전 검토 단계에서 `green_phase`의 하드코딩 허용과 `forbidden`의 하드코딩 금지 간 잠재 충돌이 발견됐다. `must_not`에 "테스트를 수정하여 통과율을 높이는 행위"를 명시하고 `forbidden`의 `alternative`에 `constants.py` 우회 경로를 제시해 충돌을 해소했다.

---

### 4.5 `testing`

```yaml
testing:
  framework: pytest
  pattern: AAA (Arrange-Act-Assert)
  coverage:
    minimum: 80%
    fail_under: true
```

`fixture_scope`를 function / class / module / session 4단계로 정의했다.  
`markers`(unit / integration / slow)를 추가해 `pytest -m unit` 등 선택 실행을 지원한다.

---

### 4.6 `forbidden`

`pattern / reason / alternative` 3-키 구조로 6개 항목을 작성했다.

| pattern | alternative |
|---|---|
| `print()` | `logging` 모듈 |
| 하드코딩 상수 | `constants.py` 명명 상수 |
| `except:` 단독 사용 | `except SpecificError as e:` |
| ECB 역방향 의존성 | DIP 또는 이벤트/콜백 패턴 |
| 타입힌트 없는 함수 | 모든 파라미터·반환값에 타입힌트 명시 |
| `assertEqual` 등 혼용 | `assert` + `pytest.raises()` 일관 사용 |

---

### 4.7 `file_structure`

`root_comment` 키에 ASCII 트리 다이어그램을 YAML 리터럴 블록(`|`)으로 삽입했다.

```
magic_square/
├── boundary/
├── control/
├── entity/
├── tests/
│   ├── boundary/
│   ├── control/
│   └── entity/
└── pyproject.toml
```

`tests/`가 소스 폴더 구조를 그대로 미러링하는 것이 핵심 규칙이다.

---

### 4.8 `ai_behavior`

코드 생성을 3단계로 분리해 각각 행동 규칙을 명시했다.

| 단계 | 대표 규칙 |
|---|---|
| before | 관련 테스트 파일 먼저 확인, ECB 레이어 파악, TDD 단계 확인 |
| while | 타입힌트 필수, ECB 경계 위반 금지, print 금지, 하드코딩 금지 |
| after | code_style 자가 검토, allowed_dependencies 확인, 커버리지 언급 |

`warnings` 4개는 위반 감지 시 코드 생성 전 경고를 출력하도록 설계했다.

> **이행 불가 규칙 배제**: 이전 검토에서 "런타임 테스트 실행 결과 자동 확인", "커버리지 수치 자동 측정" 등은 AI가 직접 수행할 수 없다고 판단해 `ai_behavior`에 포함하지 않았다. 대신 "커버리지 충족 여부를 언급한다"처럼 AI가 실제로 할 수 있는 수준으로 표현했다.

---

## 5. 검토 결과 반영 사항

| 발견 문제 | 반영 내용 |
|---|---|
| `testing` 미작성으로 `refactor_phase` 커버리지 조건 기준 불명확 | `testing.coverage.minimum: 80%` 명시 |
| `green_phase` 하드코딩 허용 vs `forbidden` 하드코딩 금지 잠재 충돌 | `green_phase.must_not`에 명시 + `forbidden.alternative`에 `constants.py` 경로 제시 |
| `ai_behavior`에 런타임 이행 불가 규칙 포함 위험 | 런타임 확인·측정·이벤트 관련 규칙 전면 배제 |

---

## 6. 최종 파일 정보

| 항목 | 값 |
|---|---|
| 경로 | `c:\DEV\MagicSquare\.cursorrules` |
| 총 라인 수 | 233줄 |
| 최상위 섹션 수 | 8개 |
| 섹션 구분 | 80자 `#` 구분선 |
| YAML 문법 오류 | 없음 |
