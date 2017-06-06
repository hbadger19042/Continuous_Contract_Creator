'''
Created on May 23, 2017

@author: kevin
'''

from ..adjustLogic import AdjustLogic
from .perpetualMain import AdjustWeightType
from _operator import itemgetter

class PerpetualAdjustLogic(AdjustLogic):
    def __init__(self, adjust_pair_list, contract_data_dict, matching_price_index):
        super().__init__(adjust_pair_list, contract_data_dict)
        self.matchingPriceIndex = matching_price_index
    
    def GetContractData(self, contract_name):
        return self.contractDataDict[contract_name].getContractData()
        
    def MakeAdjustment(self, result_model, roll_period, 
                       weight_type, matching_price_index = 1):
        if weight_type == AdjustWeightType.TIME:
            first_data = self.GetContractData(self.adjustPairList[-1][3])
            first_index = len(first_data) -1
            second_index = 0        
            pair_len = len(self.adjustPairList)
            for pairIndex in reversed(range(pair_len)):
                second_index = first_index
                if pairIndex > 0:
                    next_rp = self.adjustPairList[pairIndex-1][-1]        
                    first_data = self.GetContractData(self.adjustPairList[pairIndex][0])        
                    for first_row in range(len(first_data)):
                        if first_data[first_row][0] == next_rp:
                            first_index = first_row+1
                            break
                else:
                    first_index = 0
                self.TimeWeightAdjustmentForSinglePair(self.adjustPairList[pairIndex], first_index, second_index, 
                                result_model, roll_period, matching_price_index)
#             for pairIndex, each_pair in enumerate(self.adjustPairList):
#                 first_index = second_index + 1
#                 second_data = self.GetContractData(each_pair[3])   
#                 second_data_length = len(second_data)
#                 if pairIndex < pair_len -1:
#                     second_rp = self.adjustPairList[pairIndex+1][-1]                 
#                     for second_row in range(second_data_length):
#                         if second_data[second_row][0] == second_rp:
#                             second_index = second_row
#                             break
#                 else:
#                     second_index = second_data_length -1
#                 self.TimeWeightAdjustmentForSinglePair(each_pair, first_index, second_index, 
#                                 result_model, roll_period, matching_price_index)
        
    
    def TimeWeightAdjustmentForSinglePair(self, adjustpair, start_index, end_index, 
                                   result_model, roll_period, matching_price_index):
        roll_point = adjustpair[-1]
        first_name = adjustpair[0]
        second_name = adjustpair[3]
        first_data = self.GetContractData(first_name)
        second_data = self.GetContractData(second_name)
        #index_pair = [first_data_index, second_data_index, roll_point_time, time_to_rp]
        index_pair = self.FindAdjustIndexPairAscending(first_data, second_data, roll_period, roll_point, matching_price_index)
        if not index_pair: return
        total_length = index_pair[len(index_pair)-1][-1]
        if total_length == 0: return
        last_adjust_second_index = index_pair[0][1]
        for second_row in reversed(range(last_adjust_second_index+1, end_index)):
            ddata = second_data[second_row] + [0] + [second_name]
            result_model.prependRow(ddata)

        for index, each_pair in enumerate(index_pair):
            first_item = first_data[each_pair[0]]
            second_item = second_data[each_pair[1]]
            ddata = [each_pair[2]]
            first_weight = each_pair[-1]/total_length
            for i in range(1, 6):
                ddata.append(first_item[i] * first_weight + second_item[i] * (1-first_weight))
            ddata.append(first_weight)
            if index == 0:
                ddata.append(second_name)
            elif index == len(index_pair)-1:
                ddata.append(first_name)
            else:
                ddata.append(first_name + "-" + second_name)
            result_model.prependRow(ddata)
        first_range = range(start_index, index_pair[-1][0])
        for first_row in reversed(first_range):
            ddata = first_data[first_row] + [0] + [first_name]
            result_model.prependRow(ddata)              

    def FindAdjustIndexPairAscending(self, first_data, second_data, roll_period, 
                            roll_point, matching_price_index):
        """
        Find data for adjustment. Return index pair of two data required adjustment.
        first_data is older one and second_data is newer.
        Index pair is in ascending order
        """
        index_pair = []
        first_rp_index = None
        second_rp_index = None
        for first_row in range(len(first_data)):
            if first_data[first_row][0] == roll_point and first_data[first_row][matching_price_index]:
                first_rp_index = first_row
                break
        for second_row in range(len(second_data)):
            if second_data[second_row][0] == roll_point and second_data[second_row][matching_price_index]:
                second_rp_index = second_row
                break
        if first_rp_index and second_rp_index:
            second_length = 0 #time length for the newer contract's weight
            index_pair.append([first_rp_index, second_rp_index, roll_point, second_length])
        if first_rp_index <= 0:
            return index_pair
        for first_row in range(first_rp_index-1, -1, -1):
            first_point = first_data[first_row][0]
            for second_row in range(second_rp_index-1, -1, -1):
                if first_point == second_data[second_row][0]:
                    second_rp_index = second_row
                    if (first_data[first_row][matching_price_index] 
                        and second_data[second_row][matching_price_index]):
                        time_to_rp = roll_point - first_point
                        index_pair.append([first_row, second_row, first_point, time_to_rp.total_seconds()])
                        if len(index_pair) >= roll_period:
                            return index_pair
                        else:
                            break
                elif first_point > second_data[second_row][0]:
                    second_rp_index = second_row + 1
                    break
        return index_pair
                        
                    
                
        
    
