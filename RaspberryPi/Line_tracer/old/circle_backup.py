################반지름 30으로 맞춰서 원 그리기

import cv2
import numpy as np
import math

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while camera.isOpened():
    ret, frame = camera.read()
    #frame = cv2.flip(frame, -1)
    if ret:
        # 이미지를 원하는 크기로 자르기 (예: 하단 부분)
        crop_img = frame[300:400, 0:640]

        # 흑백 변환 및 Gaussian, Median 블러 적용 (잡음 제거)
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        Median_blur = cv2.medianBlur(Gaussian_blur, 3)
        # Canny 엣지 감지
        edges2 = cv2.Canny(Median_blur, 50, 200)
        # 허프 변환을 사용하여 선 탐지
        lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 20, maxLineGap=200)

        if lines is not None: ## 검출된 선이 없지 않을때 (=선이 있을 때만)
            positive_slopes = []  # 양수 기울기를 가진 선
            negative_slopes = []  # 음수 기울기를 가진 선
            
            negative_x = []  # 교점 x 좌표를 저장할 리스트
            positive_x = []
            avg_n = 0 #모든 x 접점의 평균
            k_n = 0
            avg_p = 0 #모든 x 접점의 평균
            k_p = 0

            # 양수 기울기를 가진 선과 음수 기울기를 가진 선에 대한 처리
            for line in lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1)
                if slope > 0: 
                    positive_slopes.append(line) 
                else:
                    negative_slopes.append(line)

            # 음수 기울기를 가진 직선에 대해 교점 x 좌표 계산
            for line in negative_slopes:
                x1, y1, x2, y2 = line[0]

                # 직선 방정식 계산
                slope = (y2 - y1) / (x2 - x1)
                if slope !=0 :
                    intercept = y1 - slope * x1

                    # 교점 x 좌표 계산
                    intersection_x = (50 - intercept) / slope
                    negative_x.append(intersection_x)

                    avg_n = avg_n + intersection_x
                    k_n = k_n + 1
            

            # 양수 기울기를 가진 직선에 대해 교점 x 좌표 계산
            for line in positive_slopes:
                x1, y1, x2, y2 = line[0]
                # 직선 방정식 계산
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1    
                # 교점 x 좌표 계산
                intersection_x = (50 - intercept) / slope
                positive_x.append(intersection_x)
                avg_p = avg_p + intersection_x
                k_p=k_p+1
            if avg_p !=0 and k_p !=0 : 
                avg_p = avg_p / k_p

            if avg_n !=0 and k_n !=0 : 
                avg_n = avg_n / k_n

            if negative_x:
                max_x = max(negative_x)
                min_x = min(negative_x)
            # 중심 좌표 계산
            center_x = abs(max_x + min_x) / 2
            center = abs(avg_n + avg_p) / 2
            if not math.isnan(avg_p) and not math.isnan(avg_n) and not math.isnan(max_x) and not math.isnan(max_x) and (max_x - min_x) != 0 and center_x<1000 and center_x>-1000:
                
                
                # 반지름 계산
                radius = abs(avg_n - avg_p) / 2
                # 원을 그리기 위한 중심 좌표 (x, y)
                center_coordinates = (int(center_x), 50)  # y 좌표는 고정
                if not math.isnan(center_x) and not math.isnan(radius):
                    # 중심 좌표와 반지름 값이 NaN이 아닌 경우에만 원을 그리도록 처리
                    cv2.circle(crop_img, center_coordinates, int(30), (255, 0, 0), 5)

                        
                    if avg_p and avg_n : 
                        max_min_n = (max(negative_x) + min(negative_x))/2
                        max_min_p = (max(positive_x) + min(positive_x))/2
                        c2 = (int((max_min_n+max_min_p)/2), 50) ###############################################################
                        print(c2)
                        #print(c2)
                        cv2.circle(crop_img, c2, int(30), (255, 250, 0), 5)
                        #cv2.circle(crop_img, center_coordinates, int(radius), (255, 0, 0), 5)

                        if(int((max_min_n+max_min_p)/2)) < 275:
                            print('turn left')
                        elif(int((max_min_n+max_min_p)/2)) > 375 : 
                            print('turn right')

                            

    
                    if radius < 30 : #!!반지름의 길이가 30보다 작을때(테이프의 두께)
                        # 원을 그리기
                        cv2.circle(crop_img, center_coordinates, int(30), (0, 0, 255), 5)
                    else :  #30보다 큼
                        cv2.circle(crop_img, center_coordinates, int(30), (0, 0, 255), 5)
    
            if positive_x:
                max_x = max(positive_x)
                min_x = min(positive_x)
                if not math.isinf(max_x) and not math.isinf(min_x):
                    # 중심 좌표 계산
                    center_x = (max_x + min_x) / 2
                    # 반지름 계산
                    radius = abs(max_x - min_x) / 2
                    #print("Green_r = ", radius)
                    # 원을 그리기 위한 중심 좌표 (x, y)
                    center_coordinates = (int(center_x), 50)  # y 좌표는 고정
                    # 원을 그리기
                    if radius < 30 : #!!반지름의 길이가 30보다 작을때(테이프의 두께)
                        # 원을 그리기
                        cv2.circle(crop_img, center_coordinates, int(30), (0, 255, 0), 5)
                    else : 
                        cv2.circle(crop_img, center_coordinates, int(30), (0, 255, 0), 5)
    
        cv2.line(frame, (320, 0), (320, 640), (255, 0, 0), 2)
        cv2.line(frame, (0, 350), (640, 350), (255, 0, 0), 2)
        cv2.imshow('Original', frame)
        cv2.imshow('Edges2', edges2)
    
        if cv2.waitKey(1) == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()
