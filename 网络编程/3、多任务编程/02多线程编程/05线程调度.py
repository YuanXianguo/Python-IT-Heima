import threading

con = threading.Condition()

def run1():
    for i in range(0, 10, 2):
        with con:
            print(threading.current_thread().name, i)
            con.wait()
            con.notify()

def run2():
    for i in range(1, 10, 2):
        with con:
            print(threading.current_thread().name, i)
            con.notify()
            con.wait()

threading.Thread(target=run1).start()
threading.Thread(target=run2).start()
