## 물체 회피 

import RPi.GPIO as GPIO
import time
import sys

# GPIO 핀 설정
trigPins = [2, 4, 14, 11, 18, 19, 20]
echoPins = [3, 17, 15, 5, 25, 26, 21]
distances=[]

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPins, GPIO.OUT)
GPIO.setup(echoPins, GPIO.IN)

#Motor 핀 설정
motorA = Motor(forward=8, backward=7)
motorB = Motor(forward=24, backward=23)
motorC = Motor(forward=10, backward=9)
motorD = Motor(forward=22, backward=27)

#움직임 코드
def motor_go():
    motorA.forward(0.7)
    motorB.forward(0.7)
    motorC.forward(0.7)
    motorD.forward(0.7)
def motor_back():
    motorA.backward(1)
    motorB.backward(1)
    motorC.backward(1)
    motorD.backward(1)
def motor_right():
    motorA.forward(0.6)
    motorB.backward(0.6)
    motorC.forward(0.6)
    motorD.backward(0.6)
def motor_left():
    motorA.backward(0.6)
    motorB.forward(0.6)
    motorC.backward(0.6)
    motorD.forward(0.6)
def motor_stop():
    motorA.stop()
    motorB.stop()
    motorC.stop()
    motorD.stop()

def get_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)
    
    pulse_start = time.time()
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # 소리의 속도 (약 34300 cm/s) / 2 (왕복)
    return distance

def evasion() :
    times1 = 0
    times2 = 0
    if distances[0] > distances[2] : #좌측 이동
        while distances[2] > 25 : 
            motor_left()
            times1 = times1 + 1
            times2 = times2 + 1
        while distances[4] > 35 : 
            motor_go()
        while times1 : 
            motor_right()
            times1 = times1 - 1 #times1 = 0됨
        while distances[6] > 20 : #차 끝까지 이동
            motor_go()
        while times2 : 
            motor_right()
            times2 = times2 - 1
            times1 = times1 + 1
        while times1 :
            motor_left()
            times1 = times1 - 1
        print("OK!")
    else : #우측 이동 
        while distances[0] > 25 : 
            motor_right()
            times1 = times1 + 1
            times2 = times2 + 1
        while distances[3] > 35 : 
            motor_go()
        while times1 : 
            motor_left()
            times1 = times1 - 1 #times1 = 0됨
        while distances[5] > 20 : #차 끝까지 이동
            motor_go()
        while times2 : 
            motor_left()
            times2 = times2 - 1
            times1 = times1 + 1
        while times1 :
            motor_right()
            times1 = times1 - 1
        print("OK!")


try:
    while True:
        
        for i in range(7) :
            distances.append(get_distance(trigPins[i], echoPins[i]))
            time.sleep(0.03)
            if distances[1] < 15 :
                print("stop!")
                motor_stop()
                evasion()
                
        #print(distances)
        sys.stdout.flush()
            
            
        #print('ok')
        
except KeyboardInterrupt:
    pass

finally:
    print("cleanup")
    GPIO.cleanup()



