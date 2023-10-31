import RPi.GPIO as GPIO
import time

servoPIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p1 = GPIO.PWM(servoPIN, 50)

p1.start(7) # Init

current = 70
def go():
    global current
    p1.ChangeDutyCycle(7)
    time.sleep(0.3)
    current = 70

def right():
    global current
    # Servo 모터가 천천히 회전하도록
    for duty in range(int(current), 115, 20): 
        p1.ChangeDutyCycle(duty/10)
        time.sleep(0.03)

    print(int(current))
    current = 115

def left():
    global current
    # Servo 모터가 천천히 회전하도록
    for duty in range(int(current), 25, -20):
        p1.ChangeDutyCycle(duty/10)
        time.sleep(0.03)

    print(int(current))
    current = 25


