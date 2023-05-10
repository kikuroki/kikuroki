import time
import threading
def a(e:threading.Event):
    
    while True:
        
        
        if e.is_set():
            time.sleep(1)
            print(1)
    
k=threading.Event()
dic={'e':k}
threading.Thread(target=a,args=(dic['e'], )).start()
#dic['e']={'dsadas':'eqwewqe'}
dic['e'].set()
dic['e']=threading.Event()
threading.Thread(target=a,args=(dic['e'], )).start()
threading.Thread(target=a,args=(dic['e'], )).start()
threading.Thread(target=a,args=(dic['e'], )).start()
threading.Thread(target=a,args=(dic['e'], )).start()