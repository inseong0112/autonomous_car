import cv2
import numpy as np

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # 너비
camera.set(4, 480)  # 높이

while camera.isOpened():
    ret, frame = camera.read()
    #ROI 지정
    crop_img = frame[300:480, 0:640]

    # 흑백 변환
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur 적용
    Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    Median_blur = cv2.medianBlur(Gaussian_blur, 3)

    # 이진화 (흰색 강조)
    _, thresh1 = cv2.threshold(Median_blur, 200, 255, cv2.THRESH_BINARY)

    # 수축, 팽창으로 노이즈 제거
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # 윤곽선 찾기
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 빨간색으로 윤곽선 그리기
    frame_with_contours = crop_img.copy()
    cv2.drawContours(frame_with_contours, contours, -1, (0, 0, 255), 2)  # 빨간색 선
    
    # 허프 변환을 사용하여 직선 탐지
    lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 50, maxLineGap=50)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame_with_contours, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow('Original', frame)
    cv2.imshow('Contours', frame_with_contours)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()




