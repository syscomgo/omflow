'''
Created on 2019年12月24日
@author: kailin
'''
import queue, threading, json
from django.utils.translation import gettext as _
from time import sleep
from importlib import import_module
from concurrent.futures.thread import ThreadPoolExecutor
from omflow.syscom.common import try_except
from omflow.global_obj import FlowActiveGlobalObject
from omflow.syscom.default_logger import error


class QueueMonitor():
    
    def __init__(self, name):
        '''
        init class
        input: 
        return: no
        author: Kolin Hsu
        '''
        self.threadPool = ThreadPoolExecutor(max_workers=10)
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
                flow_uuid = jsonObj['param'].get('flow_uuid','')
                fa = None
                if flow_uuid:
                    fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                #import module
                try:
                    module_name = jsonObj['module_name']
                    l = module_name.split('.')
                    if l[0] == 'omformflow' and fa and self.name == 'FormFlow':
                        if l[-2] != fa.version:
                            module_name = 'omformflow.production.' + flow_uuid + '.' + str(fa.version) + '.main'
                    module = import_module(module_name)
                    #submit threads
                    self.threadPool.submit(getattr(module, jsonObj['method']),jsonObj['param'])
                except Exception as e:
                    try:
                        if fa:
                            error(_('找不到main.py'),e)
                        else:
                            error(_('找不到流程'),e)
                    except:
                        pass
            sleep(0.00001)
    
    def stopMonitor(self):
        self.Monitor_Start =False
    
    def startMonitor(self):
        self.Monitor_Start = True
    
    def setRunning(self):
        if not self.Monitor_Running:
            self.Monitor_Running = True
            self.threadsubmit()
    
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
LoadBalanceMonitor = QueueMonitor('LoadBalance')