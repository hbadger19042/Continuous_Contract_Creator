'''
Created on May 17, 2017

@author: kevin
'''

from ..filelistModel import FilelistModel
from PyQt5.QtCore import Qt, QVariant, QModelIndex
from PyQt5.QtGui import QBrush


class ShiftFilelistModel(FilelistModel):
    def __init__(self, row_length, col_length, headerdata, parent = None):
        super().__init__(row_length, col_length, headerdata, parent)
        self.base_string = "base"
        self.base_row = self.INVALID_ROW     
        
    def data(self, index, role= Qt.DisplayRole):  
        if not index.isValid():
            return QVariant()   
        r = index.row()
        c = index.column()     
        if role == Qt.DisplayRole:
            return QVariant(self.filelistData[r][c])
        elif role == Qt.BackgroundRole and r == self.base_row:
            return QBrush(self.HILIGHT_COLOR)
        else:
            return QVariant()

    def removeRows(self, row, count, parent = QModelIndex()):
        if row > self.row_length or row + count > self.row_length:
            return
        self.beginRemoveRows(QModelIndex(), row, row + count -1)
        for _ in range(count):
            self.filelistData.pop(row)
        self.row_length = len(self.filelistData)
        
        self.base_row = self.INVALID_ROW
        for each_row in range(self.row_length):
            if self.filelistData[each_row][self.col_length-1] == self.base_string:
                self.base_row = each_row
                break
        self.endRemoveRows()
                
    def toggleBase(self, index):
        if not index.isValid():
            return
        r = index.row()
        if index.row() == self.base_row:
            self.base_row = self.INVALID_ROW
            self.filelistData[r][self.col_length-1] = None
        else:
            self.base_row = index.row()
            for each_row in range(self.row_length):
                if each_row == r:
                    self.filelistData[each_row][self.col_length-1] = self.base_string
                else:
                    self.filelistData[each_row][self.col_length-1] = None
        
        upper = self.index(0, 0)
        lower = self.index(self.row_length-1, self.col_length -1)
        self.dataChanged.emit(upper, lower) 

    
    def getBaseContract(self):
        if self.base_row == self.INVALID_ROW:
            return None
        else:
            return self.filelistData[self.base_row][0]
        