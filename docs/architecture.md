# 구조

## 한 턴의 흐름

```
 사용자 말 ──► voice.stt.listen() ──► "이거 뭐야?"
                                        │
                     vision.needs_vision()? ──yes──► vision.capture_best_frame() ─► JPEG
                                        │                                         │
                                        ▼                                         ▼
                         core.llm.ask(text, context, image)  ◄── context: 오늘 날짜, 재료 목록, 요리 상태
                                        │
                                        ▼
                     Response { reply, emotion, action }   (core.schema.parse_response 로 검사)
                                        │
                                        ▼
                     tools.dispatcher.dispatch(action) ──► ToolResult { say?, emotion? }
                                        │
               ┌────────────────────────┴────────────────────────┐
               ▼                                                 ▼
 motion.play(result.emotion or response.emotion)      voice.tts.speak(result.say or response.reply)
     (바로 리턴, 말하는 동안 움직임)                         (다 말할 때까지 기다림)
```

## 설계 원칙

1. **LLM 은 한 턴에 한 번만 불러요.** 사진도 같은 호출에 같이 보내요. 무료 한도를 아끼고 응답이 빨라요.
2. **숫자·목록·날짜는 코드가 정해요.** 재료 목록, 유통기한 계산, 요리 단계는 `ToolResult.say` 로 코드가 직접 말해요.
   LLM 이 지어내지 못하게요.
3. **로봇 연결은 한 번만.** `main.py` 에서 `robot.connection.connect()` 로 한 번 연결하고 `motion` 에만 넘겨요.
   음성·카메라는 PC 장치를 직접 써서 로봇 없이도 개발할 수 있어요.
4. **한 기능의 오류가 전체를 멈추지 않게.** `dispatch` 가 예외를 잡아서 "미안, 그건 지금 처리하지 못했어"로 바꿔요.
   LLM 응답이 깨지면 `parse_response` 가 "다시 말해줄래?"로 바꿔요.

## 모듈 사이 약속 (함수)

| 함수 | 입력 | 출력 | 담당 |
|---|---|---|---|
| `voice.stt.listen()` | | `str` | 강준형 |
| `voice.tts.speak(text)` | `str` | `None` (blocking) | 강준형 |
| `core.llm.ask(user_text, context, image)` | `str, dict, bytes \| None` | `Response` | 강준형 |
| `vision.camera.needs_vision(text)` | `str` | `bool` | 강유진 |
| `vision.camera.capture_best_frame()` | | `bytes \| None` (JPEG) | 강유진 |
| `motion.emotions.EmotionPlayer(mini).play(emotion)` | `str` | `None` (non-blocking) | 김민석 |
| `tools.dispatcher.dispatch(action)` | `Action \| None` | `ToolResult` | 강유진 |
| `tools.*.<action 이름>(params)` | `dict` | `ToolResult` | action 담당자 |
| `rag/search.py` 레시피 검색 | 담당자가 설계 | | 김민석 |

`Response`, `Action`, `ToolResult` 는 `core/schema.py` 에 정의돼 있어요.
