import cv2
import numpy as np

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 색상 범위 설정
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])
    lower_yellow = np.array([15, 150, 100])
    upper_yellow = np.array([35, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    maskr = cv2.add(mask1, mask2)

    # 색상에 따라 윤곽선 찾기
    contours_red, _ = cv2.findContours(maskr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(masky, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(maskg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 각 색상에 맞는 사각형 그리고 넓이 출력
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area >= 2000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 빨간색
            cv2.putText(frame, f'Red: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    for contour in contours_yellow:
        area = cv2.contourArea(contour)
        if area >= 2000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # 노란색
            cv2.putText(frame, f'Yellow: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area >= 2000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 초록색
            cv2.putText(frame, f'Green: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Color Detection', frame)

    if cv2.waitKey(1) == ord('q'):  
        break

camera.release()
cv2.destroyAllWindows()
