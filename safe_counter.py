import threading

class SafeCounter:
    def __init__(self, length):
        self.counter = 0
        self.length = length
        self.mutex = threading.Lock()

    def check(self):
        return counter

    def get(self):
        if (self.counter >= self.length): 
            return -1
        self.mutex.acquire()
        counter = self.counter
        self.counter += 1
        self.mutex.release()
        return counter