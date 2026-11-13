"""PC 웹캠 -> LLM 에 보낼 사진. (담당: 강유진)

사진 인식 자체는 LLM(Gemini)이 해요. 여기서는 "언제 찍을지"와 "얼마나 좋은 사진을 줄지"를 맡아요.
"""

VISION_KEYWORDS = ("이거", "이게", "이건", "뭐야", "보여", "들고", "등록해", "봐줘")


def needs_vision(user_text: str) -> bool:
    """이번 말에 사진이 필요한지. 필요할 때만 찍어서 무료 API 요청을 아껴요."""
    return any(keyword in user_text for keyword in VISION_KEYWORDS)


def capture_best_frame() -> bytes | None:
    """웹캠에서 가장 선명한 한 장을 JPEG bytes 로. 카메라가 없으면 None."""
    # TODO(강유진):
    #   1. cv2.VideoCapture(0) 으로 0.5초 동안 여러 장 찍기
    #   2. cv2.Laplacian(gray, cv2.CV_64F).var() 가 가장 큰(= 가장 선명한) 프레임 선택
    #   3. 가운데 crop + 긴 변 768px 로 줄이기
    #   4. cv2.imencode(".jpg", frame)[1].tobytes() 반환
    return None
