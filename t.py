import turtle

# 초기화
screen = turtle.Screen()
screen.bgcolor("white")

# Turtle 설정
snowflake = turtle.Turtle()
snowflake.speed(0)
snowflake.color("blue")

# 눈 결정 프랙탈을 그리는 함수
def draw_snowflake_side(snowflake, length, depth):
    if depth == 0:
        snowflake.forward(length)
        return
    length /= 3.0
    draw_snowflake_side(snowflake, length, depth-1)
    snowflake.left(60)
    draw_snowflake_side(snowflake, length, depth-1)
    snowflake.right(120)
    draw_snowflake_side(snowflake, length, depth-1)
    snowflake.left(60)
    draw_snowflake_side(snowflake, length, depth-1)

def draw_snowflake(snowflake, length, depth):
    for _ in range(6):
        draw_snowflake_side(snowflake, length, depth)
        snowflake.right(60)

# 프랙탈 그리기
snowflake.penup()
snowflake.goto(-150, 90)
snowflake.pendown()
draw_snowflake(snowflake, 300, 4)

# 화면 유지
screen.mainloop()
