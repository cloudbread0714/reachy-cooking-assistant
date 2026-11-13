# Reachy Cooking Assistant 🍳🤖

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

## 누가 어디서 개발하나요

| 이름 | 담당 | 내 폴더 / 파일 | 시작 문서 |
|---|---|---|---|
| **강준형** | 🎤 음성 대화 + 🍳 요리 안내 | `voice/`, `core/llm.py`, `core/prompt.py`, `tools/cooking.py` | [dev-guide.md#강준형](docs/dev-guide.md#강준형) |
| **김민석** | 🤖 감정 표현 + 🥬 재료 관리 + 🍽️ 음식 추천 | `motion/`, `tools/ingredients.py`, `tools/recipes.py`, `rag/` | [dev-guide.md#김민석](docs/dev-guide.md#김민석) |
| **강유진** | 👁️ 시각 인식 + 📷 비전 재료 등록 + 통합 | `vision/`, `robot/`, `core/schema.py`, `tools/dispatcher.py`, `main.py` | [dev-guide.md#강유진](docs/dev-guide.md#강유진) |
| 다 같이 | 레시피 데이터 | `data/recipes/` | [data-contract.md](docs/data-contract.md#레시피-형식) |

**규칙: 내 폴더 밖의 파일은 고치지 않아요.** 필요하면 담당자에게 말하거나 PR에서 리뷰를 요청해요.
각 파일의 `TODO(이름)` 이 내가 채울 부분이에요.

## 폴더 구조

```
main.py              대화 루프 (듣기 → 사진 → LLM → action → 동작+말하기)
core/
  schema.py          ★ 데이터 약속: 감정 8개, action 10개, 응답 검사/예외 처리
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
  recipes/*.json     레시피 데이터 (커밋)
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
