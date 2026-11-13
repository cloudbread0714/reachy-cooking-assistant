# 개발 환경 세팅

수업 자료(Reachy Mini 개발환경 setup)와 같은 방식이에요: **Python 3.12 + uv + reachy-mini[mujoco]**

## 1. 설치 (처음 한 번)

필요한 것: Git, [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/cloudbread0714/reachy-cooking-assistant.git
cd reachy-cooking-assistant
git config core.hooksPath .githooks
uv sync
cp .env.example .env        # Windows PowerShell: copy .env.example .env
```

`uv sync` 가 Python 3.12 가상환경(`.venv`)을 만들고 `pyproject.toml` + `uv.lock` 그대로 설치해요.
패키지를 추가할 때는 `uv add 패키지명` 을 쓰고 `pyproject.toml`, `uv.lock` 을 같이 커밋해요.

VS Code: `Ctrl+Shift+P` → Python: Select Interpreter → `.venv` 선택

## 2. API 키 (.env)

| 키 | 발급 | 용도 |
|---|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/) | LLM + 비전 |
| `GEMINI_MODEL` | AI Studio 에서 무료로 쓸 수 있는 Flash 모델명 | |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com/) | STT (Whisper) |

- 개발할 때는 **각자 본인 키**를 써요. 무료 한도가 프로젝트 단위라서 하나를 같이 쓰면 금방 막혀요.
- `.env` 는 절대 커밋하지 않아요. 실수로 올렸으면 바로 키를 재발급해요.

## 3. 실행

**시뮬레이터 없이** (대부분의 개발은 이걸로 충분해요)

```bash
uv run main.py --no-robot
```

**시뮬레이터 연결** (터미널 2개)

| | Windows (PowerShell) | Mac |
|---|---|---|
| 터미널 1: 시뮬레이터 | `uv run reachy-mini-daemon --sim` | `uv run mjpython -m reachy_mini.daemon.app.main --sim` |
| 터미널 2: 로봇 | `uv run main.py` | `uv run main.py` |

MuJoCo 창에 로봇이 보이면 성공이에요. 시뮬레이터는 실행 중에 계속 켜둬야 해요.
`--scene minimal` 을 붙이면 테이블과 물체가 있는 장면이 나와요.

**테스트**

```bash
uv run pytest
```

## 4. 문제 해결

- **"No Reachy Mini Audio ... found" / "Cannot change resolution of Mujoco simulated camera"**
  실제 로봇이 없어서 나오는 안내 메시지예요. 오류가 아니에요.
- **`ConnectionError: Auto connection: both localhost and remote attempts failed`**
  시뮬레이터(터미널 1)가 안 켜져 있어요.
- **Mac: `uv sync` 중 `pycairo` 빌드 실패**
  - `pkg-config not found` → `brew install pkgconf`
  - `Compiler cc cannot compile programs` / `tapi error: malformed file` → Command Line Tools SDK 문제예요.
    Xcode SDK 를 쓰도록 지정하고 다시 설치해요:
    ```bash
    export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
    export SDKROOT=$(xcrun --sdk macosx --show-sdk-path)
    uv sync
    ```
- **PowerShell 에서 스크립트 실행 권한 오류** → 관리자 PowerShell 에서 `Set-ExecutionPolicy RemoteSigned` (최초 1회)
