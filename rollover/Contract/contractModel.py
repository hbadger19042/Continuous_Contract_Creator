'''
Created on May 20, 2017

@author: dongi
'''

from rollover.tablemodel import TableModel
from PyQt5.QtCore import Qt, QVariant, QModelIndex
from PyQt5.QtGui import QBrush
from datetime import datetime

class ContractModel(TableModel):
    def __init__(self, row_length, col_length, headerdata, parent = None):
        self.contract_data = []
        super().__init__(row_length, col_length, headerdata, parent)

    def loadData(self, contract_data):
        self.contract_data = contract_data
        self.row_length = len(self.contract_data)    
        self.beginInsertRows(QModelIndex(), 0, self.row_length-1)
        self.endInsertRows()     

    def removeRows(self, row, count, parent = QModelIndex()):
        if row > self.row_length or row + count > self.row_length:
            return
        self.beginRemoveRows(QModelIndex(), row, row + count -1)
        for _ in range(count):
            self.contract_data.pop(row)
        self.row_length = len(self.contract_data)        
        self.endRemoveRows()
        
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
    def setData(self, index, value, role = Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if col == 0 and role==Qt.DisplayRole:
            self.cont_data[row][col] = value.strptime(self.TIME_FORMAT)   
        elif col>0 and role == Qt.DisplayRole:
            self.cont_data[row][col] = value
    
    def data(self, index, role= Qt.DisplayRole):  
        if not index.isValid():
            return QVariant()
        row = index.row()
        col = index.column()  
        if col == 0 and role == Qt.DisplayRole:
            return self.contract_data[row][col].strftime(self.TIME_FORMAT)   
        elif col > 0 and role == Qt.DisplayRole:
            return self.contract_data[row][col]
    

            