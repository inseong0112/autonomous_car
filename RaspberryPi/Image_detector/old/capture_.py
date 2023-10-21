import command
import picamera     
import time
import datetime

def capture():
    camera = picamera.PiCamera()   
    camera.resolution = (1920,1080) 
    camera.start_preview()         
    now=datetime.datetime.now()
    filename=now.strftime('%Y-%m-%d-%H-%M-%S')
    camera.rotation = 180
    camera.capture('/home/pi03/darknet/img/' + filename + '.jpg')
    camera.close()
    return filename

def main():
    filename = capture()
    command.command(filename)
    return filename
        
    
if __name__ == "__main__" :
    main()