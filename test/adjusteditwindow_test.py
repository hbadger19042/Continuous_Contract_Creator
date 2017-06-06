'''
Created on May 20, 2017

@author: dongi
'''

import sys
from rollover.shift.adjustEditWindow import Ui_RpEditWindow
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)

window = Ui_RpEditWindow("old", "new")
window.show()


sys.exit(app.exec_())

