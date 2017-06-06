'''
Created on May 15, 2017

@author: kevin
'''
from PyQt5.QtWidgets import QStyledItemDelegate, QCheckBox, QStyleOptionButton, QStyle, QApplication
from PyQt5.QtCore import Qt

class CheckBoxDelegate(QStyledItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every
    cell of the column to which it's applied
    """

    def createEditor(self, parent, option, index):
        editor = QCheckBox(parent)
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
         
    def paint(self, painter, option, index):
        '''
        Paint a checkbox without the label.
        '''
        painter.save()
        checked = index.model().data(index, Qt.EditRole).value()
       
        check_box_style_option = QStyleOptionButton()
    
#         if (index.flags() & Qt.ItemIsEditable) > 0:
#             check_box_style_option.state |= QStyle.State_Enabled
#         else:
#                     check_box_style_option.state |= QStyle.State_ReadOnly      
        if checked:
            check_box_style_option.state |= QStyle.State_On        
        else:
            check_box_style_option.state |= QStyle.State_Off
        check_box_style_option.rect = option.rect
#         if not index.model().hasFlag(index, Qt.ItemIsEditable):
#             check_box_style_option.state |= QStyle.State_ReadOnly
        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)    
        painter.restore()
 
       
    def setModelData(self, editor, model, index):
        """
        Toggle the bool
        """
        if editor.checkState() == Qt.Checked:    
            model.setData(index, True, Qt.EditRole)
        else:
            model.setData(index, False, Qt.EditRole)
    
    def setEditorData(self, editor, index):
        data = index.model().data(index, Qt.EditRole).value()
        if data == True:
            editor.setCheckState(Qt.Checked)
        else:
            editor.setCheckState(Qt.Unchecked)
        