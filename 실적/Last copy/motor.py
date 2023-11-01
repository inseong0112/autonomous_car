from gpiozero import Motor
import time
import RPi.GPIO as GPIO
import servo


motorA = Motor(forward=8, backward=7)
motorB = Motor(forward=9, backward=10)

def go():
    motorA.forward(0.65)
    motorB.forward(0.65)
    servo.go()

def back():
    motorA.forward(8)
    motorB.forward(8)

def right():
    motorA.forward(0.7)
    motorB.forward(0.45)
    servo.right()

def left():
    motorA.forward(0.45)
    motorB.forward(0.7)
    servo.left()

def back():
    motorA.backward(0.8)
    motorB.backward(0.8)

def stop():
    motorA.stop()
    motorB.stop() 
    servo.p1.stop()


if __name__ == '__main__' :
    stop()
        
