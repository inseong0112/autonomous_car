import RPi.GPIO as GPIO
import time
import sys

# GPIO 핀 설정
trigPins = [2, 4, 14, 11, 18, 19, 20]
echoPins = [3, 17, 15, 5, 25, 26, 21]

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPins, GPIO.OUT)
GPIO.setup(echoPins, GPIO.IN)

def calc_distance(trig_pin, echo_pin): 
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
    distance = pulse_duration * 17150 
    return distance

def get_distance():
    distances=[]
    for i in range(7) :
        distances.append(calc_distance(trigPins[i], echoPins[i]))
        time.sleep(0.04)
    return distances
        
try:
    while True:
        a = get_distance()
        print(a)
        
                
        
except KeyboardInterrupt:
    pass

finally:
    print("cleanup")
    GPIO.cleanup()



