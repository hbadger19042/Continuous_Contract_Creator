'''
Created on May 21, 2017

@author: dongi
'''

from .csvhandler import CSVHandler
from .excelhandler import ExcelHandler

import logging

iofactoryLogger = logging.getLogger("ioFactory.py")

class IOFactory():
    @staticmethod
    def CreateHandler(filepath):
        if filepath[-5:] == ".xlsx" or filepath[-4:]==".xls":
            return ExcelHandler(filepath)
        elif filepath[-4:] == ".csv":
            return CSVHandler(filepath)
        else:
            iofactoryLogger.info("Unsupported filetype: %s" %filepath)
            return None
            