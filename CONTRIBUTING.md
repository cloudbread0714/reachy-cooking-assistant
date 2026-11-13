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

## 이름 규칙

| 종류 | 브랜치 | 커밋 |
|---|---|---|
| 새 기능 | `feat/stt`, `feat/emotion-motion`, `feat/vision-capture` | `feat(voice): ...` |
| 버그 수정 | `fix/json-parse-error` | `fix(core): ...` |
| 문서·설정 | `docs/setup-windows`, `chore/deps` | `docs: ...`, `chore: ...` |

커밋 괄호 안에는 폴더 이름을 써요: `core`, `voice`, `motion`, `vision`, `tools`, `rag`, `data`

## 원칙

- **내 폴더만 고쳐요.** 담당은 [README](README.md#누가-어디서-개발하나요) 참고
- PR 은 작게: 기능 하나 = PR 하나
- `core/schema.py` 를 바꾸는 PR 은 단톡방에 공유하고 merge
- API 키, `.env`, `data/ingredients.json` 은 커밋하지 않아요
