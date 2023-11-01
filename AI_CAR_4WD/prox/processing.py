import multiprocessing
import other_file
import time

def do_something():
    other_file.do_something()

if __name__ == "__main__":
    # 함수를 별도의 프로세스로 시작
    process = multiprocessing.Process(target=do_something)
    
    try:
        # 프로세스 시작
        process.start()
        
        # 메인 스레드에서 다른 작업을 수행할 수 있음
        while True:
            print("Main thread working...")
            #time.sleep(2)
            
    except KeyboardInterrupt:
        # KeyboardInterrupt(Ctrl+C)를 받으면 프로세스 종료
        process.terminate()
        process.join()



####################################################################################################################

def evasion() :
    print('called')
    turn_times = 0
    go_times = 0
    turn_tmp = 0
    go_tmp = 0
    #if distances[0] > distances[2] : #좌측 이동
        #print('1')
    print(distances[2])
    while distances[2] > 25 :
        print('turn left')
        motor_left()
        turn_times += 1
        time.sleep(0.5)
    turn_tmp = turn_times
    while distances[4] > 35 :
        print('go')
        motor_go()
        go_times += 1
        time.sleep(0.5)
    go_tmp = go_times
    while turn_times : 
        motor_right()
        print('turn right')
        turn_times -= 1
        time.sleep(0.5)
    
    
    while distances[6] > 20 : #차 끝까지 이동
        print('go')
        motor_go()
        time.sleep(0.5)
        
    #car passing obj
    turn_times = turn_tmp
    while turn_times : 
        motor_right()
        print('turn right')
        turn_times -= 1
        time.sleep(0.5)
    while go_times :
        motor_go()
        print('go')
        go_times -= 1
    turn_times = turn_tmp
    while turn_times :
        print('turn left')
        motor_left()
        turn_times -= 1
        time.sleep(0.5)
    print("OK!")

def main():
    k=0
    print("i'm main")
    go_process.start()
    while True:
        
        motor_go()
        print('go')
        if len(distances) > 1 and distances[1]<15 : 
            motor_stop()
            print("stop!")
            evasion()
        else :
            #print("go! "+str(k))
            #k+=1
            motor_go()
        time.sleep(0.1)