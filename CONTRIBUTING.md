# 협업 규칙

## 작업 흐름

```bash
git switch main && git pull               # 1. 최신 main
git switch -c feat/stt                    # 2. 기능 브랜치
# ... 작업 ...
uv run pytest                             # 3. 테스트
git add -A && git commit -m "feat(voice): Groq Whisper STT 연결"
git push -u origin feat/stt               # 4. push
```

5. GitHub 에서 main 으로 PR 생성 (템플릿 채우기)
6. **CodeRabbit 이 자동으로 리뷰**해요. 지적을 반영하거나, 안 고칠 거면 이유를 답글로 남겨요.
7. 모든 대화(conversation)를 해결하면 **본인이 Squash merge**해요. 브랜치는 자동으로 지워져요.

## 리뷰 규칙

### 누가 리뷰하나요

- **모든 PR**: CodeRabbit 이 자동으로 리뷰해요.
- **팀원 리뷰가 꼭 필요한 PR**: 아래 경우에는 해당 팀원을 Reviewer 로 지정하고, 확인을 받은 뒤 merge 해요.
  - `core/schema.py` (데이터 약속) 변경 → 팀원 2명 모두
  - 다른 사람 담당 폴더를 고친 경우 → 그 폴더 담당자
  - `main.py` 흐름 변경 → 강유진

### PR 올리는 사람

1. PR 템플릿의 "무엇을 했나요 / 어떻게 테스트했나요"를 채워요.
2. CodeRabbit 코멘트에는 **전부 대응**해요.
   - 맞는 지적 → 고치고 커밋 (`fix(voice): 리뷰 반영 - 녹음 타임아웃 처리`)
   - 안 고칠 지적 → 이유를 답글로 남겨요 (예: "시연용이라 지금은 단순하게 둠")
   - 대응한 코멘트는 **Resolve conversation** 을 눌러요. 모두 해결해야 merge 버튼이 켜져요.
3. 리뷰를 요청받은 팀원이 **1일 안에** 답이 없으면 단톡방에서 한 번 더 요청해요.

### 리뷰하는 사람 (팀원)

코멘트 앞에 머리말을 붙여서 꼭 고쳐야 하는 건지 바로 알 수 있게 해요.

| 머리말 | 뜻 | PR 올린 사람은 |
|---|---|---|
| `[필수]` | 버그, 데이터 약속 위반, 키 노출처럼 꼭 고쳐야 함 | 고치고 나서 merge |
| `[제안]` | 이렇게 하면 더 좋을 것 같음 | 반영하거나 이유를 답글로 남기기 |
| `[질문]` | 이해가 안 돼서 물어봄 | 답글로 설명 |

예시

```
[필수] reply 비어 있으면 FALLBACK 안 타고 speak("") 호출됨
[제안] 녹음 시간 5초는 상수로 빼자
[질문] 여기 lock 왜 걸었어?
```

- **짧게, 반말로** 써요. 코멘트 하나에 1~2문장. (CodeRabbit 도 같은 말투로 설정돼 있어요)
- **사람이 아니라 코드에 대해** 써요. "왜 이렇게 했어?" 보다 "이 경우에 OO 됨".
- 문제를 지적할 때는 **어떤 상황에서 어떻게 틀리는지**를 같이 써요.
- 좋은 부분이 있으면 짧게라도 남겨요.

### 리뷰에서 꼭 확인할 것

- [ ] 데이터 약속(`core/schema.py`)의 함수 모양, 감정/action 이름을 지켰나
- [ ] 다른 사람 담당 폴더를 말없이 고치지 않았나
- [ ] API 키, `.env`, 개인 데이터(`data/ingredients.json`)가 없나
- [ ] `uv run pytest`, `uv run main.py --no-robot` 이 되나
- [ ] 실패해도 로봇 전체가 멈추지 않나 (예외 처리)

## main 보호

- `main` 에는 직접 커밋/push 할 수 없어요. (GitHub 브랜치 보호 + `.githooks/pre-commit`)
- 클론한 뒤 `git config core.hooksPath .githooks` 를 꼭 한 번 실행해요.
- `main` 은 항상 `uv run main.py --no-robot` 과 `uv run pytest` 가 되는 상태로 유지해요.

## 브랜치 이름

`종류/짧은-설명` (영어 소문자, 단어는 `-` 로 연결)

| 종류 | 예시 |
|---|---|
| 새 기능 | `feat/stt`, `feat/emotion-motion`, `feat/vision-capture` |
| 버그 수정 | `fix/json-parse-error` |
| 문서·설정 | `docs/setup-windows`, `chore/deps` |

## 커밋 메시지

```
종류(폴더): 무엇을 했는지

(선택) 왜 했는지, 주의할 점
```

예시

```
feat(voice): Groq Whisper STT 연결
fix(motion): 모르는 emotion 은 nod 로 처리
test(tools): 재료 중복 등록 테스트 추가
docs: Windows 시뮬레이터 실행 방법 추가
chore: edge-tts 의존성 추가
```

**종류**

| 종류 | 언제 |
|---|---|
| `feat` | 새 기능, 기능 추가 |
| `fix` | 버그 수정 |
| `refactor` | 동작은 같고 코드 구조만 정리 |
| `test` | 테스트 추가·수정 |
| `docs` | 문서만 수정 |
| `chore` | 설정, 의존성, 기타 잡일 |

**폴더** (생략 가능): `core` `voice` `motion` `vision` `tools` `rag` `robot` `data` `docs` `tests`

**규칙**

1. 첫 줄은 **한국어로, 50자 안쪽**, 끝에 마침표 없이 써요.
2. "무엇을 했는지"가 보이게 써요. `수정`, `update`, `asdf` 처럼 내용 없는 메시지는 안 돼요.
3. 커밋 하나에는 **한 가지 변경**만 담아요. (STT 연결 + 모션 수정 → 커밋 2개)
4. 왜 그렇게 했는지 설명이 필요하면 한 줄 띄우고 본문에 적어요.

**자동 검사**

- 커밋할 때 `.githooks/commit-msg` 가 형식을 검사해서, 틀리면 커밋을 막아요.
  (`git config core.hooksPath .githooks` 를 실행해야 켜져요)
- Squash merge 하면 **PR 제목이 main 의 커밋 메시지**가 돼요. 그래서 PR 제목도 같은 형식으로 쓰고,
  GitHub Actions(`PR 제목 검사`)가 형식을 확인해요.

## 원칙

- **내 폴더만 고쳐요.** 담당은 [README](README.md#누가-어디서-개발하나요) 참고
- PR 은 작게: 기능 하나 = PR 하나
- `core/schema.py` 를 바꾸는 PR 은 단톡방에 공유하고 merge
- API 키, `.env`, `data/ingredients.json` 은 커밋하지 않아요
