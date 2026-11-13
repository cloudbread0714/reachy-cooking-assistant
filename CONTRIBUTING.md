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
