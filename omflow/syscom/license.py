'''
syscom omflow license file
you can modify this file at will
@author: Pen Lin
'''
import urllib.request
import json
import hashlib
import os
from django.conf import settings
__base_path__ = os.path.join(settings.BASE_DIR, 'omflow/syscom/')
#__base_path__ = ''

def getVersion():
    version = ''
    try:
        fp = open(__base_path__ + 'version.bin', "r", encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.startswith('version='):
                version = line[8:]
            line = fp.readline()
        fp.close()
    except  IOError:
        version = '0.0.0.0' 
        
    return version.strip()
    
def getVersionNum():
    version = '000000000000'
    try:
        fp = open(__base_path__ + 'version.bin', "r", encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.startswith('version_num='):
                version = line[12:]
            line = fp.readline()
        fp.close()
    except  IOError:
        version = '000000000000' 
        
    return int(version)
'''
You can modify the license type at will, and the software will define your license based on this value.
C = Open Source GPL V3 License.
B/E/U = free license for personal, educational or evaluation use, or an Enterprise License, which is a for-fee license.
'''    
def getVersionType():
    version_type = 'C'
    try:
        fp = open(__base_path__ + 'license.bin', "r", encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.startswith('lic_type='):
                version_type = line[9:]
            line = fp.readline()
        fp.close()
    except  IOError:
        version_type = 'C' 
        
    return version_type.strip() 
    
def getUsers():
    user_count = '5'
    try:
        fp = open(__base_path__ + 'license.bin', "r", encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.startswith('user_count='):
                user_count = line[11:]
            line = fp.readline()
        fp.close()
    except  IOError:
        user_count = '5' 
        
    return int(user_count)

def getApps():
    app_count = '2'
    try:
        fp = open(__base_path__ + 'license.bin', "r", encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.startswith('app_count='):
                app_count = line[10:]
            line = fp.readline()
        fp.close()
    except  IOError:
        app_count = '2' 
        
    return int(app_count)

def getDevices():
    device_count = '0'
    try:
        fp = open(__base_path__ + 'license.bin', "r", encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.startswith('device_count='):
                device_count = line[13:]
            line = fp.readline()
        fp.close()
    except  IOError:
        device_count = '0' 
        
    return int(device_count)
    
def getCustomer():
    customer_name = 'no name'
    try:
        fp = open(__base_path__ + 'license.bin', "r", encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.startswith('customer_name='):
                customer_name = line[14:]
            line = fp.readline()
        fp.close()
    except  IOError:
        customer_name = 'no name' 
        
    return customer_name.strip() 
    
def getRepository(content , url='https://raw.githubusercontent.com/syscomgo/omlib/master/'):
    if content == '':
        content = 'main.json'
       
    try:
        page = urllib.request.urlopen(url + content)
        data =  json.loads(page.read().decode('utf-8'))
        return data
    except:
        return None
        
def license_file_checker():
    fileName1 = __base_path__ + 'license.bin'
    md5_checker = hashlib.md5()
    try:
        fd = open(fileName1, "r", encoding='UTF-8')
    except IOError:
        return 0
    x = fd.read()
    fd.close()
    md5_checker.update(x.encode("utf-8"))
    md_string = str(md5_checker.hexdigest())
    check_code = 0
    for word in list(md_string):
        if word in ['0','2','4','5','7']:
            check_code = check_code + (int(word)*1)
        elif word in ['1','3','6','8','9']:
            check_code = check_code + (int(word)*3)
        else:
            check_code = check_code + (ord(word)*5)
    
    return check_code
    