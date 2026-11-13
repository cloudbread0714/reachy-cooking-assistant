# 사람별 개발 가이드

모든 모듈은 **mock(가짜 구현)** 으로 이미 연결돼 있어요. 그래서 `uv run main.py --no-robot` 이 처음부터 돌아가고,
각자 자기 함수의 안쪽만 진짜로 바꾸면 돼요. **함수 이름과 입출력(아래 "약속")은 바꾸지 않아요.**
바꿔야 하면 팀 단톡방에 먼저 말해요.

공통 흐름 (`main.py`):

```
listen() → needs_vision()? → capture_best_frame() → llm.ask() → dispatch(action) → motion.play() + speak()
```

---

## 강준형

**음성 대화** + **요리 안내**

| 파일 | 할 일 | 약속 (바꾸지 않기) |
|---|---|---|
| `voice/stt.py` | PC 마이크 녹음 → Groq Whisper | `listen() -> str` 한 문장 들을 때까지 기다림 |
| `voice/tts.py` | edge-tts 로 말하기 | `speak(text: str) -> None` 다 말할 때까지 기다림 |
| `core/llm.py` | Gemini 호출 (사진 포함) | `ask(user_text, context, image) -> Response` |
| `core/prompt.py` | 프롬프트 다듬기 | `build_system_prompt(context) -> str` |
| `tools/cooking.py` | 요리 단계 진행 | 각 함수 `(params: dict) -> ToolResult` |

**혼자 테스트하기**
- LLM: `uv run python -c "from core.llm import ask; print(ask('우유 샀어 20일까지', {'today':'2026-11-13'}))"`
- 응답이 이상해도 `parse_response` 가 FALLBACK 으로 막아줘요. 원문을 print 해서 프롬프트를 고치세요.
- 요리 안내: `tests/test_cooking.py` 를 만들어서 `start_cooking → next_step → prev_step` 순서로 확인

**주의**
- `next/prev/repeat_step` 은 LLM 을 다시 부르지 않아요. `state.current_step` 만 움직여요.
- `start_cooking` 은 `rag.search.find_recipe(name)` 이 있으면 그 steps 를, 없으면 `params["steps"]` 를 써요.
- 요리 단계 문장은 `ToolResult(say=...)` 로 돌려주세요. LLM reply 대신 그 문장을 말해요.

---

## 김민석

**감정 표현** + **재료 관리** + **음식 추천**

| 파일 | 할 일 | 약속 (바꾸지 않기) |
|---|---|---|
| `motion/emotions.py` | 8개 감정 동작 다듬기 (`MOVES` 키프레임) | `EmotionPlayer(mini).play(emotion)` 바로 리턴(말하면서 움직임) |
| `tools/ingredients.py` | add/remove/list/check_expiry | 각 함수 `(params: dict) -> ToolResult` |
| `tools/recipes.py` | 추천 문장 만들기 | `recommend_recipe(params) -> ToolResult` |
| `rag/search.py` | 레시피 검색 | `search_recipes(ingredient_names, query, k) -> list[dict]` |

**혼자 테스트하기**
- 모션: 시뮬레이터를 켜고([setup.md](setup.md)) `uv run python -m motion.demo` (특정 감정만: `uv run python -m motion.demo nod shake`)
- 재료/추천: `data/ingredients.example.json` 을 `data/ingredients.json` 으로 복사해서 `tests/test_ingredients.py` 작성

**주의**
- 감정을 추가하려면 `core/schema.py` 의 `EMOTIONS` 와 `MOVES` 둘 다 추가 (schema 변경은 단톡방 공유)
- 같은 이름으로 `add_ingredient` 가 오면 expiry 만 업데이트, expiry 가 None 이면 "유통기한은 언제까지야?"
- 임박 기준은 `schema.EXPIRY_SOON_DAYS` (지금 3일, 2차 회의에서 결정 예정)
- 켜자마자 자동 알림은 보류 (2차 회의에서 결정)

---

## 강유진

**시각 인식** + **비전 재료 등록** + **통합**

| 파일 | 할 일 | 약속 (바꾸지 않기) |
|---|---|---|
| `vision/camera.py` | 웹캠에서 가장 선명한 사진 | `needs_vision(text) -> bool`, `capture_best_frame() -> bytes \| None` (JPEG) |
| `core/prompt.py` 의 사진 규칙 | 인식 품질 (애매하면 다시 묻기, 재료명 통일) | 준형님과 같이 수정 |
| `core/schema.py` | 데이터 약속 관리 | 바꾸면 단톡방 공유 |
| `tools/dispatcher.py` | action → 함수 연결 | `dispatch(action) -> ToolResult` |
| `main.py` | 전체 연결, 시연 흐름 | |

**혼자 테스트하기**
- `uv run python -c "from vision.camera import capture_best_frame; open('shot.jpg','wb').write(capture_best_frame())"` 로 사진 확인
- 인식 정확도: 재료 사진 20~30장으로 테스트 세트를 만들어 프롬프트 바꿀 때마다 비교

**주의**
- 사진 인식은 LLM 한 번 호출 안에서 같이 해요 (별도 비전 모델 호출 없음 → 무료 한도 절약)
- "이거 등록해줘"도 action 은 `add_ingredient` 하나예요. 저장 처리는 민석님 코드가 해요.

---

## 다 같이: 레시피 데이터

`data/recipes/` 에 레시피 JSON 을 각자 10~15개 추가해요. 형식은 [data-contract.md](data-contract.md#레시피-형식),
예시는 `data/recipes/kimchi-jjigae.json`. 재료 이름은 냉장고에 등록할 이름과 똑같이 써요 ("대파" O, "파 한 줌" X).
