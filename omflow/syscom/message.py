'''
message process module
@author: Pen Lin
'''
from  enum import IntEnum
import json
from django.http.response import JsonResponse

class ResponseAjax():
    '''
    convert data to json , and return to client
    '''
    def __init__(self, status_code, status_message, status_result=None):
        '''
        init class
        input:status_code,statusEnum code;status_message,message text,result
        return:no
        author:Pen Lin,Jia Liu
        '''
        self.code = status_code
        self.message = status_message
        self.result = status_result
    def returnJSON(self):
        '''
        return JsonResponse for HTTP
        author:Pen Lin
        '''
        return JsonResponse(self.getDict(), safe=False)
           
    def getJson(self):
        '''
        return json format
        input:no
        return:no
        author:Pen Lin,Jia Liu
        '''
        output = {}
        output['status'] = int(self.code)
        output['message'] = self.message
        output['result'] = self.result
        return json.dumps(output)
    
    def getDict(self):
        '''
        get python dict object
        input:no
        return:dict
        author:Pen Lin,Jia Liu
        '''
        output = {}
        output['status'] = int(self.code)
        output['message'] = self.message
        output['result'] = self.result
        return output
    
    def __str__(self):
        '''
        return status code
        input:no
        return:no
        author:Pen Lin
        '''
        return self.code
    
class statusEnum(IntEnum):
    '''
    HTTP Return Code
    input:no
    return:200/403/404/500
    author:Pen Lin
    '''
    success = 200
    no_permission = 403
    not_found = 404
    error = 500
    

    
    