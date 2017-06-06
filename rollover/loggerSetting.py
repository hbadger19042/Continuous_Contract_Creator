'''
Created on Jun 3, 2017

@author: dongi
'''

import logging

class SetLogger():
    def __init__(self):
        self.SetRootLogger()
        
    def SetRootLogger(self):
        rootlogger = logging.getLogger("")
        rootlogger.setLevel(logging.NOTSET)
        
        flhandler = logging.FileHandler("rollover.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        flhandler.setFormatter(formatter)        
        
        rootlogger.addHandler(flhandler)