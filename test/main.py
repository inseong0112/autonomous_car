import cv2
import traffic_light
import time
import multiprocessing
import atexit
import numpy as np

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

red_light = None

def detect(frame):
    ret, frame = camera.read()
    print('called')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 색상 범위 설정
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([136, 87, 111])
    upper_red2 = np.array([180, 255, 255])
    lower_green = np.array([66, 122, 129])
    upper_green = np.array([86, 255, 255])
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
    key = cv2.waitKey(1)

    if key == ord('q'):
        return None
    elif len(contours_red) > 0:
        return 'red'
    elif len(contours_yellow) > 0:
        return 'yellow'
    elif len(contours_green) > 0:
        return 'green'
    else:
        return 'unknown'



if __name__ == '__main__':
    ret, frame = camera.read()
    # detect 함수 실행을 위한 프로세스 시작

    while True:
        try:
            print('start')
            red_light = traffic_light.detect(frame)
            # 여기에서 red_light 변수를 사용하여 필요한 작업 수행
            if red_light == 'red':
                print("Stop!")
            elif red_light == 'green':
                print("Go!")
            elif red_light == 'yellow':
                print("Prepare to stop!")
            cv2.imshow('frame', frame)

        except KeyboardInterrupt:
            # Ctrl+C로 프로그램 종료
            
            break