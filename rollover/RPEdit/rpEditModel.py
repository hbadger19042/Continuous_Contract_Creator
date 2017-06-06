'''
Created on May 20, 2017

@author: dongi
'''

from rollover.tablemodel import TableModel
from PyQt5.QtCore import Qt, QVariant, QModelIndex
from PyQt5.QtGui import QBrush


class RpEditModel(TableModel):
    def __init__(self, row_length, col_length, headerdata, parent = None):
        self.displayData = []
        super().__init__(row_length, col_length, headerdata, parent)
        self.base_row = self.INVALID_ROW
        self.bp_string = "roll point"
    def removeRows(self, row, count, parent=QModelIndex()):
        if row > self.row_length or row + count > self.row_length:
            return
        self.beginRemoveRows(QModelIndex(), row, row + count -1)
        for _ in range(count):
            self.displayData.pop(row)
        self.row_length = len(self.displayData)
        
        self.base_row = self.INVALID_ROW
        for each_row in range(self.row_length):
            if self.displayData[each_row][self.col_length-1] == self.base_string:
                self.base_row = each_row
                break            
        self.endRemoveRows()
              
        
    def loadData(self, old_data, new_data, roll_point):
        """
        This method make display data and update view with data.
        The logic assumes that there is at least one time overlap between old_data and new_data. 
        """
        #clear the previous data first
        if self.row_length != 0:
            self.removeRows(0, self.row_length, QModelIndex()) 
            
        olen =len(old_data)
        nlen = len(new_data)
        new_empty=[None,None,None,None,None,None]
        old_empty=[None,None,None,None,None]
        new_searched_index = 0
        base_index = -1
        for old_index in range(olen):
            base_index += 1
            if old_data[old_index][0] == new_data[new_searched_index][0]:                
                ddata = old_data[old_index] + new_data[new_searched_index][1:]+[None]
                new_searched_index += 1
                if old_data[old_index][0] == roll_point:
                    ddata[11] = self.bp_string
                    self.base_row = base_index
                self.appendRow(ddata)
            elif old_data[old_index][0] < new_data[new_searched_index][0]:
                ddata = old_data[old_index] + new_empty
                self.appendRow(ddata)
            elif old_data[old_index][0] > new_data[new_searched_index][0]:
                new_range = range(new_searched_index, nlen)
                for new_index in new_range:
                    if old_data[old_index][0] > new_data[new_index][0]:
                        ddata = new_data[new_index] + [None]
                        ddata[1:1] = old_empty
                        self.appendRow(ddata)
                        new_searched_index += 1
                        base_index+=1
                    elif old_data[old_index][0] == new_data[new_index][0]:
                        ddata = old_data[old_index] + new_data[new_searched_index][1:]+[None]
                        if old_data[old_index][0] == roll_point:
                            ddata[11] = self.bp_string
                            self.base_row = base_index
                        self.appendRow(ddata)
                        new_searched_index += 1
                        break
                    else:
                        ddata = old_data[old_index] + new_empty
                        self.appendRow(ddata)
                        break                             
        for new_index in range(new_searched_index, nlen):
            ddata = new_data[new_index] + [None]
            ddata[1:1] = old_empty
            self.appendRow(ddata)      
        
        
    def flags(self, index):
        return Qt.ItemIsEnabled
        
    def setData(self, index, value, role = Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role==Qt.DisplayRole:
            self.displayData[row][col] = value    
    
    def data(self, index, role= Qt.DisplayRole):  
        if not index.isValid():
            return QVariant()
        row = index.row()
        col = index.column()  
        if col == 0 and role == Qt.DisplayRole:
            return self.displayData[row][col].strftime(self.TIME_FORMAT)   
        elif col > 0 and role == Qt.DisplayRole:
            return self.displayData[row][col]
        elif row ==self.base_row and role == Qt.BackgroundRole:
            return QBrush(self.HILIGHT_COLOR)
    
    def appendRow(self, data):
        self.beginInsertRows(QModelIndex(), self.row_length, self.row_length)   
        self.displayData.append(data)  
        self.row_length += 1           
        self.endInsertRows()  
        
    def try_set_new_bp(self, index):
        base_data = self.displayData[index.row()]
        if all(base_data[:-1]):
            if self.base_row == index.row():
                return True
            else:
                oldrow = self.base_row
                self.displayData[oldrow][-1] = None
                self.displayData[index.row()][-1] = self.bp_string
                self.base_row = index.row()
                upper = self.index(0,0)
                lower = self.index(self.row_length-1, self.col_length-1)
                self.dataChanged.emit(upper, lower)
            return True
        else:
            return False
            