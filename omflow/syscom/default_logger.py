import logging,sys
import base64
from django.urls.base import resolve
from pprint import pformat


class LowLevelFilter(object):
    '''
    Logging filter: Show log messages below input level.
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    NOTSET-to-INFO to stderr 
    author: Jia Liu
    ''' 
    #LOG等級在INFO以下印出STDERR
    def __init__(self, level):
        self.__level = level

    def filter(self, log):
        return log.levelno <= self.__level


class HighLevelFilter(object):
    '''
    Logging filter: Show log messages Above input level.
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    WARNING-to-CRITICAL to stdout
    '''
    #LOG等級在WARN以上印出STDOUT
    def __init__(self, level):
        self.__level = level

    def filter(self, log):
        return log.levelno >= self.__level
    

#設定LOG名稱
omflow_name = 'omflowlog'
root_name = 'django'
omflow_logger = logging.getLogger(omflow_name)
root_logger = logging.getLogger(root_name)



def IpUserget(*args):
    '''
    Get user,IP,path,function name
    input:request
    return: Get list
    author: Jia Liu
    ''' 
    #假如有Request參數,印出 IP、User、URL、view name 並組合字串丟到log裡面
    request = str(args)
    if 'Request' in request:
        ip = None
        ip = args[0].META.get('REMOTE_ADDR')
        user = None
        if args[0].user.is_authenticated:
            user = args[0].user.username
        else:
            try:
                basic_auth_str = args[0].headers['Authorization'][6:]
                username,password= base64.b64decode(
                    basic_auth_str).decode('utf-8').split(':')
                user = username
            except:
                user = "None"
        path = None
        path = args[0].META['PATH_INFO']
        url_name = resolve(path).url_name
        listall = [ip] + [user] + [path] + [url_name]
        alls = str(listall)
        return alls
    else:
        ip = "localhost"
        source = "system"
        listall = [ip] + [source]
        alls = str(listall)
        return alls


def debug(param,request=None):
    '''
    Set debug log message
    input: args
    return: log message
    author: Jia Liu
    ''' 
    msg = IpUserget(request) + ' - ' + str(param)
    omflow_logger.debug(msg)
    root_logger.debug(msg)
    #印出所有參數
    if request != None:
        post = request.POST
        if post != {}:
            posts = IpUserget(request) + ' - ' + '\n' + str(pformat(post))
            omflow_logger.debug(posts)
            root_logger.debug(posts)


def info(param,request=None):
    '''
    Set info log message,if log level set debug,print debug post
    input: args
    return: log message
    author: Jia Liu
    ''' 
    #假如有Request參數,印出 IP、User、URL、view name 以及自訂 info 訊息    
    msg = IpUserget(request) + ' - ' + str(param)
    omflow_logger.info(msg)
    root_logger.info(msg)

def error(param,request=None):
    '''
    Set error log message,print error exception and post error information
    input: args
    return: log message
    author: Jia Liu
    '''
    #假如有Request參數,印出 IP、User、URL、view name Exception，以及自訂Error訊息
    exc_tu = sys.exc_info()
    exc_bol = True
    if exc_tu.count(None) == 3:
        exc_bol = False
    else:
        exc_bol = True
    if request != None:
        errormsg = IpUserget(request) + ' - ' + str(param)
        omflow_logger.exception(errormsg,exc_info=exc_bol)
        root_logger.exception(errormsg,exc_info=exc_bol)
        #印出所有Request POST
        post = request.POST
        if post != {}:
            errorpost = IpUserget(request) + ' - ' + '\n' + str(pformat(post))
            omflow_logger.error(errorpost)
            root_logger.error(errorpost)
    else:
        errorpost = IpUserget(request) + ' - ' + str(param)
        omflow_logger.error(errorpost)
        root_logger.error(errorpost)
        
def critical(param,request=None):
    '''
    Set critical log message,if log level set debug,print debug post
    input: args
    return: log message
    author: Jia Liu
    ''' 
    #假如有Request參數,印出 IP、User、URL、view name 以及自訂 critical 訊息    
    msg = IpUserget(request) + ' - ' + str(param)
    omflow_logger.critical(msg)
    root_logger.critical(msg)
    log_level = logging.getLevelName(logging.getLogger('django').getEffectiveLevel())
    #如果等級等於DEBUG，印出POST訊息
    if  log_level == "DEBUG":
        if request != None:
            post = request.POST
            if post != {}:
                debugmsg = IpUserget(request) + ' - ' + '\n' + str(pformat(post))
                omflow_logger.debug(debugmsg)
                root_logger.debug(debugmsg)