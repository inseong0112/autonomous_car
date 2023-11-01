import cv2
import numpy as np

# 신호등 감지
def detect(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    global red_light
    # 색상 범위 설정
    lower_red = np.array([136, 87, 111])
    upper_red = np.array([180, 255, 255])
    lower_green = np.array([66, 122, 129])
    upper_green = np.array([86, 255, 255])

    # lower, upper 범위에 속하는 경우 255(흰색), 아니면 0(검정색)
    maskr = cv2.inRange(hsv, lower_red, upper_red)
    maskg = cv2.inRange(hsv, lower_green, upper_green)

    # 색상에 따라 윤곽선 찾기
    contours_red, _ = cv2.findContours(maskr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(maskg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 각 색상에 맞는 사각형 그리고 넓이 보여주기
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area >= 10000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 빨간색
            cv2.putText(frame, f'Red: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return 'red'

    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area >= 10000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 초록색
            cv2.putText(frame, f'Green: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return 'green'

    return 'unknown'
