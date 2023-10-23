import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG_PIN = 17
ECHO_PIN = 18
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
def read_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(2)  # 센서를 초기화하기 위한 시간
    
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2  # 초당 343m 속도로 음파가 이동
    return round(distance, 2)
try:
    while True:
        distance = read_distance()
        print(f"Distance: {distance} cm")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
