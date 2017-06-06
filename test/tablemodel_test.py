'''
Created on May 14, 2017

@author: dongi
'''

from PyQt5.Qt import QModelIndex

from rollover.tablemodel import TableModel

def test_setData():
    header = ["file name", "start date", "end date", "base"]
    filemodel = TableModel(4, 20, header)
    
    index = filemodel.index(0, 0, QModelIndex())
    test_string = "hello"
    filemodel.setData(index, test_string)      
    result_string = filemodel.data(index) 
    assert test_string == result_string
