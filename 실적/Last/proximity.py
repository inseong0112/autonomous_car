import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG_PIN = 20
ECHO_PIN = 21
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def read_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.3)  # 센서를 초기화하기 위한 시간
    
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    pulse_start = 0  # pulse_start 변수 초기화
    pulse_end = 0  # pulse_end 변수 초기화
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2  # 초당 343m 속도로 음파가 이동
    return round(distance, 2)       #소수점 두번째에서 반올림 








if __name__ == '__main__':
    try:
        while True:
            distance = read_distance()
            print(f"Distance: {distance} cm")
            time.sleep(0.001)
        
    except KeyboardInterrupt:
        GPIO.cleanup()




