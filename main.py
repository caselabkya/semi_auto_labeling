import sys
import os
import cv2
import execute_fsam
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
print("sdfsdf")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Second Window
class SecondWindow(QMainWindow):
    def __init__(self):
        super(SecondWindow, self).__init__()
        loadUi(f"{DIR_PATH}/secondwindow.ui", self)
        self.setWindowTitle("Image")
        self.fs = execute_fsam.FSAM()
        self.right_arrow = False

    def load_image(self, filepath):
        # 이미지 불러오기
        self.scene = QGraphicsScene(self)
        self.graphv.setScene(self.scene)
        self.graphv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        pixmap = QPixmap(filepath)
        w = int(pixmap.width()*0.5)
        h = int(pixmap.height()*0.5)
        pixmap = pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation) # 종횡비 및 scale 할 때 이미지 화질 조정
        self.resize(w,h)
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.graphv.resize(w, h)
        
    def keyPressEvent(self, event):
        if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
            self.graphv.setDragMode(QGraphicsView.ScrollHandDrag)
        elif event.key() == Qt.Key.Key_Right:
            self.right_arrow = True
            print('right arrow pressed')


    def keyReleaseEvent(self, event):
        self.graphv.setDragMode(QGraphicsView.NoDrag)
        self.right_arrow = False
    
    def resizeEvent(self, event):   # 윈도우 크기가 조정될 때마다 호출되는 이벤트 핸들러
        window_size = self.size()  # 현재 윈도우 크기 가져오기
        self.graphv.resize(window_size.width(), window_size.height())  # 이미지 크기 조정
    
    def wheelEvent(self, event):    # 이미지 Zoom in/out
        if event.angleDelta().y() > 0:  # 스크롤 범위 (0, -120<y<120)
            self.graphv.scale(1.1, 1.1) # 확대
        else:
            self.graphv.scale(0.9, 0.9) # 축소
    
    def mousePressEvent(self, event):
        self.x = event.x()
        self.y = event.y()
        # self.fs.execute_fsam(filepath, [[self.x, self.y]])

# Thread_1
class Thread_1(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.w = SecondWindow()

    def open_image(self, filepath):
        self.w.load_image(filepath)
        self.w.show()

    def thd_1_stop(self):
        self.quit()

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(f"{DIR_PATH}/mainwindow.ui", self)
        self.right_arrow = False
        # Thread
        self.thd_1 = Thread_1()
        # buttons
        self.open_folder_btn.clicked.connect(self.open_folder_btn_clicked)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.right_arrow = True
            print('right arrow pressed')

    def keyReleaseEvent(self, event):
        self.right_arrow = False

    def open_folder_btn_clicked(self):    # load image file
        self.folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        file_names = os.listdir(self.folder)    # ['dogs.jpg', 'cat.jpg']
        file_name_idx = 0
        if file_names is None:
            return
        if self.right_arrow:
            file_name_idx += 1
            self.thd_1.open_image(f'{self.folder}/{file_names[file_name_idx]}')
            self.thd_1.w.move(self.x() + self.width(), self.y())    # mainwindow 옆에 secondwindow 열기
            self.thd_1.start()
            self.thd_1.thd_1_stop()
        else:
            self.thd_1.open_image(f'{self.folder}/{file_names[file_name_idx]}')
            self.thd_1.w.move(self.x() + self.width(), self.y())    # mainwindow 옆에 secondwindow 열기
            self.thd_1.start()
            self.thd_1.thd_1_stop()

        # for file_name in file_names:


if __name__== "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.installEventFilter(ui)
    ui.show()
    sys.exit(app.exec_())