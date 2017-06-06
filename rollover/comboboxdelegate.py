'''
Created on May 15, 2017

@author: kevin
'''
from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox

class ComboBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        choices =["Not set", "Set as base"]
        editor.addItems(choices)
        return editor
       
    def setModelData(self, editor, model, index):
        if editor.currentIndex() == 1:
            model.setData(index, "base")
        else:
            model.setData(index, None)
    
    def setEditorData(self, editor, index):
        if index.model().data(index):
            editor.setCurrentIndex(1)
        else:
            editor.setCurrentIndex(0)
        