import cv2
import numpy as np
from gpiozero import Motor

motorA = Motor(forward=8, backward=7)
motorB = Motor(forward=24, backward=23)
motorC = Motor(forward=10, backward=9) ##change need
motorD = Motor(forward=22, backward=27)

def motor_go():
    motorA.forward(1)
    motorB.forward(1)
    motorC.forward(1)
    motorD.forward(1)
def motor_back():
    motorA.backward(1)
    motorB.backward(1)
    motorC.backward(1)
    motorD.backward(1)
def motor_right():
    motorA.forward(1)
    motorB.backward(1)
    motorC.forward(1)
    motorD.backward(1)
def motor_left():
    motorA.backward(1)
    motorB.forward(1)
    motorC.backward(1)
    motorD.forward(1)
def motor_stop():
    motorA.stop()
    motorB.stop()
    motorC.stop()
    motorD.stop()

def manual():
    while(1):
        keyValue = cv2.waitKey(10)
        if keyValue == ord('q'):
            print("stop")
            motor_stop()
            break
        if keyValue == ord('w'):
            print("go")
            motor_go()
        elif keyValue == ord('s'):
            print("back")
            motor_back()
        elif keyValue == ord('a'):
            print("left")
            motor_left()
        elif keyValue == ord('d'):
            print("right")
            motor_right()
        if keyValue == ord('b'):
            print("stop")
            motor_stop()
  
def main():
    camera = cv2.VideoCapture(-1)
    camera.set(3,640) #160
    camera.set(4,480) #120

    while( camera.isOpened() ):
        ret, frame = camera.read()
        frame = cv2.flip(frame,-1)
        cv2.imshow('normal',frame)


        if cv2.waitKey(1) == ord('m'):
            print("manual")
            manual()
            
        if cv2.waitKey(1) == ord('q'):
            motor_stop()
            break
    cv2.destroyAllWindows()
    motor_stop()

if __name__ == '__main__':
    main()
