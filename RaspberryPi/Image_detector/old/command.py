import subprocess


def command(filename):
    command2 = "./darknet detector test cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights -ext_output -dont_show /home/pi03/darknet/img/" + filename + ".jpg -thresh 0.1 -out output/"+filename+".json"
    subprocess.call([command2], shell=True)
    
if __name__ == '__main__':
    command(filename)
