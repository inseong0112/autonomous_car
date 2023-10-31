import cv2
import numpy as np

# 비디오 캡처 초기화
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # 너비
camera.set(4, 480)  # 높이

def combine_similar_lines(lines):
    combined_lines = []
    if lines is not None:
        lines = np.squeeze(lines)  # 3D 배열을 2D로 변경
        if len(lines) > 0:
            slopes = [(y2 - y1) / (x2 - x1) for x1, y1, x2, y2 in lines]
    
            while len(lines) > 0:
                line = lines[0]
                lines = lines[1:]
                x1, y1, x2, y2 = line

                # 기울기가 유사한 선을 찾음
                similar_lines = [line]
                similar_slopes = [slopes[0]]
                i = 0
                while i < len(lines):
                    if abs(slopes[i] - slopes[0]) < 0.5:  # 임의의 기울기 차이 임계값
                        similar_lines.append(lines[i])
                        similar_slopes.append(slopes[i])
                        lines = np.delete(lines, i, axis=0)
                        slopes.pop(i)
                    else:
                        i += 1

                # 평균 기울기를 사용하여 하나의 선으로 결합
                average_slope = np.mean(similar_slopes)
                x1_avg, y1_avg, x2_avg, y2_avg = np.mean(similar_lines, axis=0, dtype=int)
                combined_lines.append((x1_avg, y1_avg, x2_avg, y2_avg))

    return np.array(combined_lines)


while camera.isOpened():
    ret, frame = camera.read()

    # 이미지를 원하는 크기로 자르기 (예: 하단 부분)
    crop_img = frame[300:480, 0:640]

    # 흑백 변환
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용 (잡음 제거)
    Gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    Median_blur = cv2.medianBlur(Gaussian_blur, 3)

    # 이진화 (흰색 강조)
    _, thresh1 = cv2.threshold(Median_blur, 200, 255, cv2.THRESH_BINARY)

    # 팽창 연산 (물체 연결)
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Canny 엣지 감지
    edges2 = cv2.Canny(mask, 50, 200)

    # 허프 변환을 사용하여 선 탐지
    lines = cv2.HoughLinesP(edges2, 1, np.pi / 180, 100, maxLineGap=2000)

    if lines is not None:

        # 기울기가 유사한 선들을 하나의 선으로 합치기
        combined_lines = combine_similar_lines(lines)
        
        # 그림을 그릴 이미지 복사
        result_image = crop_img.copy()

        # 합쳐진 선 그리기
        for line in combined_lines:
            x1, y1, x2, y2 = line
            cv2.line(result_image, (x1, y1), (x2, y2), (0, 0, 255), 5)

        # 화면에 이미지 출력
        cv2.imshow('Original', frame)
        cv2.imshow('Combined Lines', result_image)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
