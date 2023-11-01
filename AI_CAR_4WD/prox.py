## 반복문 사용으로 센서 값 불러오는 코드

import RPi.GPIO as GPIO
import time
import sys

# GPIO 핀 설정
trigPins = [2, 4, 14, 11, 18, 19, 20]
echoPins = [3, 17, 15, 5, 25, 26, 21]
distances=[0, 0, 0, 0, 0, 0, 0, 0]
# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPins, GPIO.OUT)
GPIO.setup(echoPins, GPIO.IN)

def get_distance(trig_pin, echo_pin):
    #print("d")
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)
    #print("s")
    pulse_start = time.time()
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # 소리의 속도 (약 34300 cm/s) / 2
    #print('f')
    return distance  # 거리 값을 반환

try:
    while True:
        a=[]
        for i in range(7) :
            a.append(get_distance(trigPins[i], echoPins[i]))
            time.sleep(0.03)
            if a[i]<10:
                print(str(i+1) + " danger")
                
        print(a)
        sys.stdout.flush()
            
            
        #print('ok')
        
except KeyboardInterrupt:
    pass

finally:
    print("cleanup")
    GPIO.cleanup()

