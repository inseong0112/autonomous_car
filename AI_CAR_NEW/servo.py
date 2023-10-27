import RPi.GPIO as GPIO
import time


servoPIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p1 = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

p1.start(7) # Initialization

current = 70
def go():
    global current
    p1.ChangeDutyCycle(7)
    time.sleep(0.3)
    current = 70
    p1.ChangeDutyCycle(0)

def right():
    global current
    for duty in range(int(current), 105, 4):
        p1.ChangeDutyCycle(duty/10)
        time.sleep(0.03)

    print(int(current))
    current = 105
    p1.ChangeDutyCycle(0)

def left():
    global current
    for duty in range(int(current), 35, -4):
        p1.ChangeDutyCycle(duty/10)
        time.sleep(0.03)

    print(int(current))
    current = 35
    p1.ChangeDutyCycle(0)

go()
print('center')
time.sleep(2)
left()
print('left')
time.sleep(2)
right()
print('right')
time.sleep(2)
left()
print('left')
time.sleep(2)
go()
print('center')
time.sleep(2)