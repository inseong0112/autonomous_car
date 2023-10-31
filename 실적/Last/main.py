import cv2
import time
import numpy as np
import math
import motor
import proximity
from multiprocessing import Process, Value

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

red_light = None

# 근접 센서 값 불러오기
def read_distance(prox):
    while True :
        prox.value = proximity.read_distance()
        time.sleep(0.1)

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

def main():
    while camera.isOpened():
        ret, frame = camera.read()

        if ret:
            traffic_light_roi = frame[0:350, 0:640]     # 신호등 인식에 사용할 ROI
            traffic_light = detect(traffic_light_roi)   # detect 함수에 ROI 넘겨줌

            crop_img = frame[340:400, 0:640]                    #ROI 지정
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)   # 흑백 변환
            Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)   # Gaussian Blur
            Median_blur = cv2.medianBlur(Gaussian_blur, 3)      # Median Blur
            edge = cv2.Canny(Median_blur, 50, 200)            #Canny Edge 감지 
            lines = cv2.HoughLinesP(edge, 1, np.pi / 180, 20, maxLineGap=200) # 허프 변환을 사용하여 선 탐지
            left_lines = []  # 왼쪽에 있는 직선
            right_lines = []  # 오른쪽에 있는 직선

            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    slope = (y2 - y1) / (x2 - x1)               # 기울기 
                    intercept = y1 - slope * x1                 # y절편
                    intersection_x = (100 - intercept) / slope  # 교점 x 좌표 계산

                    if intersection_x < 320:    # 320을 기준으로 왼쪽과 오른쪽 판단
                        left_lines.append(intersection_x)
                        cv2.line(crop_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    else:
                        right_lines.append(intersection_x)
                        cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                avg_left = 0 
                avg_right = 0

                if len(left_lines) > 0 and len(right_lines) > 0:        # left_lines와 right_lines에 값이 있는지 확인
                    avg_left = (max(left_lines) + min(left_lines)) / 2 
                    avg_right = (max(right_lines) + min(right_lines)) / 2

                    # 무한대, Nan인 경우 제외
                    if not math.isinf(avg_left) and not math.isinf(avg_right) and not math.isnan(avg_left) and not math.isnan(avg_right):
                        center = int((avg_left + avg_right) / 2)

                elif len(left_lines) == 0:  # left_lines 감지 되지 않았을 경우 
                    center = 30
                elif len(right_lines) == 0: # right_lines 감지되지 않았을 경우 
                    center = 610

                cv2.circle(crop_img, (int(center), 100), 30, (255, 250, 0), 5)

                print(prox.value)
                if prox.value < 25 :    # 25cm 이내에 물체가 있는 경우
                    print('Emergency Stop!')
                    motor.stop()
                elif traffic_light == 'red' :   #신호등이 빨간불인 경우 
                    print('Red Light Stop!')
                    motor.stop()
                elif center < 260 :     # 중심이 왼쪽으로 밀렸을 경우 
                    print('turn left')
                    motor.left()
                elif center > 380 :     # 중심이 오른쪽으로 밀렸을 경우
                    print('turn right')
                    motor.right()
                else :
                    print('go')
                    motor.go()

            cv2.line(frame, (320, 0), (320, 640), (255, 0, 0), 2)
            cv2.line(frame, (0, 430), (640, 430), (255, 0, 0), 2)

            cv2.imshow('Original', frame)
            cv2.imshow('Edge', edge)

            if cv2.waitKey(1) == ord('q'):
                camera.release()
                cv2.destroyAllWindows()
                motor.stop()
                break

    camera.release()
    motor.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    prox = Value('f', 400.0)    # processing Value 이용해서 공유 메모리 만듦
    process = Process(target=read_distance, args=(prox, ))  # 프로세스 형성
    process.daemon = True       # 백그라운드 프로세스
    process.start()
    main()
    process.join()  # main 프로세스가 종료될 때까지 대기



