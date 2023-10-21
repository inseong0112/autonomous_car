import cv2
import numpy as np
import math
from gpiozero import Motor

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


motorA = Motor(forward=8, backward=7)
motorB = Motor(forward=24, backward=23)
motorC = Motor(forward=10, backward=9)
motorD = Motor(forward=22, backward=27)

def motor_go():
    motorA.forward(1)
    motorB.forward(1)
    motorC.forward(1)
    motorD.forward(1)
def motor_back():
    motorA.backward(1)
    motorB.backward(1)
    motorC.backward(1)
    motorD.backward(1)
def motor_right():
    motorA.forward(1)
    motorB.backward(1)
    motorC.forward(1)
    motorD.backward(1)
def motor_left():
    motorA.backward(1)
    motorB.forward(1)
    motorC.backward(1)
    motorD.forward(1)
def motor_stop():
    motorA.stop()
    motorB.stop()
    motorC.stop()
    motorD.stop()

def manual():
    while(1):
        keyValue = cv2.waitKey(10)
        if keyValue == ord('q'):
            print("stop")
            motor_stop()
            break
        if keyValue == ord('w'):
            print("go")
            motor_go()
        elif keyValue == ord('s'):
            print("back")
            motor_back()
        elif keyValue == ord('a'):
            print("left")
            motor_left()
        elif keyValue == ord('d'):
            print("right")
            motor_right()
        if keyValue == ord('b'):
            print("stop")
            motor_stop()
def main():
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

                if center[0] < 275 :
                    print('turn left')
                    motor_left()
                elif center[0] > 375:
                    print('turn right')
                    motor_right()
                else :
                    print('go')
                    motor_go()


            cv2.line(frame, (320, 0), (320, 640), (255, 0, 0), 2)
            cv2.line(frame, (0, 350), (640, 350), (255, 0, 0), 2)
            cv2.imshow('Original', frame)
            cv2.imshow('Edges2', edges2)
            #print(left_lines, right_lines)
            if cv2.waitKey(1) == ord('q'):
                break
    camera.release()
    motor_stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
