import threading, time

sem = threading.Semaphore(3)

def run():
    with sem:
        for i in range(5):
            print('{}--{}'.format(threading.current_thread().name, i))
            time.sleep(1)

if __name__ == '__main__':
    for i in range(5):
        threading.Thread(target=run).start()


