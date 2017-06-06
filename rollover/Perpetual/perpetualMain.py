'''
Created on May 20, 2017

@author: dongi'''

from PyQt5.QtWidgets import QHeaderView, QMenu, QFileDialog, QProgressDialog
from PyQt5.QtCore import Qt, pyqtSlot, QObject, QCoreApplication
from PyQt5.Qt import QModelIndex

from ..RPEdit.rpEditMain import RpEditMain
from ..filelistModel import FilelistModel
from ..IO.ioFactory import IOFactory
from ..resultModel import ResultModel
from ..Contract.contractMain import ContractMain
from .perpetualAdjustModel import PerpetualAdjustModel

from enum import IntEnum
import os, subprocess
from ..RPCalculator.rpByEndDate import RPByEndDate
from operator import itemgetter


translate = QCoreApplication.translate

class MatchingPrice(IntEnum):
    OPEN = 1
    HIGH = 2
    LOW = 3
    CLOSE = 4

class AdjustWeightType(IntEnum):
    TIME = 1
    VOLUME = 2

class PerpetualMain(QObject):
    contractEditor_dict = {}
    rpEditor_dict = {}
    def __init__(self, mainwindow):
        super().__init__()        
        self.mainwindow = mainwindow
        self.filelistView = self.mainwindow.ui.perpetualUi.filelistView
        self.adjustView = self.mainwindow.ui.perpetualUi.adjustView
        self.resultView = self.mainwindow.ui.perpetualUi.resultView
        self.addFiles_button = self.mainwindow.ui.perpetualUi.add_files_button
        self.startAdjust_button = self.mainwindow.ui.perpetualUi.start_adjust_button
        self.saveResult_button = self.mainwindow.ui.perpetualUi.save_result_button
        self.matchingPriceIndex = MatchingPrice.OPEN
        self.rollingPeriod = 4
        self.adjustWeightType = AdjustWeightType.TIME
        self.matchingCombo = self.mainwindow.ui.perpetualUi.matchingCombo
        self.rollingCombo = self.mainwindow.ui.perpetualUi.rollingPeriodCombo
        self.weightCombo = self.mainwindow.ui.perpetualUi.weightCombo

    def setupPerpetualMain(self):                
        self._setFilelistTable()
        self._setup_AdjustTable()
        self._setupResultTable()
        self._setupMatchingComboBox()
        self._setupRollingComboBox()
        self._setupWeightComboBox()
        
        self.filelistView.doubleClicked.connect(self.on_filelist_view_dclicked) 
        self.adjustView.doubleClicked.connect(self.on_adjustment_view_dclicked) 
 
        self.addFiles_button.clicked.connect(self.on_addFileButton_clicked)
        self.startAdjust_button.clicked.connect(self.on_startAdjustmentButton_clicked)
        self.saveResult_button.clicked.connect(self.on_saveResult_clicked)
                
        self.filelistView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.filelistView.customContextMenuRequested.connect(self._filelist_view_context) 
        self.resultView.setContextMenuPolicy(Qt.CustomContextMenu) 
        self.resultView.customContextMenuRequested.connect(self._result_view_context)  
        
        self.matchingCombo.currentIndexChanged.connect(self._set_matching_price_index)
        self.rollingCombo.currentIndexChanged.connect(self._set_rolling_period_index)
        self.weightCombo.currentIndexChanged.connect(self._set_weight_index)
        
    def _setFilelistTable(self):
        fileHeaderview = QHeaderView(Qt.Horizontal)
        fileHeaderview.resizeSections(QHeaderView.Interactive)
        styleSheet = """
            QHeaderView::section{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #616161, stop: 0.5 #505050,
                    stop: 0.6 #434343, stop:1 #656565);
                color:white;
                border:0.5px solid;                
            }
            """
        fileHeaderview.setStyleSheet(styleSheet)
        self.filelistView.setHorizontalHeader(fileHeaderview)
    
        header = ["file name", "start date", "end date"]
        row_length = 0
        self.col_length = 3
        self.filemodel = FilelistModel(row_length, self.col_length, header)
        self.filelistView.setModel(self.filemodel)   

    @pyqtSlot("QPoint")
    def _filelist_view_context(self, pos):
        context_menu = QMenu()
        remove_row_action = context_menu.addAction("Remove selected rows")
        new_action = context_menu.exec_(self.filelistView.mapToGlobal(pos))
        if new_action == remove_row_action:
            smodel = self.filelistView.selectionModel()
            index_list = smodel.selectedIndexes()
            rowSet = set()
            for index in index_list:
                rowSet.add(index.row())        
            for row in sorted(rowSet, reverse=True):
                self.filemodel.removeRows(row, 1, QModelIndex())
                newList = self.filemodel.getContractList()
                self.adjustmodel.syncDataWithFileList(newList)

           
    @pyqtSlot("QPoint")
    def _result_view_context(self, pos):
        context_menu = QMenu()
        remove_row_action = context_menu.addAction("Remove selected rows")
        new_action = context_menu.exec_(self.resultView.mapToGlobal(pos))
        if new_action == remove_row_action:
            smodel = self.resultView.selectionModel()
            index_list = smodel.selectedIndexes()
            rowlist =[]
            for index in index_list:
                rowlist.append(index.row())        
            for row in sorted(set(rowlist), reverse=True):
                self.resultmodel.removeRows(row, 1, QModelIndex())
                
                                    
    @pyqtSlot('QModelIndex')    
    def on_filelist_view_dclicked(self, index):        
        filelistModel = index.model()
        row = index.row()
        contract_name = filelistModel.filelistData[row][0]
        if contract_name not in self.contractEditor_dict.keys():            
            raise Exception("Contract name is not in the list")
        else: 
            self.contractEditor_dict[contract_name].show()

    def _setup_AdjustTable(self):
        adjustHeaderview = QHeaderView(Qt.Horizontal)
        adjustHeaderview.resizeSections(QHeaderView.Interactive)
        styleSheet = """
            QHeaderView::section{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #616161, stop: 0.5 #505050,
                    stop: 0.6 #434343, stop:1 #656565);
                color:white;
                border:0.5px solid;                
            }
            """
        adjustHeaderview.setStyleSheet(styleSheet)
        self.adjustView.setHorizontalHeader(adjustHeaderview)                
        header = ["first contract", "start date", "end date", 
                  "second contract", "start date", "end date", "roll point"]
        row_length = 0
        col_length = 7
        self.adjustmodel = PerpetualAdjustModel(row_length, col_length, header)
        self.adjustmodel.setContractDataDict(self.contractEditor_dict)
        self.adjustmodel.setRollPointCalculator(RPByEndDate(self.matchingPriceIndex))
        self.adjustView.setModel(self.adjustmodel)

    @pyqtSlot('QModelIndex')    
    def on_adjustment_view_dclicked(self, index):  
        adjust_model = index.model()
        row = index.row()
        data_list = adjust_model.displayData[row]
        old_name = data_list[0]
        old_data = self.contractEditor_dict[old_name].getContractData()
        new_name = data_list[3]
        new_data = self.contractEditor_dict[new_name].getContractData()
        default_base_point = data_list[-1]
        rp_editor=None
        editor_name = RpEditMain.make_rp_editor_name(old_name, new_name)
        if editor_name not in self.rpEditor_dict.keys():            
            rp_editor = RpEditMain(old_name, new_name)
            rp_editor.rpChanged.connect(self.adjustmodel.setRollPoint)
            self.rpEditor_dict[editor_name] = rp_editor
            rp_editor.show()
            rp_editor.loadData(old_data, new_data, default_base_point)
            bpIndex = rp_editor.getBpIndex()
            rp_editor.rpUi.editView.setCurrentIndex(bpIndex)
        else: 
            rp_editor = self.rpEditor_dict[editor_name]
            bpIndex = rp_editor.getBpIndex()
            rp_editor.rpUi.editView.setCurrentIndex(bpIndex)
            rp_editor.show()

                    
    @pyqtSlot()   
    def on_startAdjustmentButton_clicked(self):
        """
        Calculate adjusted time series accodring to adjustment model's 
        display data. This assumes that display data is ordered by the time
        of first contract.
        """
        self.resultmodel.clear()
        from .perpetualAdjustLogic import PerpetualAdjustLogic
        adjust_logic = PerpetualAdjustLogic(self.adjustmodel.displayData, 
                    self.contractEditor_dict, self.matchingPriceIndex)
        adjust_logic.MakeAdjustment(self.resultmodel, self.rollingPeriod, self.adjustWeightType)
    
   
                    
    def find_row_index_of_rp(self, data, rp):
        for row_index, sublist in enumerate(data):
            if sublist[0] == rp:
                return row_index
        return None         


    def _setupMatchingComboBox(self):
        self.matchingCombo.insertItem(0, "Open price")
        self.matchingCombo.insertItem(1, "High price")
        self.matchingCombo.insertItem(2, "Low price")
        self.matchingCombo.insertItem(3, "Close price")        
        self.matchingCombo.setCurrentIndex(0)


    @pyqtSlot(int)
    def _set_matching_price_index(self, method_number):
        if MatchingPrice.OPEN == method_number+1:
            self.matchingPriceIndex = MatchingPrice.OPEN
        elif MatchingPrice.HIGH == method_number+1:
            self.matchingPriceIndex = MatchingPrice.HIGH
        elif MatchingPrice.LOW == method_number+1:
            self.matchingPriceIndex = MatchingPrice.LOW
        elif MatchingPrice.CLOSE == method_number+1:
            self.matchingPriceIndex = MatchingPrice.CLOSE          
        
    def _setupRollingComboBox(self):
        self.rollingCombo.insertItem(0, "4")
        self.rollingCombo.insertItem(1, "6")
        self.rollingCombo.insertItem(2, "8")
        self.rollingCombo.insertItem(3, "10")    
        self.rollingCombo.insertItem(4, "12")
        self.rollingCombo.insertItem(5, "14")
        self.rollingCombo.insertItem(6, "16")
        self.rollingCombo.insertItem(7, "18")  
        self.rollingCombo.setCurrentIndex(0)        

            
    @pyqtSlot(int)
    def _set_rolling_period_index(self, combo_index):
        self.rollingPeriod = combo_index*2 + 4
        
        
    def _setupWeightComboBox(self):
        self.weightCombo.insertItem(0, "Time to roll point")
        self.weightCombo.insertItem(1, "Volume")
        self.rollingCombo.setCurrentIndex(0)     

    @pyqtSlot(int)
    def _set_weight_index(self, combo_index):
        if combo_index == 0:
            self.adjustWeightType = AdjustWeightType.TIME
        elif combo_index == 1:
            self.adjustWeightType = AdjustWeightType.VOLUME
        
    def _setupResultTable(self):
        resultHeaderview = QHeaderView(Qt.Horizontal)
        resultHeaderview.resizeSections(QHeaderView.Interactive)
        styleSheet = """
            QHeaderView::section{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #616161, stop: 0.5 #505050,
                    stop: 0.6 #434343, stop:1 #656565);
                color:white;
                border:0.5px solid;                
            }
            """
        resultHeaderview.setStyleSheet(styleSheet)
        #resultHeaderview.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.resultView.setHorizontalHeader(resultHeaderview)  
        
        header = ["date", "open", "high", "low", "close", "volume", "adjustment", "contract name"]
        row_size = 0
        col_size = 8
        self.resultmodel = ResultModel(row_size, col_size, header)        
        self.resultView.setModel(self.resultmodel)       
    
    @pyqtSlot()
    def on_saveResult_clicked(self): 
        path = QFileDialog.getSaveFileName(self.mainwindow, "Save File")
        saveHandler = IOFactory.CreateHandler(path[0])
        if not saveHandler:
            return
        saveHandler.SaveFile(self.resultmodel.displayData)  
        dir_name = os.path.dirname(os.path.abspath(path[0]))
        subprocess.Popen(r'explorer /select, %s' %dir_name)
        
               
    @pyqtSlot()
    def on_addFileButton_clicked(self):        
        fileDialog = QFileDialog(self.mainwindow)
        fileDialog.setFileMode(QFileDialog.ExistingFiles)
        fileDialog.setViewMode(QFileDialog.List)
        if fileDialog.exec_():
            file_paths = fileDialog.selectedFiles()
            whole_task_num = len(file_paths)*4
            progress = 0
            progressDialog = QProgressDialog("Accessing data....", "cancel", 0, 
                            whole_task_num, self.filelistView)
            progressDialog.setWindowModality(Qt.ApplicationModal)
            progressDialog.setValue(0)
            progressDialog.show()
            QCoreApplication.processEvents()            
            
            for each_path in file_paths:
                reader = IOFactory.CreateHandler(each_path)
                if not reader:
                    continue
                new_data = reader.ReadSingleFile()
                progress += 1
                progressDialog.setValue(progress)       
                for each_data in new_data.items(): 
                    if len(each_data[1]) > 1:
                        if each_data[1][0][0] > each_data[1][1][0]:
                            sorted_data = sorted(each_data[1], key=itemgetter(0))   
                        else:
                            sorted_data = each_data[1]
                    elif len(each_data[1]) == 0:
                        progress += 3
                        continue    
                    filemodeldata= [each_data[0], sorted_data[0][0], sorted_data[-1][0]]           
                    self.filemodel.appendRow(filemodeldata)
                    progress += 1
                    progressDialog.setValue(progress)                 
                    new_contract_name = each_data[0]
                    if new_contract_name not in self.contractEditor_dict.keys():
                        new_contract_editor = ContractMain(new_contract_name, sorted_data)
                        self.contractEditor_dict[new_contract_name] = new_contract_editor
                    progress += 1
                    progressDialog.setValue(progress)  
                    progressDialog.forceShow()
                    QCoreApplication.processEvents()
                    contract_range = [sorted_data[0][0], sorted_data[-1][0]]
                    self.adjustmodel.addNewContract(each_data[0], contract_range)
                    progress += 1
                    progressDialog.setValue(progress)
            progressDialog.close()
    
    @staticmethod               
    def UpdateRollEditor(contract_name):
        """
        Update roll point editor to match with change in contract data.
        """
        for editor_name in PerpetualMain.rpEditor_dict:
            old_cont, new_cont = RpEditMain.parse_rp_editor_name(editor_name)         
            if old_cont == contract_name or new_cont == contract_name:
                old_data = PerpetualMain.contractEditor_dict[old_cont].getContractData()
                new_data = PerpetualMain.contractEditor_dict[new_cont].getContractData()
                
                rpCal = RPByEndDate()
                new_rp = rpCal.CalculateByMaxVolume(old_data, new_data)
                
                PerpetualMain.rpEditor_dict[editor_name].loadData(old_data, new_data, new_rp)
                
#     def getContractDataDict(self):
#         """
#         Get contract data dictionary from roll pointer editor
#         """
#         contract_dict = {}
#         for name, each_editor in self.contractEditor_dict.items():
#             contract_dict[name] = each_editor.getContractData()
#         return contract_dict