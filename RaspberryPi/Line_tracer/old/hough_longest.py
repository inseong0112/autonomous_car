import cv2
import numpy as np

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while camera.isOpened():
    ret, frame = camera.read()
    
    if ret:
        # 너비와 높이 설정
        

        # 이미지를 원하는 크기로 자르기 (예: 하단 부분)
        crop_img = frame[200:480, 0:640]

        # 흑백 변환
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # 가우시안 블러 적용 (잡음 제거)
        Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        Median_blur = cv2.medianBlur(Gaussian_blur, 3)

        # Canny 엣지 감지
        edges2 = cv2.Canny(Median_blur, 50, 200)

        # 허프 변환을 사용하여 선 탐지
        lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 100, maxLineGap=200)

        if lines is not None:
            # 선의 길이를 계산
            line_lengths = [np.linalg.norm(np.array(line[0][:2]) - np.array(line[0][2:4])) for line in lines]

            # 가장 긴 4개의 선 선택
            top_4_indices = np.argsort(line_lengths)[-2:]

            # 선택한 가장 긴 4개의 선을 그리기
            for index in top_4_indices:
                line = lines[index][0]
                x1, y1, x2, y2 = line
                cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 5)

        white_color = cv2.bitwise_and(crop_img, crop_img, mask=edges2)

        cv2.imshow('Original', frame)
        cv2.imshow('White Only', white_color)
        cv2.imshow('Edges2', edges2)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
