'''
Created on May 20, 2017

@author: dongi
'''

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QSizePolicy, QLabel, QComboBox, QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

translate = QtCore.QCoreApplication.translate

class Ui_PerpetualWindow():
    def __init__(self, perpetual_page):
        self.perpetual_page = perpetual_page
    
    def setupUi(self):
        self.setupTitle()
        self.setupFileListUi()
        self.setupFileListView()
#        self.setupAdjustTab()
        self.setupAdjustmentView()
        self.setupResult()
        
    
    def setupTitle(self):
        self.outer_vertical_layout = QtWidgets.QVBoxLayout(self.perpetual_page)
        self.outer_vertical_layout.setContentsMargins(11, 0, 11, 0)
        self.outer_vertical_layout.setSpacing(6)
        self.outer_vertical_layout.setObjectName("outer_vertical_layout")
        
        self.perpetual_title_label = QtWidgets.QLabel(self.perpetual_page)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.perpetual_title_label.sizePolicy().hasHeightForWidth())
        self.perpetual_title_label.setSizePolicy(sizePolicy)
        self.perpetual_title_label.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.perpetual_title_label.setFont(font)
        self.perpetual_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.perpetual_title_label.setObjectName("perpetual_title_label")
        self.outer_vertical_layout.addWidget(self.perpetual_title_label)
        self.perpetual_title_label.setText(translate("MainWindow", "Perpetual Series Maker"))
        
        self.outer_horizontalSplitter = QSplitter()
        self.outer_horizontalSplitter.setContentsMargins(11, 6, 11, 0)
        #total_size = self.outer_horizontalSplitter.size()
        self.outer_horizontalSplitter.setSizes([320, 320])
        #self.outer_horizontalSplitter.setSpacing(6)
        self.outer_horizontalSplitter.setObjectName("outer_horizontalSplitter")
        #self.outer_horizontalSplitter.setOrientation(Qt.Vertical)
        self.outer_vertical_layout.addWidget(self.outer_horizontalSplitter)

    def setupFileListUi(self):
#         self.file_window = QtWidgets.QWidget()
#         self.outer_horizontalSplitter.addWidget(self.file_window)
        
        self.file_verticalSplitter = QSplitter()
        self.file_verticalSplitter.setContentsMargins(11, 6, 11, 0)
        #self.file_verticalSplitter.setSpacing(6)
        self.file_verticalSplitter.setObjectName("file_verticalSplitter")
        self.file_verticalSplitter.setOrientation(Qt.Vertical)
        self.outer_horizontalSplitter.addWidget(self.file_verticalSplitter)
        #self.outer_horizontalSplitter.addWidget(self.file_verticalSplitter)
        #self.outer_horizontalSplitter.addLayout(self.file_verticalLayout)
 
        self.filelist_widget = QtWidgets.QWidget()
        self.filelist_widget.setMinimumWidth(550)
        policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.filelist_widget.setSizePolicy(policy)
        self.file_verticalSplitter.addWidget(self.filelist_widget)
        
        self.filelist_verticalLayout = QtWidgets.QVBoxLayout(self.filelist_widget)
        self.filelist_verticalLayout.setContentsMargins(0, 11, 0, 0)
        self.filelist_verticalLayout.setSpacing(6)
        self.filelist_verticalLayout.setObjectName("filelist_verticalLayout")
    
        
        self.filelistButton_horizontalLayout = QtWidgets.QHBoxLayout(self.filelist_widget)
        self.filelistButton_horizontalLayout.setContentsMargins(0, 11, 0, 6)
        self.filelistButton_horizontalLayout.setSpacing(6)
        self.filelistButton_horizontalLayout.setObjectName("filelistButton_horizontalLayout")
        self.filelist_verticalLayout.addLayout(self.filelistButton_horizontalLayout)
                
         
        self.add_files_button = QtWidgets.QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.add_files_button.sizePolicy().hasHeightForWidth())
        self.add_files_button.setSizePolicy(sizePolicy)
        self.add_files_button.setObjectName("add_files_button")
        self.add_files_button.setText(translate("MainWindow", "Add Files"))          
        self.filelistButton_horizontalLayout.addWidget(self.add_files_button)        
 
         
        self.clear_list_button = QtWidgets.QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.clear_list_button.sizePolicy().hasHeightForWidth())
        self.clear_list_button.setSizePolicy(sizePolicy)
        self.clear_list_button.setObjectName("clear_list_button")
        self.clear_list_button.setText(translate("MainWindow", "Clear List"))
        self.filelistButton_horizontalLayout.addWidget(self.clear_list_button)        
        
