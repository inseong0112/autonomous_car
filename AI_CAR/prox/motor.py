from gpiozero import Motor
import sys

motorA = Motor(forward=8, backward=7)
motorB = Motor(forward=24, backward=23)
motorC = Motor(forward=10, backward=9)
motorD = Motor(forward=22, backward=27)

def go():
    motorA.forward(1)
    motorB.forward(1)
    motorC.forward(1)
    motorD.forward(1)
def back():
    motorA.backward(1)
    motorB.backward(1)
    motorC.backward(1)
    motorD.backward(1)
def right():
    motorA.forward(0.6)
    motorB.backward(0.6)
    motorC.forward(0.6)
    motorD.backward(0.6)
def left():
    motorA.backward(0.6)
    motorB.forward(0.6)
    motorC.backward(0.6)
    motorD.forward(0.6)
def stop():
    motorA.stop()
    motorB.stop()
    motorC.stop()
    motorD.stop()

sys.stdout.flush

