'''
Created on May 25, 2017

@author: dongi
'''

from PyQt5.QtWidgets import QWidget, QHeaderView, QMenu, QProgressDialog, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex
from .contractWindow import Ui_ContractWindow
from .contractModel import ContractModel

class ContractMain(QWidget):
    def __init__(self, contract_name, contract_data, parent = None):
        super().__init__(parent)
        self.contract_name = contract_name      
        
        self.setWindowTitle("Contract Data")
        self.resize(670, 800)
        
        self.cont_Ui = Ui_ContractWindow(self.contract_name)
        self.cont_Ui.setupUi(self)
        
        self.contractView = self.cont_Ui.contractView   
             
        self.createContractTable()    
        self.load_data(contract_data)    
        
        self.contractView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contractView.customContextMenuRequested.connect(self._contractView_context) 
        
        self.cont_Ui.applyChange_buttion.clicked.connect(self.apply_change)

    

    def createContractTable(self):
        self.contractHeaderView = QHeaderView(Qt.Horizontal)
        self.contractHeaderView.resizeSections(QHeaderView.Interactive)
        styleSheet = """
            QHeaderView::section{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #616161, stop: 0.5 #505050,
                    stop: 0.6 #434343, stop:1 #656565);
                color:white;
                border:0.5px solid;                
            }
            """
        self.contractHeaderView.setStyleSheet(styleSheet)
        self.contractView.setHorizontalHeader(self.contractHeaderView)
                
        header = ["time", "open", "high", "low", "close", "volume"]
        row_length = 0
        col_length = 6
        self.contractModel = ContractModel(row_length, col_length, header)
        self.contractView.setModel(self.contractModel)
        
    
    @pyqtSlot("QModelIndex")
    def on_view_dclcked(self, index):pass
    
    
    @pyqtSlot("QPoint")
    def _contractView_context(self, pos):
        context_menu = QMenu()
        remove_row_action = context_menu.addAction("Remove selected rows")
        new_action = context_menu.exec_(self.contractView.mapToGlobal(pos))
        if new_action == remove_row_action:
            smodel = self.contractView.selectionModel()
            index_list = smodel.selectedIndexes()
            rowSet = set()
            for index in index_list:
                rowSet.add(index.row())        
            for row in sorted(rowSet, reverse=True):
                self.contractModel.removeRows(row, 1, QModelIndex())
                   

    
    def load_data(self, contract_data):
        self.contractModel.loadData(contract_data)
        
    def getContractData(self):
        return self.contractModel.contract_data
    
    @pyqtSlot()
    def apply_change(self):
        progressDialog = QProgressDialog("Applying Change....", "", 0, 
                            0, self.contractView)   
        progressDialog.setWindowModality(Qt.ApplicationModal) 
        progressDialog.setCancelButton(None)
        progressDialog.setMinimumDuration(0)    
        progressDialog.forceShow()
        QApplication.processEvents()
        from ..Shift.shiftmain import ShiftMain
        ShiftMain.UpdateRollEditor(self.contract_name)
        progressDialog.hide()
        progressDialog = None
        
