'''
Created on May 18, 2017

@author: dongi
'''




from ..adjustModel import AdjustModel

class PerpetualAdjustModel(AdjustModel):
    def __init__(self, row_length, col_length, headerdata, parent = None):
        super().__init__(row_length, col_length, headerdata, parent)
    
    def getContractData(self, name):
        return self.contractDataDict[name].getContractData()
                 