#         spacerItem = QSpacerItem(20, 40, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
#         self.filelistButton_horizontalLayout.addItem(spacerItem)

    def setupFileListView(self):        
        tableviewTitle = QLabel()
        tableviewTitle.setText("Contract List")
        font = QFont()
        font.setPointSize(10)
        #font.setBold(True)
        tableviewTitle.setFont(font)
        tableviewTitle.setAlignment(Qt.AlignLeft)
        self.filelist_verticalLayout.addWidget(tableviewTitle)
         
        self.filelistView = QtWidgets.QTableView()
        self.filelistView.setObjectName("filelistView")
        self.filelist_verticalLayout.addWidget(self.filelistView)    

        
    def setupAdjustmentView(self):   
        self.adjustWidget = QtWidgets.QWidget()
        self.file_verticalSplitter.addWidget(self.adjustWidget)
        
        self.adjust_veritcalLayout = QtWidgets.QVBoxLayout(self.adjustWidget)
        self.adjust_veritcalLayout.setContentsMargins(0, 11, 0, 0)
             
        adjustViewTitle = QLabel()
        adjustViewTitle.setText("Adjustment contract pair")
        font = QFont()
        font.setPointSize(10)
        adjustViewTitle.setFont(font)
        adjustViewTitle.setAlignment(Qt.AlignLeft)
        self.adjust_veritcalLayout.addWidget(adjustViewTitle)
        
        self.adjustView = QtWidgets.QTableView(self.adjustWidget)
        self.adjustView.setObjectName("adjustView")
        self.adjust_veritcalLayout.addWidget(self.adjustView)
        
          
    def setupResult(self):
        self.result_window = QtWidgets.QWidget()
        self.outer_horizontalSplitter.addWidget(self.result_window)

        self.result_verticalLayout = QtWidgets.QVBoxLayout(self.result_window)
        self.result_verticalLayout.setContentsMargins(0, 8, 0, 0)
        #self.result_verticalLayout.setSpacing(6)
        self.result_verticalLayout.setObjectName("result_verticalLayout")
        
        self.result_option_horizontalLayout = QtWidgets.QHBoxLayout()
        self.result_option_horizontalLayout.setContentsMargins(0, 0, 0, 0)
        #self.result_option_horizontalLayout.setSpacing(6)
        self.result_option_horizontalLayout.setObjectName("result_option_horizontalLayout")
        self.result_verticalLayout.addLayout(self.result_option_horizontalLayout)
        
        self.matchingLabel = QLabel()
        self.matchingLabel.setText("Matching price:")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.matchingLabel.setSizePolicy(sizePolicy)
        self.matchingLabel.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)    
        self.matchingLabel.setFont(font) 
        self.result_option_horizontalLayout.addWidget(self.matchingLabel)
        
        self.matchingCombo = QComboBox()
        self.result_option_horizontalLayout.addWidget(self.matchingCombo)
        
#         
#         vline = QFrame()
#         vline.setGeometry(QRect(0, 0, 2, 2))
#         vline.setFrameShape(QFrame.VLine)
#         vline.setFrameShadow(QFrame.Sunken)
#         self.result_option_horizontalLayout.addWidget(vline)
        
        self.rollingPeriodLabel = QLabel()
        self.rollingPeriodLabel.setText("Rolling period:")
        self.rollingPeriodLabel.setIndent(30)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rollingPeriodLabel.setSizePolicy(sizePolicy)
        self.rollingPeriodLabel.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)    
        self.rollingPeriodLabel.setFont(font) 
        self.result_option_horizontalLayout.addWidget(self.rollingPeriodLabel)
        
        self.rollingPeriodCombo = QComboBox()
        self.result_option_horizontalLayout.addWidget(self.rollingPeriodCombo)
        
        self.weightLabel = QLabel()
        self.weightLabel.setText("Adjust Weight:")
        self.weightLabel.setIndent(30)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.weightLabel.setSizePolicy(sizePolicy)
        self.weightLabel.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)    
        self.weightLabel.setFont(font) 
        self.result_option_horizontalLayout.addWidget(self.weightLabel)
        
        self.weightCombo = QComboBox()
        self.result_option_horizontalLayout.addWidget(self.weightCombo)
        
        
        spacerItem = QtWidgets.QSpacerItem(20, 40, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.result_option_horizontalLayout.addItem(spacerItem)
        
        self.result_button_horizontalLayout = QtWidgets.QHBoxLayout()
        self.result_button_horizontalLayout.setContentsMargins(0,0, 0, 6)
        self.result_button_horizontalLayout.setSpacing(6)
        self.result_button_horizontalLayout.setObjectName("result_button_horizontalLayout")
        self.result_verticalLayout.addLayout(self.result_button_horizontalLayout)
        
        self.start_adjust_button = QtWidgets.QPushButton(self.perpetual_page)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.start_adjust_button.sizePolicy().hasHeightForWidth())
        self.start_adjust_button.setSizePolicy(sizePolicy)
        self.start_adjust_button.setObjectName("start_adjust_button")
        self.start_adjust_button.setText(translate("MainWindow", "Start Adjustment"))
        self.result_button_horizontalLayout.addWidget(self.start_adjust_button)
        
        self.draw_graph_button = QtWidgets.QPushButton(self.perpetual_page)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.draw_graph_button.sizePolicy().hasHeightForWidth())
        self.draw_graph_button.setSizePolicy(sizePolicy)
        self.draw_graph_button.setObjectName("draw_graph_button")
        self.draw_graph_button.setText(translate("MainWindow", "Draw Graph"))
        self.result_button_horizontalLayout.addWidget(self.draw_graph_button)
        
        self.save_result_button = QtWidgets.QPushButton(self.perpetual_page)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.save_result_button.sizePolicy().hasHeightForWidth())
        self.save_result_button.setSizePolicy(sizePolicy)
        self.save_result_button.setObjectName("save_result_button")
        self.save_result_button.setText(translate("MainWindow", "Save Result"))
        self.result_button_horizontalLayout.addWidget(self.save_result_button)
        
        
        
        resultviewTitle = QLabel()
        resultviewTitle.setText("Adjustment Result")
        font = QFont()
        font.setPointSize(10)
        #font.setBold(True)
        resultviewTitle.setFont(font)
        resultviewTitle.setAlignment(Qt.AlignLeft)
        self.result_verticalLayout.addWidget(resultviewTitle)
        
        
        self.resultView = QtWidgets.QTableView(self.perpetual_page)
        self.resultView.setObjectName("resultView")
        self.result_verticalLayout.addWidget(self.resultView)
        
        #self.outer_horizontalSplitter.addLayout(self.result_verticalLayout)
