import json
import time
import threading
import capture

def main():
    filename = capture.main()
    file = open('./output/' + filename + '.json')
    dict = json.load(file)
    list = []
    for key in dict[0]['objects']: 
        try: #item already exist
            list.index(key['name'])
            
        except ValueError: #item doesn't exist
            list.append(key['name'])
   
    print(list)
    try:
        list.index("cat") #find dangerous objects
        try:
            list.index("pottedplant")
            print("Dangerous!!")
            time.sleep(1)
            
            
        except ValueError:
            print("Cat!")
        
        
           
    except ValueError:
        print("OK")
            
    print("Stop!")



if __name__=='__main__':
    main()



