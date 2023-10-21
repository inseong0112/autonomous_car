import cv2
import time
import datetime
import command

def capture():
    camera = cv2.VideoCapture(0)  # 0 for the default camera
    if not camera.isOpened():
        print("Error: Camera not found.")
        return

    # Set the width and height of the frame
    camera.set(3, 1920)
    camera.set(4, 1080)

    ret, frame = camera.read()
    camera.release()

    if not ret:
        print("Error capturing image")
        return

    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'

    # Rotate the captured image (if needed)
    # frame = cv2.rotate(frame, cv2.ROTATE_180)

    cv2.imwrite('./' + filename, frame)
    print(f"Image saved as {filename}")
    return filename

def main():
    filename = capture()
    command(filename)
    return filename

if __name__ == "__main__":
    main()
