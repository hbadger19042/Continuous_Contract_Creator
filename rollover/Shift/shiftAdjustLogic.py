'''
Created on May 23, 2017

@author: kevin
'''

from datetime import timedelta
from ..adjustLogic import AdjustLogic

class ShiftAdjustLogic(AdjustLogic):
    def __init__(self, adjust_pair_list, contract_data_dict, matching_price_index):
        super().__init__(adjust_pair_list, contract_data_dict)
        self.matchingPriceIndex = matching_price_index
    
    def GetContractData(self, contract_name):
        return self.contractDataDict[contract_name].getContractData()
        
    def MakeAdjustment(self, base_contract, model):
        alen = len(self.adjustPairList)
        start_row = -1
        for row in range(alen):
            if (self.adjustPairList[row][0] == base_contract):
                start_row = row
                break
        if start_row == -1: #Backward mode
            end_date = self.GetContractData(base_contract)[-1][0]
            self._backwardAdjust(self.adjustPairList, end_date, 0, model)
        elif start_row ==0: #forward mode
            start_date = self.GetContractData(base_contract)[0][0]
            self._forwardAdjust(self.adjustPairList, start_date, 0, model)
        else: #mixed mode
            start_bp = self.adjustPairList[start_row][-1]            
            base_data = self.GetContractData(base_contract)
            base_lower_value = None
            for rRow in reversed(range(len(base_data))):
                if base_data[rRow][0] == start_bp:
                    base_lower_value = base_data[rRow][self.matchingPriceIndex]
                    break
            next_name = self.adjustPairList[start_row][3]
            next_data = self.GetContractData(next_name)
            next_upper_value = None
            next_upper_index = None
            for nRow in range(len(next_data)):
                if next_data[nRow][0] >= start_bp:
                    next_upper_value = next_data[nRow][self.matchingPriceIndex]
                    next_upper_index = nRow
                    break
            forward_adjustment = base_lower_value - next_upper_value
            if start_row == alen-1:
                for i in range(next_upper_index, len(next_data)):                
                    adjusted_data = [next_data[i][0]]
                    adjusted_data += [x + forward_adjustment for x in next_data[i][1:-1]]
                    adjusted_data += [next_data[i][-1]]
                    adjusted_data += [forward_adjustment, next_name]
                    model.appendRow(adjusted_data)
            else:
                forward_adjust_list = self.adjustPairList[start_row+1:]
                self._forwardAdjust(forward_adjust_list, start_bp, forward_adjustment, model)
        
            backward_adjust_list = self.adjustPairList[:start_row]
            backward_start_bp = start_bp - timedelta(microseconds = 1)
            self._backwardAdjust(backward_adjust_list, backward_start_bp, 0, model)

        
    
    def _backwardAdjust(self, adjustPairList, end_date, adjustment, model):       
            lower_bp = None   
            cur_name = None  
            cur_data = None
            cur_lower_bp_index = 0
            cur_upper_bp_index = 0
            
            alen = len(adjustPairList) 
            next_name = adjustPairList[alen-1][3]
            next_data = self.GetContractData(next_name)
            next_lower_bp_index = len(next_data)-1 
            upper_bp = end_date
            
            for aRow in reversed(range(alen)):
                lower_bp = upper_bp
                cur_name = next_name
                cur_data = next_data
                cur_lower_bp_index = next_lower_bp_index            
                next_name = adjustPairList[aRow][0]
                next_data=self.GetContractData(next_name)
                upper_bp = adjustPairList[aRow][-1]                
                for i in range(cur_lower_bp_index, -1, -1):
                    if lower_bp >= cur_data[i][0] and cur_data[i][0] > upper_bp:                
                        adjusted_data = [cur_data[i][0]]
                        adjusted_data += [x + adjustment for x in cur_data[i][1:-1]]
                        adjusted_data += [cur_data[i][-1]]
                        adjusted_data += [adjustment, cur_name]
                        model.prependRow(adjusted_data)
                    elif upper_bp >= cur_data[i][0]:
                        cur_upper_bp_index = i
                        break                         
                for nRow in reversed(range(len(next_data))):
                    if next_data[nRow][0] == upper_bp:
                        next_lower_bp_index = nRow
                adjustment += (cur_data[cur_upper_bp_index][self.matchingPriceIndex] 
                               - next_data[next_lower_bp_index][self.matchingPriceIndex])
                if aRow == 0:
                    for i in range(next_lower_bp_index, -1, -1):                
                        adjusted_data = [next_data[i][0]]
                        adjusted_data += [x + adjustment for x in next_data[i][1:-1]]
                        adjusted_data += [next_data[i][-1]]
                        adjusted_data += [adjustment, next_name]
                        model.prependRow(adjusted_data)
                        
    
    def _forwardAdjust(self, adjustPairList, start_date, adjustment, model):       
        alen = len(adjustPairList) 
        upper_bp = None   
        cur_name = None  
        cur_data = None
        cur_lower_bp_index = None
        cur_upper_bp_index = None
        
        next_name = adjustPairList[0][0]
        next_data = self.GetContractData(next_name)
        next_upper_bp_index = 0
        lower_bp = start_date
        
        for aRow in range(alen):
            upper_bp = lower_bp
            cur_name = next_name
            cur_data = next_data
            cur_upper_bp_index = next_upper_bp_index
            
            next_name = adjustPairList[aRow][3]
            next_data=self.GetContractData(next_name)
            lower_bp = adjustPairList[aRow][-1]                
            for i in range(cur_upper_bp_index, len(cur_data)):
                if upper_bp <= cur_data[i][0] and cur_data[i][0] < lower_bp:                
                    adjusted_data = [cur_data[i][0]]
                    adjusted_data += [x + adjustment for x in cur_data[i][1:-1]]
                    adjusted_data += [cur_data[i][-1]]
                    adjusted_data += [adjustment, cur_name]
                    model.appendRow(adjusted_data)
                elif lower_bp <= cur_data[i][0]:
                    cur_lower_bp_index = i
                    break                
            for nRow in range(len(next_data)):
                if next_data[nRow][0] == lower_bp:
                    next_upper_bp_index = nRow
            adjustment += (cur_data[cur_lower_bp_index][self.matchingPriceIndex] 
                           - next_data[next_upper_bp_index][self.matchingPriceIndex])
            if aRow == alen-1:
                for i in range(next_upper_bp_index, len(next_data)):                
                    adjusted_data = [next_data[i][0]]
                    adjusted_data += [x + adjustment for x in next_data[i][1:-1]]
                    adjusted_data += [next_data[i][-1]]
                    adjusted_data += [adjustment, next_name]
                    model.appendRow(adjusted_data)