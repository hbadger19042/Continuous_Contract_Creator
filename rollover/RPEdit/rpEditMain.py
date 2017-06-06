'''
Created on May 21, 2017

@author: dongi
'''

from PyQt5.QtWidgets import QWidget, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from .rpEditWindow import Ui_RpEditWindow
from .rpEditModel import RpEditModel

class RpEditMain(QWidget):
    rpChanged = pyqtSignal()
    def __init__(self, oldname, newname, parent = None):
        super().__init__(parent)
        self.oldName = oldname
        self.newName = newname        
        
        self.setWindowTitle("Base Point Editor")
        self.resize(1000, 800)
        
        self.rpUi = Ui_RpEditWindow(self.oldName, self.newName)
        self.rpUi.setupUi(self)
        self.editView = self.rpUi.editView
        
        self.createEditTable()
        
        self.editView.doubleClicked.connect(self.on_view_dclcked)



    def createEditTable(self):
        self.editHeaderView = QHeaderView(Qt.Horizontal)
        self.editHeaderView.resizeSections(QHeaderView.Interactive)
        styleSheet = """
            QHeaderView::section{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #616161, stop: 0.5 #505050,
                    stop: 0.6 #434343, stop:1 #656565);
                color:white;
                border:0.5px solid;                
            }
            """
        self.editHeaderView.setStyleSheet(styleSheet)
        self.editView.setHorizontalHeader(self.editHeaderView)
                
        header = ["time", "open", "high", "low", "close", "volume", 
                   "open", "high", "low", "close", "volume", "roll point"]
        row_length = 0
        col_length = 12
        self.editModel = RpEditModel(row_length, col_length, header)
        self.editView.setModel(self.editModel)
        
    def getBpIndex(self):
        return self.editModel.index(self.editModel.base_row, self.editModel.col_length -1)
    
    def getBpValue(self):                
        return self.editModel.displayData[self.editModel.base_row][0]
        
    def loadData(self, old_data, new_data, roll_point):
        self.editModel.loadData(old_data, new_data, roll_point)
    
    @staticmethod    
    def make_rp_editor_name(oldName, newName):
        return oldName + "_" + newName    
    
    @staticmethod
    def parse_rp_editor_name(editor_name):
        return editor_name.split("_")
    
    
    @pyqtSlot("QModelIndex")
    def on_view_dclcked(self, index):
        if not self.editModel.try_set_new_bp(index):
            warning = QMessageBox()
            warning.setText("The row cannot be set as base point because there is empty data.")
            warning.setIcon(QMessageBox.Warning)
            warning.exec()
        else:
            self.rpChanged.emit()