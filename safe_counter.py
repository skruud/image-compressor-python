import threading

class SafeCounter:
    def __init__(self):
        self.counter = 0
        self.mutex = threading.Lock()

    def get(self):
        self.mutex.acquire()
        counter = self.counter
        self.counter += 1
        self.mutex.release()
        return counter