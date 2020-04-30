'''
syscom omflow omuser logging setting
@author: Jia Liu
'''
import logging
'''
setting log name to different function
only record omuser fuction log
set whitelist for only function to use
author:Jia Liu
'''

'''
class Whitelist(logging.Filter):
    def __init__(self, *whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)

for handler in logging.root.handlers:
    handler.addFilter(Whitelist('UserRegister','UserLogin','UserUpdate','UserAdd'))
'''
    
def setup_logger(name, log_file, level=logging.INFO):
    formatter=logging.Formatter('[%(asctime)s] - [%(name)s] - %(levelname)s - %(message)s',
                                "%Y-%m-%d %H:%M:%S")
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
foo_logger = setup_logger('UserLogin', 'logs\omuser.log')
goo_logger = setup_logger('UserRegister','logs\omuser.log')
hoo_logger = setup_logger('UserUpdate','logs\omuser.log')
joo_logger = setup_logger('UserAdd','logs\omuser.log')
