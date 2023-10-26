import os
import shutil
import subprocess
import sys
from distutils.dir_util import copy_tree
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import kuffers_test as kt


form_class = uic.loadUiType("kuffers.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 모델
        self.model_path = ""
        self.model_name = ""
        self.g_model = None
        # 데이터셋 파일 저장 리스트
        self.dataset_list_dir = ""
        # 그림 데이터 모든파일의 절대경로
        self.img_all_list = []
        # 화면에 표시된 데이터셋 파일과 결과파일의 절대값 주소
        self.original_img = ""
        self.original_img_name = ""
        # treeView 목록 파일을 클릭하면 그 파일의 절대값을 저장
        self.tree_View_file_click = ""

        self.pushButton_model.clicked.connect(self.modelSelect)
        self.pushButton_dataset.clicked.connect(self.datasetDirSelect)
        self.start_button.clicked.connect(self.runFile)


    def modelSelect(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getOpenFileNames(self, "Select Files")[0]
        self.g_model = file_path[0]
        self.model_path = file_path[0]
        self.model_name = os.path.basename(file_path[0])

        sys.excepthook = pyqtExceptionHandler

    def datasetDirSelect(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.dataset_list_dir = file_path

        self.model_file_system = QFileSystemModel()
        self.model_file_system.setRootPath(self.dataset_list_dir)
        self.model_file_system.setReadOnly(False)
        self.treeView.setModel(self.model_file_system)
        self.treeView.setRootIndex(self.model_file_system.index(self.dataset_list_dir))
        self.treeView.doubleClicked.connect(lambda index: self.treeViewDoubleClicked(index))
        self.treeView.setDragEnabled(True)
        self.treeView.setColumnWidth(0, 300)

        sys.excepthook = pyqtExceptionHandler

    def treeViewDoubleClicked(self, index, pyqtExceptionHandler=None):
        self.tree_View_file_click = self.model_file_system.filePath(index)
        self.original_img = self.tree_View_file_click
        self.original_img_name = os.path.basename(self.original_img)

        pixmap = QPixmap(self.tree_View_file_click)
        pixmap = pixmap.scaled(self.label_D.size(), aspectRatioMode=True)
        self.label_D.setPixmap(pixmap)


        sys.excepthook = pyqtExceptionHandler

    def runFile(self, pyqtExceptionHandler=None):
        if self.g_model == None:
            self.msg_model_none()
        else:
            kt.test_one_sample(self.original_img, self.model_name)
            self.msg_box_end()

        sys.excepthook = pyqtExceptionHandler

    def msg_box_end(self):
        msg = QMessageBox()
        msg.setWindowTitle("Detection")
        msg.setText(f'{kt.print_msg[0]}\n{kt.print_msg[1]}')
        msg.exec_()

    def msg_model_none(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText('model 파일이 없습니다.')
        msg.exec_()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


