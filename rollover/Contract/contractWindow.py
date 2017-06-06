'''
Created on May 25, 2017

@author: dongi
'''


'''
Created on May 20, 2017

@author: dongi
'''

from PyQt5.QtWidgets import QTableView, QVBoxLayout, QHBoxLayout, QLabel,\
    QPushButton, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

translate = QtCore.QCoreApplication.translate

class Ui_ContractWindow():
    def __init__(self, cont_name, parent=None):
        self.cont_name = cont_name

    def setupUi(self, window):      
        
        vertical = QVBoxLayout(window)
        vertical.setContentsMargins(11, 10, 10, 5)
        

        
        contract_label = QLabel()
        contract_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        contract_label.setFont(font)
        contract_label.setText(self.cont_name)
        vertical.addWidget(contract_label)
 
        horizonal = QHBoxLayout(window)
        horizonal.setContentsMargins(0, 5, 0, 5)   
        
        self.applyChange_buttion = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.applyChange_buttion.setSizePolicy(sizePolicy)            
        self.applyChange_buttion.setObjectName("applyChange_buttion")
        self.applyChange_buttion.setText("Apply Change")
        horizonal.addWidget(self.applyChange_buttion)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        horizonal.addItem(spacerItem)
        
        vertical.addLayout(horizonal)     

        self.contractView = QTableView()
        self.contractView.setObjectName("contractView")
        vertical.addWidget(self.contractView)
        


        