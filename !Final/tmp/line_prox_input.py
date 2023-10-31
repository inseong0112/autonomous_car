import cv2
import time
import motor
from multiprocessing import Process, Value


def manual():
    while(1):
        keyValue = cv2.waitKey(10)
        if keyValue == ord('q'):
            print("stop")
            motor.stop()
            break
        if keyValue == ord('w'):
            print("go")
            motor.go()
        elif keyValue == ord('s'):
            print("back")
            motor.back()
        elif keyValue == ord('a'):
            print("left")
            motor.left()
        elif keyValue == ord('d'):
            print("right")
            motor.right()
        if keyValue == ord('b'):
            print("stop")
            motor.stop()


def main():
    try :
        while True : 
            is_manual = input('manual -> m / self -> s : ')
            if is_manual == 'm' :
                manual()
            else :
                right = input('right : ')
                left = input('left : ')
                motor.go()
                time.sleep(0.1)
                motor.stop()
                time.sleep(0.5)
                motor.right()
                time.sleep(right)
                motor.go()
                time.sleep(0.5)
                motor.left()
                time.sleep(left)
                motor.go()
                time.sleep(0.2)
                motor.left()
                time.sleep(left)
                motor.go()
                time.sleep(0.5)
                motor.right()
                time.sleep(right)
    except KeyboardInterrupt :
        motor.stop()
        motor.servo.stop()
        
if __name__ == '__main__':
    main()