'''
Created on May 20, 2017

@author: dongi
'''

from PyQt5.QtWidgets import QTableView, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

translate = QtCore.QCoreApplication.translate

class Ui_RpEditWindow():
    def __init__(self, old_name, new_name, parent=None):
        self.oldName = old_name
        self.newName = new_name

    def setupUi(self, window):      
        
        vertical = QVBoxLayout(window)
        vertical.setContentsMargins(11, 10, 10, 5)
        
        horizonal = QHBoxLayout(window)
        horizonal.setContentsMargins(25, 10, 10, 5)
        
        oldlabel = QLabel()
        newlabel = QLabel()
        oldlabel.setAlignment(Qt.AlignCenter)
        newlabel.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        oldlabel.setFont(font)
        newlabel.setFont(font)
        oldlabel.setText(self.oldName)
        newlabel.setText(self.newName)
        horizonal.addWidget(oldlabel)
        horizonal.addWidget(newlabel)
        
        vertical.addLayout(horizonal)     

        self.editView = QTableView()
        self.editView.setObjectName("editView")
        vertical.addWidget(self.editView)
        


        