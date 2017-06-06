'''
Created on May 23, 2017

@author: kevin
'''


class AdjustLogic(): 
    def __init__(self, adjusting_pair, contract_data):
        self.adjustPairList = adjusting_pair
        self.contractDataDict = contract_data
        
    def MakeAdjustment(self):
        raise Exception("MakeAdjustment is not implemented")
    
    def GetContractData(self, contract_name):
        """This method extract contract data from contractDataDict
        contractDataDict is different forms according to its own data structure therefore, 
        the subclass should implement its own logic of extraction.
        """
        raise Exception("GetContractData is not implemented")