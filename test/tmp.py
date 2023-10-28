import cv2
import traffic_light
import multiprocessing
import numpy as np

red_light = None

def detect_traffic_light(frame, result_queue):
    global red_light
    red_light = traffic_light.detect(frame)
    result_queue.put(red_light)

if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    result_queue = multiprocessing.Queue()
    process = None
    process = multiprocessing.Process(target=detect_traffic_light, args=(camera, result_queue))
    process.start()
    while camera.isOpened():
        ret, frame = camera.read()
        
        #if process is None or not process.is_alive():
            #process = multiprocessing.Process(target=detect_traffic_light, args=(frame, result_queue))
            #process.start()

#        if not result_queue.empty():
            #red_light = result_queue.get()
        
        try:
            # Here you can use the red_light variable for your desired actions
            if red_light == 'red':
                print("Stop!")
            elif red_light == 'green':
                print("Go!")
            elif red_light == 'yellow':
                print("Prepare to stop!")
                
            
            

        except KeyboardInterrupt:
            # Ctrl+C to exit the program
            break
        cv2.imshow('frame', frame)

    if process is not None and process.is_alive():
        process.terminate()

    # Release the camera and close all OpenCV windows
    camera.release()
    cv2.destroyAllWindows()
