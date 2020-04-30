'''
Created on 2019年12月24日
@author: kailin
'''
import queue, threading, json
from time import sleep
from importlib import import_module
from concurrent.futures.thread import ThreadPoolExecutor
from omflow.syscom.common import try_except


class QueueMonitor():
    
    def __init__(self, name):
        '''
        init class
        input: 
        return: no
        author: Kolin Hsu
        '''
        self.threadPool = ThreadPoolExecutor(max_workers=50)
        self.threadQueue = queue.Queue()
        self.Monitor_Running = False
        self.Monitor_Start = False
        self.value = {}
        self.name = name
    
    def setPool(self, workers):
        self.threadPool = ThreadPoolExecutor(max_workers=workers)
    
    def shutdownPool(self):
        self.threadPool.shutdown()
    
    @try_except
    def threadsubmit(self):
        while True:
            #get pool queue size
            pool_qsize = self.threadPool._work_queue.qsize()
            #get queue size
            queue_size = self.threadQueue.qsize()
            if pool_qsize == 0 and queue_size > 0 and self.Monitor_Start:
                #get json form queue
                jsonObj = self.threadQueue.get(block=True)
                #import module
                try:
                    module = import_module(jsonObj['module_name'])
                except:
                    pass
                    #flow object要從哪來?
                    if self.name == 'FormFlow':
                        from omformflow.views import flowMaker
                        flowMaker(jsonObj['param']['flow_uuid'])
                        module = import_module(jsonObj['module_name'])
                #submit threads
                self.threadPool.submit(getattr(module, jsonObj['method']),jsonObj['param'])
            sleep(0.00001)
    
    def stopMonitor(self):
        self.Monitor_Start =False
    
    def startMonitor(self):
        self.Monitor_Start = True
    
    def setRunning(self):
        if not self.Monitor_Running:
            self.Monitor_Running = True
            self.threadsubmit()
        if not self.Monitor_Start:
            self.startMonitor()
    
    def putQueue(self,module_name,method,param):
        item = {}
        #item = {'module_name':'omuser.main','method':'main','param':{'id':i,'sss':'sss','aaa':'aaa','bbb':'bbb'}}
        item['module_name'] = module_name
        item['method'] = method
        item['param'] = param
        self.threadQueue.put(item)
        if not self.Monitor_Running:
            t = threading.Thread(target=self.setRunning)
            t.start()
        if not self.Monitor_Start:
            self.startMonitor()
    
    def getQueueSize(self):
        return self.Scheduler_threadQueue.qsize()
    
    def getQueue(self):
        if not self.Monitor_Start:
            return list(self.threadQueue.queue)
        else:
            return False
    
    def removeQueue(self,data):
        try:
            self.threadQueue.queue.remove(data)
            return True
        except:
            return False
    
    def setValue(self,key,data):
        self.value[key] = data
    
    def getValue(self):
        return self.value
    
    def removeValue(self,key):
        try:
            result = self.value.pop(key)
            return result
        except:
            return False


FormFlowMonitor = QueueMonitor('FormFlow')
SchedulerMonitor = QueueMonitor('Scheduler')