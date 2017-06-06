'''
Created on May 9, 2017

@author: dongi
'''

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from rollover.loggerSetting import SetLogger
from rollover.mainwindow import Ui_MainWindow
from rollover.Shift.shiftmain import ShiftMain
from rollover.Perpetual.perpetualMain import PerpetualMain


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.shiftmain = ShiftMain(self)
        self.shiftmain.setupShiftMain()
        
        
        self.perpetualMain = PerpetualMain(self)
        self.perpetualMain.setupPerpetualMain()
    
        self._SetupMainStackedWidget()
        
    def _SetupMainStackedWidget(self):
        #Set up backward/forward adjustment page as default.
        self.ui.shift_button.toggle()
        self.ui.shift_main_stacked.setCurrentIndex(0)
        
        self.ui.shift_button.clicked.connect(lambda: self.ui.shift_main_stacked.setCurrentIndex(0))
        self.ui.perpetual_button.clicked.connect(lambda: self.ui.shift_main_stacked.setCurrentIndex(1))
        
def StartMainWindow():      
    SetLogger()
    app = QApplication(sys.argv)
    mwindow = MainWindow()
    mwindow.show()   
    
    sys.exit(app.exec_())  
                  
if __name__ == "__main__":
    StartMainWindow()

