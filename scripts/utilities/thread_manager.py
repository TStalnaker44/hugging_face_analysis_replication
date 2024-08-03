
import threading

class ThreadManager():

    def __init__(self, target_function, lyst, thread_count, *args, **kwargs):
        self.target = target_function
        self.args = args
        self.kwargs = kwargs
        self.threads = self.makeThreads(lyst, thread_count)
        
    def calculateSplit(self, lyst, thread_count):
        item_count = len(lyst)
        split = item_count // thread_count
        if split != item_count / thread_count:
            extra = item_count % thread_count
        else: extra = 0
        return split, extra
    
    def makeThreads(self, lyst, thread_count):
        split, extra = self.calculateSplit(lyst, thread_count)
        threads = []
        for i in range(thread_count):
            start = i * split
            end = start + split
            if end + split >= len(lyst):
                end += extra
            th = WorkerThread(self.target, lyst[start:end], *self.args, **self.kwargs)
            threads.append(th)
        return threads
    
    def run(self):
        for thread in self.threads:
            thread.start()

    def join(self):
        for thread in self.threads:
            thread.join()

    def get_results(self, combine_func=None):
        results = [thread.get_result() for thread in self.threads]
        if combine_func == None:
            return results
        else:
            return combine_func(results)

class WorkerThread(threading.Thread):

    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = self.target(*self.args, **self.kwargs)

    def get_result(self):
        return self.result