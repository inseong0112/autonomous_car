import cv2
import numpy as np

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # 너비
camera.set(4, 480)  # 높이

while camera.isOpened():
    ret, frame = camera.read()

    crop_img = frame[300:640, 0:640]

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    Median_blur = cv2.medianBlur(Gaussian_blur, 3)

    _, thresh1 = cv2.threshold(Median_blur, 200, 255, cv2.THRESH_BINARY)

    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    frame_with_contours = crop_img.copy()
    cv2.drawContours(frame_with_contours, contours, -1, (0, 0, 255), 2) 

    lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 50, maxLineGap=50)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame_with_contours, (x1, y1), (x2, y2), (0, 0, 255), 2)

    white_color = cv2.bitwise_and(crop_img, crop_img, mask=mask)

    cv2.imshow('Original', frame)
    cv2.imshow('White Only', white_color)
    cv2.imshow('Contours', frame_with_contours)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()




