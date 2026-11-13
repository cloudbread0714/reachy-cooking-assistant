# 데이터 약속

코드 기준은 [`core/schema.py`](../core/schema.py) 예요. 이 문서와 다르면 schema.py 가 맞아요.
바꿀 때는 schema.py + 이 문서 + 노션 ④를 같이 고치고 단톡방에 공유해요.

## 1. LLM 응답 형식

```json
{
  "reply": "로봇이 말할 내용 (1~2문장)",
  "emotion": "nod",
  "action": {"name": "add_ingredient", "params": {"name": "우유", "expiry": "2026-11-20"}}
}
```

- `reply` (필수) → TTS
- `emotion` (필수) → 모션. 목록에 없으면 `nod`
- `action` (선택) → 할 일이 없으면 `null`

## 2. 감정 (8개, 추가 가능)

| emotion | 언제 |
|---|---|
| `happy` | 기쁠 때, 칭찬, 인사 |
| `sad` | 위로, 아쉬울 때 (만들 수 있는 음식 없음) |
| `curious` | 궁금할 때, 제안할 때 |
| `confused` | 못 알아들었을 때, 인식이 애매할 때 |
| `nod` | 알겠다 (등록·삭제 완료) |
| `shake` | 안 된다 (유통기한 지난 재료) |
| `think` | 생각 중 (추천 계산) |
| `excited` | 신날 때 (요리 시작) |

## 3. action (10개)

| 담당 | name | params | 예시 말 |
|---|---|---|---|
| 김민석 | `add_ingredient` | `name`, `expiry` (YYYY-MM-DD 또는 null) | "우유 샀어, 20일까지야" / (재료 들고) "이거 등록해줘" |
| 김민석 | `remove_ingredient` | `name` | "우유 다 먹었어" |
| 김민석 | `list_ingredients` | | "냉장고에 뭐 있어?" |
| 김민석 | `check_expiry` | | "곧 상하는 거 있어?" |
| 김민석 | `recommend_recipe` | `query` (선택) | "지금 재료로 뭐 만들 수 있어?" |
| 강준형 | `start_cooking` | `recipe`, `steps` (선택) | "김치찌개 만들래" |
| 강준형 | `next_step` | | "다음", "다 했어" |
| 강준형 | `prev_step` | | "이전 단계 뭐였지?" |
| 강준형 | `repeat_step` | | "다시 말해줘" |
| 강준형 | `stop_cooking` | | "그만할래" |

- 레시피는 혼합 방식: `start_cooking` 은 `data/recipes/` 에 있는 요리면 그 steps, 없으면 LLM 이 만든 `params.steps` 사용
- 말로 등록하든 카메라로 등록하든 `add_ingredient` 하나만 써요.
- 같은 이름으로 다시 오면 expiry 만 업데이트해요.
- 보류 (2차 회의): 켜자마자 자동 유통기한 알림, `set_alert_days`, 임박 기준 일수

## 4. 예외 처리

| 상황 | 처리 |
|---|---|
| JSON 깨짐 / `reply` 없음 | `{"reply": "다시 말해줄래?", "emotion": "confused", "action": null}` |
| 모르는 emotion | `nod` |
| 모르는 action / 필수 params 없음 | action 무시, `reply` 만 말하기 |
| action 실행 중 오류 | "미안, 그건 지금 처리하지 못했어." + `confused` |

## 5. 저장 형식

`data/ingredients.json` (각자 로컬, 커밋 안 함)

```json
[{"name": "우유", "expiry": "2026-11-20"}, {"name": "김치", "expiry": null}]
```

요리 진행 상태 (메모리, `tools/cooking.py`)

```json
{"cooking": true, "recipe": "김치찌개", "steps": ["...", "..."], "current_step": 0}
```

## 레시피 형식

`data/recipes/<영문-이름>.json` 한 파일에 레시피 하나

```json
{
  "name": "김치찌개",
  "ingredients": ["김치", "돼지고기", "두부", "대파", "양파"],
  "optional": ["고춧가루", "참치"],
  "tags": ["매운", "찌개", "한식"],
  "time_min": 25,
  "steps": ["냄비에 돼지고기를 넣고 중불에서 볶아줘.", "..."]
}
```

- `ingredients`: 꼭 필요한 재료. 냉장고 등록 이름과 똑같이 ("대파" O, "파 한 줌" X)
- 기본 양념(소금, 설탕, 간장, 고추장, 식용유, 참기름 등)은 `ingredients` 에 안 넣음. 집에 있다고 가정
- 파일 이름은 영문 (`kimchi-jjigae.json`), `uv run pytest` 가 형식 검사
- `steps`: 로봇이 한 단계씩 그대로 읽어요. 한 단계에 한 동작, 반말로 써요.
