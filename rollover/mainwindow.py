# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'self.MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QSizePolicy, QMenu, QMenuBar, QWidget, QToolBar, 
            QGridLayout, QStatusBar, QAction, QPushButton, QLayout, QVBoxLayout,
            QStackedWidget, QSpacerItem, QButtonGroup)
from .Shift.shiftWindow import Ui_ShiftWindow
from .Perpetual.perpetualWindow import Ui_PerpetualWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        
        self.setupMainWindow()
        self.setupMenuBar()
        self.setupAjdustmentOptionBar()
        self.setupMainStack()
        
        self.shiftUi = Ui_ShiftWindow(self.shift_page)
        self.shiftUi.setupUi()
        
        self.perpetualUi = Ui_PerpetualWindow(self.perpetual_page)
        self.perpetualUi.setupUi()
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)  

        
    def setupMainWindow(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1500, 800)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.MainWindow.setMinimumSize(QtCore.QSize(1500, 800))
        
        self.centralWidget = QWidget(self.MainWindow)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QtCore.QSize(1500, 800))
        self.centralWidget.setSizeIncrement(QtCore.QSize(5, 5))
        self.centralWidget.setBaseSize(QtCore.QSize(5, 5))
        self.centralWidget.setObjectName("centralWidget")    
        self.MainWindow.setCentralWidget(self.centralWidget)
        
        
        self.statusBar = QStatusBar(self.MainWindow)
        self.statusBar.setObjectName("statusBar")
        self.MainWindow.setStatusBar(self.statusBar)
        
        self.toolBar = QToolBar(self.MainWindow)
        self.toolBar.setObjectName("toolBar")
        self.MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.outer_gridLayout = QGridLayout(self.centralWidget)
        self.outer_gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.outer_gridLayout.setContentsMargins(11, 6, 11, 0)
        self.outer_gridLayout.setSpacing(6)
        self.outer_gridLayout.setObjectName("outer_gridLayout")
    
    def setupMenuBar(self):
        self.menuBar = QMenuBar(self.MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 942, 21))
        self.menuBar.setObjectName("menuBar")
        
        self.MainWindow.setMenuBar(self.menuBar)
                
        self.menuLog = QMenu(self.menuBar)
        self.menuLog.setObjectName("menuLog")
        self.actionLog = QAction(self.MainWindow)
        self.actionLog.setObjectName("actionLog")
        self.menuLog.addAction(self.actionLog)
        self.menuBar.addAction(self.menuLog.menuAction())  
        
        _translate = QtCore.QCoreApplication.translate
        self.menuLog.setTitle(_translate("MainWindow", "Log"))
        self.actionLog.setText(_translate("MainWindow", "Show Log"))
        
        self.menuAbout = QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        self.actionHelp = QAction(self.MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuAbout.addAction(self.actionHelp)
        self.menuBar.addAction(self.menuAbout.menuAction())    

        _translate = QtCore.QCoreApplication.translate
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))

    def setupAjdustmentOptionBar(self):
        self.verticalWidget = QWidget(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setMinimumSize(QtCore.QSize(120, 0))
        self.verticalWidget.setMaximumSize(QtCore.QSize(120, 16777215))
        self.verticalWidget.setStyleSheet("background-color:darkgray")
        self.verticalWidget.setObjectName("verticalWidget")
        
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setContentsMargins(5, 65, 5, 11)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.shift_button = QPushButton(self.verticalWidget)
        self.shift_button.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.shift_button.setFont(font)
        self.shift_button.setObjectName("shift_button")
        self.shift_button.setCheckable(True)
          
           
        
        self.perpetual_button = QPushButton(self.verticalWidget)
        self.perpetual_button.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.perpetual_button.setFont(font)
        self.perpetual_button.setCheckable(True)
        self.perpetual_button.setObjectName("perpetual_button")
        
        self.verticalLayout.addWidget(self.shift_button)   
        self.verticalLayout.addWidget(self.perpetual_button)
        
        self.buttonGroup = QButtonGroup(self.verticalWidget)
        self.buttonGroup.addButton(self.shift_button)
        self.buttonGroup.addButton(self.perpetual_button)
        self.buttonGroup.setExclusive(True)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.outer_gridLayout.addWidget(self.verticalWidget, 0, 0, 1, 1)    
        
    def setupMainStack(self):
        
        self.shift_main_stacked = QStackedWidget(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.shift_main_stacked.sizePolicy().hasHeightForWidth())
        self.shift_main_stacked.setSizePolicy(sizePolicy)
        self.shift_main_stacked.setObjectName("shift_main_stacked")        
        
        self.shift_page = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.shift_page.sizePolicy().hasHeightForWidth())
        self.shift_page.setSizePolicy(sizePolicy)
        self.shift_page.setObjectName("shift_page")        
        self.shift_main_stacked.addWidget(self.shift_page)
        
        self.perpetual_page = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.perpetual_page.sizePolicy().hasHeightForWidth())
        self.perpetual_page.setSizePolicy(sizePolicy)
        self.perpetual_page.setObjectName("perpetual_page")
        self.shift_main_stacked.addWidget(self.perpetual_page)
        
        self.outer_gridLayout.addWidget(self.shift_main_stacked, 0, 1, 1, 1)
    
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "Continuous Contract Maker"))
        self.shift_button.setText(_translate("MainWindow", "Forward\n"
"Backward"))
        self.perpetual_button.setText(_translate("MainWindow", "Perputual\n"
" Series"))
        
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))


