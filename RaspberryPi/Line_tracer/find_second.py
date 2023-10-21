my_list = [10, 25, 30, 50, 40, 60]

# 리스트에서 max 값 찾기
max_value = max(my_list)

# max_value보다 작으면서 가장 큰 값을 찾기
second_largest = None  # 두 번째로 큰 값을 저장할 변수

for item in my_list:
    if item < max_value:
        if second_largest is None:
            second_largest = item
        elif item > second_largest:
            second_largest = item

# 결과 출력
print("Max:", max_value)
print("Second largest:", second_largest)