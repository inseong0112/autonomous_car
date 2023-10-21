from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

dir = "C:/Users/hwang/OneDrive/Desktop/autonomous_car/RaspberryPi/Image_detector/keras/"

# Load the model
model = load_model(dir + "keras_Model.h5", compile=False)

# Load the labels
class_names = open(dir + "labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the web camera's image.
    ret, image_original = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image_original, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predict the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Display class name and confidence score on the image
    display_text = f"Class: {class_name[2:]}!, Confidence: {str(np.round(confidence_score * 100))[:-2]}%"
    cv2.putText(image_original, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the image in a window
    cv2.imshow("Webcam Image", image_original)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
