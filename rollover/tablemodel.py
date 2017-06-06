'''
Created on May 14, 2017

@author: dongi
'''

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant

class TableModel(QAbstractTableModel): 
    TIME_FORMAT = "%Y_%m_%d %H:%M:%S"    
    INVALID_ROW = -1   
    INVALID_COL = -1
    INVALID_POS = [INVALID_ROW, INVALID_COL]
    HILIGHT_COLOR = Qt.cyan 
    def __init__(self, row_length, col_length, headerdata, parent=None): 
        super().__init__()
        self.row_length = row_length
        self.col_length = col_length
        self.headerdata = headerdata
        #self.datatable = [[None for _ in range(self.col_length)] for _ in range(self.row_length)] #datatable[i][j] is i-th row, j-th column

    def rowCount(self, parent= QModelIndex()):
        return self.row_length
        
    def columnCount(self, parent= QModelIndex()):
        return self.col_length       

    def flags(self, index):
        return Qt.ItemIsEnabled    
    
    def data(self, index, role= Qt.DisplayRole):
        raise Exception("data method is not implemented.")
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return QVariant(self.headerdata[section])
        else:
            return QAbstractTableModel.headerData(self, section, orientation, role)