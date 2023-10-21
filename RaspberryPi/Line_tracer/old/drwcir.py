import cv2
import numpy as np

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while camera.isOpened():
    ret, frame = camera.read()
    
    if ret:
        # 이미지를 원하는 크기로 자르기 (예: 하단 부분)
        crop_img = frame[300:400, 0:640]

        # 흑백 변환
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # 가우시안 블러 적용 (잡음 제거)
        Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        Median_blur = cv2.medianBlur(Gaussian_blur, 3)

        # Canny 엣지 감지
        edges2 = cv2.Canny(Median_blur, 50, 200)

        # 허프 변환을 사용하여 선 탐지
        lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 20, maxLineGap=200)

        cv2.circle(frame, (30, 350), 30, (255, 0, 0), 2)
        cv2.line(frame, (320, 0), (320, 640), (255, 0, 255), 2)
        cv2.line(frame, (0, 350), (640, 350), (255, 0, 0), 2)
        cv2.imshow('Original', frame)
        cv2.imshow('Edges2', edges2)

        if cv2.waitKey(1) == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()
