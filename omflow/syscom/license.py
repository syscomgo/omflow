'''
syscom omflow license file
you can modify this file at will
@author: Pen Lin
'''
import urllib.request
import json

def getVersion():
    return '0.1.0.0'
    
def getVersionNum():
    return int('000100000000')
    
def getVersionType():
    return 'C'    
    
def getUsers(key_string):
    return 5

def getApps(key_string):
    return 5

def getDevices(key_string):
    return 0
  
def getRepository(content , url='https://raw.githubusercontent.com/syscomgo/omlib/master/'):
    if content == '':
        content = 'main.json'
       
    try:
        page = urllib.request.urlopen(url + content)
        data =  json.loads(page.read().decode('utf-8'))
        return data
    except:
        return None