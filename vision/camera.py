"""웹캠 → LLM 에 보낼 사진. 인식은 LLM 이 하고, 여기선 언제 찍을지 + 사진 품질. (담당: 강유진)"""

VISION_KEYWORDS = ("이거", "이게", "이건", "뭐야", "보여", "들고", "등록해", "봐줘")


def needs_vision(user_text: str) -> bool:
    """사진 필요한 말인지. 필요할 때만 찍어서 API 요청 아낌."""
    return any(keyword in user_text for keyword in VISION_KEYWORDS)


def capture_best_frame() -> bytes | None:
    """가장 선명한 한 장 JPEG. 카메라 없으면 None."""
    # TODO(강유진):
    #   1. cv2.VideoCapture(0) 로 0.5초 동안 여러 장
    #   2. Laplacian 분산 최대(= 가장 선명) 프레임 선택
    #   3. 가운데 crop + 긴 변 768px
    #   4. cv2.imencode(".jpg", frame)[1].tobytes()
    return None
