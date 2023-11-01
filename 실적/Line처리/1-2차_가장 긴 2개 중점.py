import cv2
import numpy as np
import time

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while camera.isOpened():
    ret, frame = camera.read()
    
    if ret:
        # ROI 지정
        crop_img = frame[300:480, 0:640]

        # 흑백 변환qq
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # Gaussian Blur, Median Blur 적용
        Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        Median_blur = cv2.medianBlur(Gaussian_blur, 3)

        # Canny 엣지 
        edges2 = cv2.Canny(Median_blur, 50, 200)

        # 허프 변환
        lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 100, maxLineGap=200)

        if len(lines) >= 2:
            # 선의 길이를 계산 (시작점의 (x, y) - 끝점의 (x, y))
            line_lengths = [np.linalg.norm(np.array(line[0][:2]) - np.array(line[0][2:4])) for line in lines]

            # 가장 긴 2개의 선 (오름차순 정렬, 맨 뒤 두개 선택)
            top_2 = np.argsort(line_lengths)[-2:]

            x1, y1, x2, y2 = lines[top_2[0]][0]
            cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 5)
            x = x1 + x2

            x1, y1, x2, y2 = lines[top_2[1]][0]
            cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 5)
            x += x1 + x2

            cv2.circle(crop_img, (int(x/4), 100), 30, (255, 0, 0), 3)


        cv2.imshow('Original', frame)
        cv2.imshow('Edges2', edges2)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()

