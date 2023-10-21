import cv2
import numpy as np
import math

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while camera.isOpened():
    ret, frame = camera.read()
    
    if ret:
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
        lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 20, maxLineGap=200)

        if lines is not None:
            positive_slopes = []  # 양수 기울기를 가진 선
            negative_slopes = []  # 음수 기울기를 가진 선

            for line in lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1)

                if slope > 0:
                    positive_slopes.append(line)
                else:
                    negative_slopes.append(line)

            # 양수 기울기를 가진 선과 음수 기울기를 가진 선에 대한 처리

            # 점 (0, 100)과 (640, 100)을 지나는 직선 방정식 설정
            horizontal_line_1 = np.array([100, 200, 540, 200])
            negative_x = []  # 교점 x 좌표를 저장할 리스트
            positive_x = []
            avg_n = 0 #모든 x 접점의 평균
            k_n = 0
            # 음수 기울기를 가진 직선에 대해 교점 x 좌표 계산
            for line in negative_slopes:
                x1, y1, x2, y2 = line[0]

                # 직선 방정식 계산
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1

                # 교점 x 좌표 계산
                intersection_x = (100 - intercept) / slope
                negative_x.append(intersection_x)

                avg_n = avg_n + intersection_x
                k_n = k_n + 1

            avg_n = avg_n / k_n

            avg_p = 0 #모든 x 접점의 평균
            k_p = 0
            # 양수 기울기를 가진 직선에 대해 교점 x 좌표 계산
            for line in positive_slopes:
                x1, y1, x2, y2 = line[0]
                # 직선 방정식 계산
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1

                # 교점 x 좌표 계산
                intersection_x = (100 - intercept) / slope
                positive_x.append(intersection_x)

                avg_p = avg_p + intersection_x
                k_p=k_p+1

            avg_p = avg_p / k_p

            if negative_x:
                max_x = max(negative_x)
                min_x = min(negative_x)

                if not math.isinf(max_x) and not math.isinf(min_x):
                    # 중심 좌표 계산
                    center_x = (max_x + min_x) / 2
                    # 반지름 계산
                    radius = (max_x - min_x) / 2
                    #print("Red_r = ", radius)
                    # 원을 그리기 위한 중심 좌표 (x, y)
                    center_coordinates = (int(center_x), 100)  # y 좌표는 고정
                    
                    if avg_p and avg_n : 
                    
                        c2 = (int((avg_p + avg_n)/2), 100) ###############################################################
                        print(c2)
                        cv2.circle(crop_img, c2, int(radius), (255, 250, 0), 5)
                    cv2.circle(crop_img, center_coordinates, int(radius), (255, 0, 0), 5)

                    if radius < 30 : #!!반지름의 길이가 30보다 작을때(테이프의 두께)
                        # 원을 그리기
                        cv2.circle(crop_img, center_coordinates, int(radius), (0, 0, 255), 5)
                    else :  #30보다 큼
                        # 리스트에서 max 값 찾기
                        max_value = max_x

                        # max_value보다 작으면서 가장 큰 값을 찾기
                        second_largest = None  # 두 번째로 큰 값을 저장할 변수

                        for item in negative_x:
                            if item < max_value:
                                if second_largest is None:
                                    second_largest = item
                                elif item > second_largest:
                                    second_largest = item

                        # 결과 출력
                        #print("Max:", max_value)
                        #print("Second largest:", second_largest)
                        cv2.circle(crop_img, center_coordinates, int(30), (0, 0, 255), 5)

            if positive_x:
                max_x = max(positive_x)
                min_x = min(positive_x)
                if not math.isinf(max_x) and not math.isinf(min_x):
                    # 중심 좌표 계산
                    center_x = (max_x + min_x) / 2
                    # 반지름 계산
                    radius = (max_x - min_x) / 2
                    #print("Green_r = ", radius)
                    # 원을 그리기 위한 중심 좌표 (x, y)
                    center_coordinates = (int(center_x), 100)  # y 좌표는 고정
                    # 원을 그리기
                    if radius < 30 : #!!반지름의 길이가 30보다 작을때(테이프의 두께)
                        # 원을 그리기
                        cv2.circle(crop_img, center_coordinates, int(radius), (0, 255, 0), 5)
                    else : 
                        cv2.circle(crop_img, center_coordinates, int(30), (0, 255, 0), 5)


            

        cv2.imshow('Original', frame)
        cv2.imshow('Edges2', edges2)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
