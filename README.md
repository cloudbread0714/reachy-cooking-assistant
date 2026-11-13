# Reachy Cooking Assistant

Reachy Mini(시뮬레이터)로 만드는 요리 도우미 로봇: 음성 대화, 감정 표현, 시각 인식, 재료 관리·음식 추천·요리 안내.

## 처음 클론한 뒤 꼭 실행

```bash
git config core.hooksPath .githooks   # main 직접 커밋 방지 훅 켜기
```

## 협업 규칙

1. `git switch main && git pull`
2. `git switch -c feat/<기능명>`
3. 작업 → 커밋 → `git push -u origin feat/<기능명>`
4. GitHub에서 main으로 PR 생성 → CodeRabbit 자동 리뷰
5. 리뷰 반영 + 대화 모두 해결 → Squash merge

`main`은 브랜치 보호가 걸려 있어서 직접 push할 수 없어요.
