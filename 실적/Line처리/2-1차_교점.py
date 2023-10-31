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
        # ROI 지정
        crop_img = frame[300:480, 0:640]
        # 흑백 변환
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        # Gaussian Blur, Median Blur 적용
        Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        Median_blur = cv2.medianBlur(Gaussian_blur, 3)
        # Canny 엣지 감지
        edges2 = cv2.Canny(Median_blur, 50, 200)
        # 허프 변환을 사용하여 선 탐지
        lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 20, maxLineGap=200)
        if lines is not None:
            positive_slopes = []  # 양수 기울기를 가진 선
            negative_slopes = []  # 음수 기울기를 가진 선

            # 기울기 양수 음수 판단
            for line in lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1)

                if slope > 0:
                    positive_slopes.append(line)
                else:
                    negative_slopes.append(line)

            positive_x = [] # 기울기가 양수인 직선과 y=100 과의 교점의 x 좌표
            negative_x = [] # 기울기가 음수인 직선과 y=100 과의 교점의 x 좌표 
            
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
            if len(line)>0 : 
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
                        # 원 그리기
                        cv2.circle(crop_img, (int(center_x), 100), 30, (0, 0, 255), 5)

    
                
                if positive_x:
                    max_x = max(positive_x)
                    min_x = min(positive_x)

                    if not math.isinf(max_x) and not math.isinf(min_x):
                        # 중심 좌표 계산
                        center_x = (max_x + min_x) / 2
                        # 원 그리기
                        cv2.circle(crop_img, (int(center_x), 100), 30, (0, 255, 0), 5)

                # 기울기가 양수와 음수인 선의 교점 x 좌표의 평균값을 계산하고, 해당 좌표에 원을 그립니다.
                # 기울기가 양수와 음수인 선의 교점의 x좌표 평균 
                c2 = (int((avg_p + avg_n)/2), 100) 
                print(c2)
                cv2.circle(crop_img, c2, 30, (255, 250, 0), 5)
    
    
        cv2.imshow('Original', frame)
        cv2.imshow('Edges2', edges2)
    
        if cv2.waitKey(1) == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()