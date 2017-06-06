'''
Created on May 21, 2017

@author: dongi
'''


from .tablemodel import TableModel
from PyQt5.QtCore import Qt, QVariant, QModelIndex


class ResultModel(TableModel):
    def __init__(self, row_size, col_size, header, parent=None):
        super().__init__(row_size, col_size, header, parent)
        self.header = header
        self.displayData = []
    
    def data(self, index, role = Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole and col == 0:
            return self.displayData[row][col].strftime(self.TIME_FORMAT)
        elif role==Qt.DisplayRole and col !=0:
            return self.displayData[row][col]
        else:
            return QVariant()
        
    def setData(self, index, value, role=Qt.DisplayRole):
        if not index.isValid():
            return False
        if role == Qt.DisplayRole:
            self.displayData[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)        
    
    def appendRow(self, data):
        self.beginInsertRows(QModelIndex(), self.row_length, self.row_length)
        self.displayData.append(data)
        self.row_length += 1
        self.endInsertRows()    
    
    def prependRow(self, data):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.displayData.insert(0, data)
        self.row_length += 1
        self.endInsertRows()    
        
        
    def removeRows(self, row, count, parent=QModelIndex()):
        if row > self.row_length or row + count > self.row_length or count == 0:
            return
        self.beginRemoveRows(QModelIndex(), row, row + count -1)
        for _ in range(count):
            self.displayData.pop(row)
        self.row_length = len(self.displayData)           
        self.endRemoveRows()        
        
    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable
        
    def clear(self):
        self.removeRows(0, self.row_length)