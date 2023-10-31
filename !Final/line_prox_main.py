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

def read_distance(prox):
    while True : 
        prox.value = proximity.read_distance()
        time.sleep(0.1)

def manual():
    while(1):
        keyValue = cv2.waitKey(10)
        if keyValue == ord('q'):
            print("stop")
            motor.stop()
            break
        if keyValue == ord('w'):
            print("go")
            motor.go()
        elif keyValue == ord('s'):
            print("back")
            motor.back()
        elif keyValue == ord('a'):
            print("left")
            motor.left()
        elif keyValue == ord('d'):
            print("right")
            motor.right()
        if keyValue == ord('b'):
            print("stop")
            motor.stop()

def detect(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    global red_light
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
    maskr = cv2.inRange(hsv, lower_red2, upper_red2)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #maskr = cv2.inRange(mask2)

    # 색상에 따라 윤곽선 찾기
    contours_red, _ = cv2.findContours(maskr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(masky, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(maskg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 각 색상에 맞는 사각형 그리고 넓이 출력
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area >= 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 빨간색
            cv2.putText(frame, f'Red: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return 'red'

    for contour in contours_yellow:
        area = cv2.contourArea(contour)
        if area >= 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # 노란색
            cv2.putText(frame, f'Yellow: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            return 'yellow'

    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area >= 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 초록색
            cv2.putText(frame, f'Green: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return 'green'

    key = cv2.waitKey(1)

    if key == ord('q'):
        return None
    else:
        return 'unknown'

def main():
    while camera.isOpened():
        ret, frame = camera.read()

        if ret:
            traffic_light_roi = frame[0:300, 0:640]
            traffic_light = detect(traffic_light_roi)
            cv2.imshow('roi', traffic_light_roi)



            #차선 인식 위치
            crop_img = frame[340:400, 0:640]

            # 흑백 변환
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

            # 가우시안 블러 적용 (잡음 제거)
            Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
            Median_blur = cv2.medianBlur(Gaussian_blur, 3)

            # Canny 엣지 감지
            edges2 = cv2.Canny(Median_blur, 50, 200)

            # 허프 변환을 사용하여 선 탐지
            lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 20, maxLineGap=200)
            left_lines = []  # 왼쪽에 있는 직선
            right_lines = []  # 오른쪽에 있는 직선

            avg_left = 0 # 최대 최소 / 2 전체평균 아님!!
            avg_right = 0

            if lines is not None:

                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    slope = (y2 - y1) / (x2 - x1)
                    intercept = y1 - slope * x1 #y절편
                    # 교점 x 좌표 계산
                    intersection_x = (100 - intercept) / slope  # 위에서 계산한 방법 사용

                    # 320을 기준으로 왼쪽과 오른쪽 판단
                    if intersection_x < 320:
                        left_lines.append(intersection_x)
                        cv2.line(crop_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    else:
                        right_lines.append(intersection_x)
                        cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                if len(left_lines) > 0 and len(right_lines) > 0:  # left_lines와 right_lines에 값이 있는지 확인
                    avg_left = (max(left_lines) + min(left_lines)) / 2
                    avg_right = (max(right_lines) + min(right_lines)) / 2

                    if not math.isinf(avg_left) and not math.isinf(avg_right) and not math.isnan(avg_left) and not math.isnan(avg_right):
                        center = (int((avg_left + avg_right) / 2), 50)

                elif len(left_lines) == 0:
                    center = (0, 50)
                elif len(right_lines) == 0:
                    center = (640, 50)

                cv2.circle(crop_img, center, int(30), (255, 250, 0), 5)
                #print(center[0])
                print(prox.value)
                if int(prox.value) < 30 :
                    print('Stop!!')
                    motor.go()
                    time.sleep(0.1)
                    motor.stop()
                    time.sleep(0.5)
                    motor.back()
                    time.sleep(1)
                    
                    motor.right()
                    time.sleep(1)
                    motor.go()
                    time.sleep(0.4)
                
                    motor.left()
                    time.sleep(2)
                    
                    #motor.go()
                    #time.sleep(0.2)
                    
                    motor.left()
                    time.sleep(2)
                    motor.right()
                    
                    time.sleep(1.5)
                    
                elif traffic_light == 'red':
                    print('Red Light Stop!')
                    motor.stop()
                elif center[0] < 260 :#275
                    print('turn left')
                    motor.left()
                elif center[0] > 380: #375
                    print('turn right')
                    motor.right()
                else :
                    print('go')
                    motor.go()


            cv2.line(frame, (320, 0), (320, 640), (255, 0, 0), 2)
            cv2.line(frame, (0, 430), (640, 430), (255, 0, 0), 2)
            cv2.imshow('Original', frame)
            cv2.imshow('Edges2', edges2)
            #print(left_lines, right_lines)
            if cv2.waitKey(1) == ord('m'):
                manual()
            if cv2.waitKey(1) == ord('q'):
                camera.release()
                cv2.destroyAllWindows()
                motor.servo.p1.stop()
                break
    camera.release()
    motor.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    prox = Value('f', 0.0)
    process = Process(target=read_distance, args=(prox, ))
    process.daemon = True
    process.start()
    main()
    process.join()

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

def read_distance(prox):
    while True : 
        prox.value = proximity.read_distance()
        time.sleep(0.3)

def manual():
    while(1):
        keyValue = cv2.waitKey(10)
        if keyValue == ord('q'):
            print("stop")
            motor.stop()
            break
        if keyValue == ord('w'):
            print("go")
            motor.go()
        elif keyValue == ord('s'):
            print("back")
            motor.back()
        elif keyValue == ord('a'):
            print("left")
            motor.left()
        elif keyValue == ord('d'):
            print("right")
            motor.right()
        if keyValue == ord('b'):
            print("stop")
            motor.stop()

def detect(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    global red_light
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
    maskr = cv2.inRange(hsv, lower_red2, upper_red2)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #maskr = cv2.inRange(mask2)

    # 색상에 따라 윤곽선 찾기
    contours_red, _ = cv2.findContours(maskr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(masky, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(maskg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 각 색상에 맞는 사각형 그리고 넓이 출력
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area >= 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 빨간색
            cv2.putText(frame, f'Red: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return 'red'

    for contour in contours_yellow:
        area = cv2.contourArea(contour)
        if area >= 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # 노란색
            cv2.putText(frame, f'Yellow: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            return 'yellow'

    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area >= 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 초록색
            cv2.putText(frame, f'Green: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return 'green'

    key = cv2.waitKey(1)

    if key == ord('q'):
        return None
    else:
        return 'unknown'

def main():
    while camera.isOpened():
        ret, frame = camera.read()

        if ret:
            traffic_light_roi = frame[0:300, 0:640]
            traffic_light = detect(traffic_light_roi)
            cv2.imshow('roi', traffic_light_roi)



            #차선 인식 위치
            crop_img = frame[340:400, 0:640]

            # 흑백 변환
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

            # 가우시안 블러 적용 (잡음 제거)
            Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
            Median_blur = cv2.medianBlur(Gaussian_blur, 3)

            # Canny 엣지 감지
            edges2 = cv2.Canny(Median_blur, 50, 200)

            # 허프 변환을 사용하여 선 탐지
            lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 20, maxLineGap=200)
            left_lines = []  # 왼쪽에 있는 직선
            right_lines = []  # 오른쪽에 있는 직선

            avg_left = 0 # 최대 최소 / 2 전체평균 아님!!
            avg_right = 0

            if lines is not None:

                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    slope = (y2 - y1) / (x2 - x1)
                    intercept = y1 - slope * x1 #y절편
                    # 교점 x 좌표 계산
                    intersection_x = (100 - intercept) / slope  # 위에서 계산한 방법 사용

                    # 320을 기준으로 왼쪽과 오른쪽 판단
                    if intersection_x < 320:
                        left_lines.append(intersection_x)
                        cv2.line(crop_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    else:
                        right_lines.append(intersection_x)
                        cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                if len(left_lines) > 0 and len(right_lines) > 0:  # left_lines와 right_lines에 값이 있는지 확인
                    avg_left = (max(left_lines) + min(left_lines)) / 2
                    avg_right = (max(right_lines) + min(right_lines)) / 2

                    if not math.isinf(avg_left) and not math.isinf(avg_right) and not math.isnan(avg_left) and not math.isnan(avg_right):
                        center = (int((avg_left + avg_right) / 2), 50)

                elif len(left_lines) == 0:
                    center = (30, 50)
                elif len(right_lines) == 0:
                    center = (610, 50)

                cv2.circle(crop_img, center, int(30), (255, 250, 0), 5)
                #print(center[0])
                if prox < 30 : 
                    print('Stop!!')
                    motor.stop()
                elif traffic_light == 'red':
                    print('Red Light Stop!')
                    motor.stop()
                elif center[0] < 260 :#275
                    print('turn left')
                    motor.left()
                elif center[0] > 380: #375
                    print('turn right')
                    motor.right()
                else :
                    print('go')
                    motor.go()


            cv2.line(frame, (320, 0), (320, 640), (255, 0, 0), 2)
            cv2.line(frame, (0, 430), (640, 430), (255, 0, 0), 2)
            cv2.imshow('Original', frame)
            cv2.imshow('Edges2', edges2)
            #print(left_lines, right_lines)
            if cv2.waitKey(1) == ord('m'):
                manual()
            if cv2.waitKey(1) == ord('q'):
                motor.servo.p1.stop()
                motor.servo.p2.stop()
                break
    camera.release()
    motor.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    prox = Value('f', 0.0)
    process = Process(target=read_distance, args=(prox, ))
    process.daemon = True
    process.start()
    main()
    process.join()
