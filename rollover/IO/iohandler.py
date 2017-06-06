'''
Created on May 21, 2017

@author: dongi
'''

class IOHandler():
    def __init__(self, abs_path):
        self.absPath = abs_path
        
    def ReadSingleFile(self):
        raise Exception("ReadSingleFile method is not implemented")
    
    def SaveFile(self):
        raise Exception("ReadSingleFile method is not implemented")