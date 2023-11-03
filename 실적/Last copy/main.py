# main.py
import cv2
from multiprocessing import Process
import time

import detect  # detect.py를 import

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ret, frame = camera.read()
def detect_traffic_light(frame):
    print("call")
    while True:
        
        traffic_light = detect.detect(frame)
        print(traffic_light)
        time.sleep(0.1)

def main():
    while camera.isOpened():
        ret, frame = camera.read()
        if ret:
            cv2.imshow('Original', frame)

            if cv2.waitKey(1) == ord('q'):
                camera.release()
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    traffic_process = Process(target=detect_traffic_light, args=(frame, ))
    traffic_process.daemon = True
    traffic_process.start()

    main()
