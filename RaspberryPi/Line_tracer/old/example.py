import cv2
import numpy as np

# 두 선의 기울기 차이가 이 값보다 작으면 합침 (임의 값)
max_slope_difference = 0.1

def combine_similar_lines(lines):
    combined_lines = []
    lines = np.squeeze(lines)  # 3D 배열을 2D로 변경
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
            if abs(slopes[i] - slopes[0]) < max_slope_difference:
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

# 테스트를 위한 가상의 선들
test_lines = np.array([[[1, 2, 10, 20]], [[3, 6, 12, 24]], [[20, 40, 50, 100]]])

# 유사한 기울기를 가진 선들을 하나로 합침
combined_lines = combine_similar_lines(test_lines)
print("Combined Lines:", combined_lines)
