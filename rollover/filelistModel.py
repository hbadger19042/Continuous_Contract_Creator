'''
Created on May 17, 2017

@author: kevin
'''

from .tablemodel import TableModel
from PyQt5.QtCore import Qt, QVariant, QModelIndex
from operator import itemgetter


class FilelistModel(TableModel):
    def __init__(self, row_length, col_length, headerdata, parent = None):
        super().__init__(row_length, col_length, headerdata, parent)
        self.filelistData = []
    
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
    def setData(self, index, value, role = Qt.DisplayRole):
        if not index.isValid():
            return False
        r = index.row()
        c = index.column()
        if role == Qt.DisplayRole:
            self.filelistData[r][c] = value                
            self.dataChanged.emit(index, index)
            return True           
        return False
    

    def data(self, index, role= Qt.DisplayRole):  
        if not index.isValid():
            return QVariant()   
        r = index.row()
        c = index.column()   
        if role == Qt.DisplayRole and (c == 1 or c==2):
            return self.filelistData[r][c].strftime(self.TIME_FORMAT)
        elif role == Qt.DisplayRole:
            return self.filelistData[r][c]
        else:
            return QVariant()    
      
    def removeRows(self, row, count, parent = QModelIndex()):
        if row > self.row_length or row + count > self.row_length:
            return
        self.beginRemoveRows(QModelIndex(), row, row + count -1)
        for _ in range(count):
            self.filelistData.pop(row)
        self.row_length = len(self.filelistData)         
        self.endRemoveRows()
      
        
    def appendRow(self, data):
        self.beginInsertRows(QModelIndex(), self.row_length, self.row_length)   
        data.append(None)  
        self.filelistData.append(data)
        self.row_length += 1
        self.endInsertRows()     
        self.filelistData.sort(key=itemgetter(1, 2))
        leftIndex = self.index(0,0)
        rightIndex = self.index(self.row_length-1, self.col_length-1)
        self.dataChanged.emit(leftIndex, rightIndex)
    

    def getContractList(self):
        contList = []
        for each_data in self.filelistData:
            contList.append(each_data[0])
        return contList
    
        