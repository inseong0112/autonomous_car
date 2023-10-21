import cv2
import numpy as np

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(3, 1440)  # 너비
camera.set(4, 2560)  # 높이

while camera.isOpened():
    ret, frame = camera.read()

    # 이미지를 원하는 크기로 자르기 (예: 하단 부분)
    crop_img = frame[600:1440, 0:2560]

    # 흑백 변환
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용 (잡음 제거)
    Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    Median_blur = cv2.medianBlur(Gaussian_blur, 3)

    # 이진화 (흰색 강조)
    _, thresh1 = cv2.threshold(Median_blur, 200, 255, cv2.THRESH_BINARY)

    # 팽창 연산 (물체 연결)
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # 허프 변환을 사용하여 선 탐지
    lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 50, maxLineGap=50)

    if lines is not None:
        # 가장 긴 선 찾기
        longest_line = max(lines, key=lambda line: np.linalg.norm(np.array(line[0][:2]) - np.array(line[0][2:4])))
        
        x1, y1, x2, y2 = longest_line[0]
        cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 가장 긴 선 그리기

    white_color = cv2.bitwise_and(crop_img, crop_img, mask=mask)

    cv2.imshow('Original', frame)
    cv2.imshow('White Only', white_color)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
