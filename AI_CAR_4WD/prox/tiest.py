import p
import threading
import time
import sys
from multiprocessing import Manager, Process
import motor


distances = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
def get_and_print_distance():
    global distances
    distances = Manager().list()
    while True : 
        distances = p.get_distance()

if __name__ == '__main__':
    try:
        #define processes
        sensor_process = Process(target=get_and_print_distance)
        sensor_process.start()
        go_process = Process(target=motor.go)
        go_process.start()
        left_process = Process(target=motor.left)
        left_process.start()
        right_process = Process(target=motor.right)
        right_process.start()
        stop_process = Process(target=motor.stop)
        stop_process.start()
        

        while True :
            if len(distances)>1 and distances[1]<20 : 
                stop_process.join()
                print('stoop!')
            else : 
                go_process.join()

        
    except KeyboardInterrupt:
        stop_process.join()
        # GPIO 리소스 정리 코드 추가
