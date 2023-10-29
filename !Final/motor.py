from gpiozero import Motor
import time
import RPi.GPIO as GPIO
import servo


motorA = Motor(forward=8, backward=7)
motorB = Motor(forward=9, backward=10)

def go():
    motorA.forward(0.7)
    motorB.forward(0.7)
    servo.go()

def back():
    motorA.forward(1)
    motorB.forward(1)

def right():
    motorA.forward(0.7)
    motorB.forward(0.5)
    servo.right()

def left():
    motorA.forward(0.5)
    motorB.forward(0.7)
    servo.left()

def back():
    motorA.backward(0.8)
    motorB.backward(0.8)

def stop():
    motorA.stop()
    motorB.stop()
    #motorC.stop()
    #motorD.stop()

if __name__ == '__main__' :
    try :
        time.sleep(0.5)
        go()
        time.sleep(0.5)
        #left()
        #time.sleep(2)
        #right()
        #time.sleep(2)
        #go()
        #time.sleep(2)
        stop()
        
        servo.p1.stop()
        servo.p2.stop()
        
    except KeyboardInterrupt:
        
        servo.p1.stop()
        servo.p2.stop()
        stop()
        