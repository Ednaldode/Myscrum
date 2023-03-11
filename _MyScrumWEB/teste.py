import threading
import time

def worker():
    time.sleep(20)
    print('Fim do worker')



for i in range(10):
    t = threading.Thread(target=worker)
    t.start()