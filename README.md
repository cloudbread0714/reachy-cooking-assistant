# Reachy Cooking Assistant

Reachy Mini(시뮬레이터)로 만드는 **요리 도우미 로봇**이에요.

- 기본 기능: 음성 대화 · 감정 표현(안테나/고개/몸통) · 시각 인식("내가 들고 있는 게 뭐야?")
- 추가 기능: 재료 관리 · 음식 추천(레시피 검색) · 요리 단계 안내

## 빠른 시작

```bash
git clone https://github.com/cloudbread0714/reachy-cooking-assistant.git
cd reachy-cooking-assistant
git config core.hooksPath .githooks   # main 직접 커밋 방지 (꼭 한 번 실행)
uv sync                               # Python 3.12 + 의존성 설치
cp .env.example .env                  # API 키 입력 (Windows: copy .env.example .env)

uv run main.py --no-robot             # 시뮬레이터 없이 실행 (키보드로 대화)
uv run pytest                         # 테스트
```

시뮬레이터 연결, Windows/Mac 차이, 문제 해결은 [docs/setup.md](docs/setup.md)를 보세요.

## 누가 어디서 개발하나

- 수정: 이미 있는 파일. `TODO(이름)` 부분을 채우면 됨
- 새로 만들기: 아직 없는 파일. 이 이름으로 만들어서 구현
- 함수 이름·입출력은 그대로 유지 (바꾸려면 단톡방 공유)
- 내 파일 밖은 수정 금지. 필요하면 담당자에게 요청
- 자세한 설명: [docs/dev-guide.md](docs/dev-guide.md)

### 강준형: 음성 대화 + 요리 안내

| 구분 | 파일 | 할 일 |
|---|---|---|
| 수정 | `voice/stt.py` | `listen()`: 마이크 녹음 → Groq Whisper → 텍스트 |
| 수정 | `voice/tts.py` | `speak()`: edge-tts 로 말하기 |
| 수정 | `core/llm.py` | `ask()`: Gemini 호출 (사진 포함, JSON 응답) |
| 수정 | `core/prompt.py` | 프롬프트 다듬기 |
| 수정 | `tools/cooking.py` | `start_cooking`, `next_step`, `prev_step`, `repeat_step`, `stop_cooking` |
| 새로 만들기 | `voice/recorder.py` | 마이크 녹음, 말 끝나면(무음) 자동 종료 |
| 새로 만들기 | `tests/test_cooking.py` | 시작 → 다음 → 이전 → 종료 순서 테스트 |
| 새로 만들기 | `tests/test_llm.py` | 이상한 LLM 응답 샘플로 파싱 테스트 |

### 김민석: 감정 표현 + 재료 관리 + 음식 추천

| 구분 | 파일 | 할 일 |
|---|---|---|
| 수정 | `motion/emotions.py` | 감정 8개 동작 다듬기 (`MOVES`), 필요하면 감정 추가 |
| 수정 | `tools/ingredients.py` | `add_ingredient`, `remove_ingredient`, `list_ingredients`, `check_expiry` |
| 수정 | `tools/recipes.py` | `recommend_recipe`: 추천 문장 만들기 |
| 수정 | `rag/search.py` | `search_recipes()`: 가진 재료로 레시피 검색 |
| 새로 만들기 | `rag/embed.py` | (선택) "매운 거" 같은 요청용 임베딩 검색 |
| 새로 만들기 | `tests/test_ingredients.py` | 등록·중복 등록·삭제·임박 테스트 |
| 새로 만들기 | `tests/test_search.py` | 재료별 추천 순위 테스트 |

모션 확인: 시뮬레이터 켜고 `uv run python -m motion.demo`

### 강유진: 시각 인식 + 비전 재료 등록 + 통합

| 구분 | 파일 | 할 일 |
|---|---|---|
| 수정 | `vision/camera.py` | `capture_best_frame()`: 가장 선명한 사진, `needs_vision()` 키워드 |
| 수정 | `core/prompt.py` | 사진 규칙 (애매하면 다시 묻기, 재료명 통일). 준형님과 협의 |
| 수정 | `main.py` | 전체 흐름, 시연 시나리오 |
| 수정 | `core/schema.py`, `tools/dispatcher.py` | 데이터 약속 관리 |
| 새로 만들기 | `vision/eval.py` | 재료 사진 세트로 인식 정확도 측정 |
| 새로 만들기 | `tests/test_vision.py` | `needs_vision()` 키워드 테스트 |

### 다 같이

| 구분 | 파일 | 할 일 |
|---|---|---|
| (완료) | `data/recipes/*.json` | 레시피 44개 채워둠 (한식·양식·중식·일식·분식·디저트). 필요하면 추가만 |

## 폴더 구조

```
main.py              대화 루프 (듣기 → 사진 → LLM → action → 동작+말하기)
core/
  schema.py          데이터 약속: 감정 8개, action 10개, 응답 검사/예외 처리
  llm.py             Gemini 호출 (지금은 mock)
  prompt.py          시스템 프롬프트
  config.py          .env 읽기
robot/connection.py  Reachy Mini 연결 (main.py 에서 한 번만)
motion/emotions.py   감정 → 안테나/고개/몸통 동작
voice/stt.py         마이크 → 텍스트 (지금은 키보드 입력)
voice/tts.py         텍스트 → 스피커 (지금은 print)
vision/camera.py     웹캠 → 가장 선명한 사진
tools/
  dispatcher.py      action 이름 → 실행 함수 연결
  ingredients.py     재료 관리 action
  recipes.py         음식 추천 action
  cooking.py         요리 안내 action
rag/search.py        레시피 검색
data/
  recipes/*.json     레시피 44개 (커밋)
  ingredients.json   내 냉장고 재료 (각자 로컬, 커밋 안 함)
tests/               pytest
docs/                문서
```

## 문서

- [docs/setup.md](docs/setup.md): 개발 환경, 시뮬레이터 실행
- [docs/dev-guide.md](docs/dev-guide.md): 사람별 개발 가이드 (어디서 시작하고, 혼자 어떻게 테스트하는지)
- [docs/architecture.md](docs/architecture.md): 전체 흐름, 모듈끼리 주고받는 함수
- [docs/data-contract.md](docs/data-contract.md): LLM 응답 형식, 감정/action 목록, 저장 형식
- [CONTRIBUTING.md](CONTRIBUTING.md): 브랜치, 커밋, PR, CodeRabbit 리뷰 규칙
