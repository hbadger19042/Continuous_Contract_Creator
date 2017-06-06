'''
Created on May 18, 2017

@author: dongi
'''


from PyQt5.QtCore import Qt, QVariant, QModelIndex, pyqtSlot
from datetime import datetime
from itertools import combinations
from operator import itemgetter
from PyQt5.QtGui import QBrush
from .tablemodel import TableModel

import logging
adjustModelLogger = logging.getLogger("adjustModel.py")

class AdjustModel(TableModel):
    def __init__(self, row_length, col_length, headerdata, parent = None):
        super().__init__(row_length, col_length, headerdata, parent)
        self.dataRange_dict = {} #contract_name:(strate_date, end_date)
        #all possible pairs. The display data is chose from this list
        # [prev_contract_name, start_time, end_time, next_contract_name, start_time, end_time]
        self.allPairList = []
        #The date is in datatime format. It should be transformed into string when getting data. 
        #This data will be used in acutal adjustment
        # [first_contract_name, start_time, end_time, second_contrace_name, start_time, end_time, rollpoint]
        self.displayData = []
        #old one: {(old_name, new_name):rollpoint}
        #new one: {(old_name, new_name):[old_index, new_index, rollpoint]}
        self.rollPoint_dict = {} 
    
    def setRollPointCalculator(self, rollpointcalculator):
        self.rpCalculator = rollpointcalculator
        
    def setContractDataDict(self, data_dict):
        self.contractDataDict = data_dict
        
    def getContractData(self, name):
        raise Exception("Method, getContractData is not implemented.")
        
    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable
        
    def setData(self, index, value, role = Qt.DisplayRole):
        if not index.isValid(): return False
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if col != 0 and col !=3:
                self.displayData[row][col] = datetime.strptime(value, self.TIME_FORMAT)
            else:
                self.displayData[row][col] = value
            self.dataChanged.emit(index, index)
        return True
    
    def data(self, index, role= Qt.DisplayRole):  
        if not index.isValid(): return QVariant()
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            if col != 0 and col !=3:
                return self.displayData[row][col].strftime(self.TIME_FORMAT)
            else:
                return self.displayData[row][col]
        elif role == Qt.BackgroundRole:
            if col < 3:
                return QBrush(Qt.lightGray)
            elif col >=3 and col <6:
                return QBrush(Qt.white)
            else:
                return QBrush(Qt.lightGray)
              
    def removeRows(self, row, count, parent = QModelIndex()):
        if row >= self.row_length or row + count > self.row_length:
            return
        self.beginRemoveRows(QModelIndex(), row, row + count -1)
        for _ in range(count):
            self.displayData.pop(row)
        self.row_length = len(self.displayData)
        displayedSet = self.getDisplayContractNameSet()
        old_names = list(self.dataRange_dict.keys())
        for contract_name in old_names:
            if not contract_name in displayedSet:
                self.dataRange_dict.pop(contract_name)
                self.contractDataDict.pop(contract_name)
        self.endRemoveRows()
    
                    
    def addNewContract(self, contract_name, contract_range): 
        if contract_name in self.dataRange_dict.keys():
            adjustModelLogger.info("Existing contract name: %s" %contract_name)
            return                
        if not self.checkNewDataRangeIsNotDuplicated(contract_range): 
            adjustModelLogger.info("Duplicated contract range: %s" %contract_name)
            return   
        ##self._addToAllPairListSorted(contract_name, contract_range)
        self._addToRPDict(contract_name, contract_range)         
        self.dataRange_dict[contract_name] = contract_range #order is important
        ##self._reconstructDisplayDataByVolume(contract_name, contract_range)
        
        self._sync_display_data_with_other_containers()
    
    def _addToAllPairListSorted(self, contract_name, contract_range):
        """
        Add new contract into pair list by assuming new contract is not duplicate of 
        the existing one.
        """
        if len(self.dataRange_dict) <1: return
        for each_name, each_range in self.dataRange_dict.items():
            if (contract_range[0] < each_range[0] and each_range[0] <= contract_range[1] and 
                contract_range[1] <= each_range[1]):
                first_data = self.getContractData(contract_name)
                second_data = self.getContractData(each_name)        
                self.allPairList.append([contract_name, first_data[0][0], first_data[-1][0], 
                            each_name, second_data[0][0]], second_data[-1][0])
            elif (contract_range[0] >= each_range[0] and contract_range[0] < each_range[1] and
                    each_range[1] <= contract_range[1]):
                first_data = self.getContractData(each_name)
                second_data = self.getContractData(contract_name)        
                self.allPairList.append([contract_name, first_data[0][0], first_data[-1][0], 
                            each_name, second_data[0][0]], second_data[-1][0])
        self.allPairList.sort(key=itemgetter(1, 2, 4, 5))
    
    def _addToRPDict(self, contract_name, contract_range): 
        """
        Add new contract into Role point dictionary.
        """
        if len(self.dataRange_dict) <1: return
        for each_name, each_range in self.dataRange_dict.items():
            if (contract_range[0] < each_range[0] and each_range[0] <= contract_range[1] and 
                contract_range[1] <= each_range[1]):
                new_pair = (contract_name, each_name)
                rpList = []
                if not new_pair in self.rollPoint_dict:
                    first_data = self.getContractData(contract_name)
                    second_data = self.getContractData(each_name)
                    rpList = self.rpCalculator.Calculate(first_data, second_data)
                    self.rollPoint_dict[new_pair] = rpList[2] #for old way       
            elif (contract_range[0] >= each_range[0] and contract_range[0] < each_range[1] and
                    each_range[1] <= contract_range[1]):
                new_pair = (each_name, contract_name)
                rpList = []
                if not new_pair in self.rollPoint_dict:
                    first_data = self.getContractData(each_name)
                    second_data = self.getContractData(contract_name)
                    rpList = self.rpCalculator.Calculate(first_data, second_data)
                    self.rollPoint_dict[new_pair] = rpList[2] #for old way   
    
    def _reconstructDisplayDataByVolume(self, contract_name, contract_range):
        """
        Reconstruct display data from all pair list
        """
        pass 
        
   
    def _sync_display_data_with_other_containers(self):
        """
        After adding new data into dataRange_dict, update displayData
        according to the new data.
        """
        self.displayData = self._make_sorted_display_data()
        nlen = len(self.displayData)
        pre_row_size = self.row_length
        if nlen > pre_row_size:
            self.beginInsertRows(QModelIndex(), pre_row_size, nlen-1)   
            self.row_length = nlen 
            self.endInsertRows()        
            upperLeft = self.index(0,0)
            lowerRight = self.index(nlen-1, self.col_length-1)            
            self.dataChanged.emit(upperLeft, lowerRight)
        elif nlen == pre_row_size:
            upperLeft = self.index(0,0)
            lowerRight = self.index(nlen-1, self.col_length-1)
            self.dataChanged.emit(upperLeft, lowerRight)
        elif nlen < pre_row_size:
            self.beginRemoveRows(QModelIndex(), nlen, pre_row_size-1)
            upperLeft = self.index(0,0)
            lowerRight = self.index(nlen-1, self.col_length-1)   
            self.row_length = nlen 
            self.dataChanged.emit(upperLeft, lowerRight)
            self.endRemoveRows()        
            
    def _make_sorted_display_data(self):
        """
        Make new display data from an existing containers. 
        It is assumed that all the data is well-behaved for calculation.
        That is to say, no same data range and no included data range.
        """
        if len(self.dataRange_dict) <2:
            return []
        new_display_data =[]
        contracts = self.dataRange_dict.keys()
        for each_pair in combinations(contracts, 2):
            first = each_pair[0]
            second = each_pair[1]
            first_range = self.dataRange_dict[first]
            second_range = self.dataRange_dict[second]
            if (first_range[0] <= second_range[0] and second_range[0] <= first_range[1]
                and first_range[1] <= second_range[1]):
                new_pair = (first_range[0], second_range[0]) 
                if new_pair in self.rollPoint_dict.keys():
                    ddata = [first] + first_range + [second] + second_range +[self.rollPoint_dict[new_pair]]
                    new_display_data.append(ddata)
                else:
                    first_data = self.getContractData(first)
                    second_data = self.getContractData(second)
                    new_rp = self.rpCalculator.Calculate(first_data, second_data)
                    ddata = [first] + first_range + [second] + second_range +[new_rp[2]]
                    new_display_data.append(ddata)
                    self.rollPoint_dict[new_pair] = new_rp[2]
            elif (second_range[0] <= first_range[0] and first_range[0] <= second_range[1]
                and second_range[1] <= first_range[1]):
                new_pair = (second_range[0], first_range[0]) 
                if new_pair in self.rollPoint_dict.keys():
                    ddata = [second] + second_range + [first] + first_range +[self.rollPoint_dict[new_pair]]
                    new_display_data.append(ddata)
                else:
                    first_data = self.getContractData(first)
                    second_data = self.getContractData(second)
                    new_rp = self.rpCalculator.Calculate(second_data, first_data)
                    ddata = [second] + second_range + [first] + first_range +[new_rp[2]]
                    new_display_data.append(ddata)  
                    self.rollPoint_dict[new_pair] = new_rp[2]
        new_display_data = sorted(new_display_data, key=itemgetter(1, 2, 4, 5))
        return new_display_data
    
    def _removeDuplicateContractInDisplayData(self):pass
        
    
    def syncDataWithFileList(self, name_list):
        old_contract_names = list(self.dataRange_dict.keys())
        for each_name in old_contract_names:
            if not each_name in name_list:
                olen = len(self.displayData)
                for row in reversed(range(olen)):
                    if (self.displayData[row][0] == each_name or
                        self.displayData[row][3] == each_name): 
                        self.beginRemoveRows(QModelIndex(), row, row)
                        self.displayData.pop(row)
                        self.row_length = len(self.displayData)
                        displayedSet = self.getDisplayContractNameSet()
                        old_names = list(self.dataRange_dict.keys())
                        for contract_name in old_names:
                            if not contract_name in displayedSet and not contract_name in name_list:
                                self.dataRange_dict.pop(contract_name)
                                self.contractDataDict.pop(contract_name)
                        self.endRemoveRows()
        
    def getDisplayContractNameSet(self):
        displaySet = set()
        for each_item in self.displayData:
            displaySet.add(each_item[0])
            displaySet.add(each_item[3])
        return displaySet
    
    def getInternalContainerNameSet(self):
        internal_names = set()
        for each_name in self.dataRange_dict:
            internal_names.add(each_name)
        return internal_names
              
         
    def checkNewDataRangeIsNotDuplicated(self, new_data_range):
        """
        Check if new contract date range is not included in existing contract's date range
        and not the same as the existing one
        """
        for _, each_range in self.dataRange_dict.items():
            if (each_range[0] == new_data_range[0]
                    and new_data_range[1] == each_range[1]):
                return False
        return True
    
    @pyqtSlot()
    def setRollPoint(self):
        sender = self.sender()
        name_pair = (sender.oldName, sender.newName)
        value = sender.getBpValue()
        self.rollPoint_dict[name_pair] = value
        dataLen = len(self.displayData)      
        for row in range(dataLen):
            if (name_pair[0] == self.displayData[row][0] and 
                name_pair[1] == self.displayData[row][3]):
                self.displayData[row][-1] = value
                index = self.index(row, self.col_length-1)
                self.dataChanged.emit(index, index)
                return