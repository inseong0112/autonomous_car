import RPi.GPIO as GPIO
import time

servoPIN1 = 5
servoPIN2 = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)
p1 = GPIO.PWM(servoPIN1, 50) # GPIO 17 for PWM with 50Hz
p2 = GPIO.PWM(servoPIN2, 50) # GPIO 17 for PWM with 50Hz
p1.start(6) # Initialization
p2.start(6) # Initialization

def set_angle(angle) :
    GPIO.setup(servoPIN1, GPIO.OUT)
    p1.ChangeDutyCycle(angle/18 + 2)
    time.sleep(0.05)
    GPIO.setup(servoPIN1, GPIO.IN)
    time.sleep(0.05)
    GPIO.setup(servoPIN2, GPIO.OUT)
    p2.ChangeDutyCycle(angle/18 + 2)
    time.sleep(0.05)
    GPIO.setup(servoPIN2, GPIO.IN)
    
for i in range(9):
    set_angle(90+(i*10))
    time.sleep(1)

import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
try:
  while True:
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    p.ChangeDutyCycle(12.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(2.5)
    time.sleep(0.5)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()