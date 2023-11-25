import cv2
import numpy as np

camera = cv2.VideoCapture(0)
camera.set(3, 640)  # 너비
camera.set(4, 480)  # 높이

while camera.isOpened():
    ret, frame = camera.read()

    #ROI 지정
    crop_img = frame[340:400, 0:640]    

    # 흑백 변환
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur, Median Blur 적용
    Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    Median_blur = cv2.medianBlur(Gaussian_blur, 3)

    # Canny 엣지 감지
    edges = cv2.Canny(Median_blur, 50, 150)

    # 허프 변환을 사용하여 선 탐지
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 2)


    cv2.imshow('Original', frame)
    cv2.imshow('Edges', edges)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()





