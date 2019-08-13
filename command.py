import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'AR벤저스'
        self.left = 50
        self.top = 50
        self.width = 1000
        self.height = 1000
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        btn_drive_mode = QPushButton('주행모드 증강현실 시스템', self)
        btn_drive_mode.resize(300, 80)
        btn_drive_mode.move(150, 70)
        btn_drive_mode.clicked.connect(self.on_click_AR_Drive_Mode)

        btn_pikachu = QPushButton('피카츄 증강현실', self)
        btn_pikachu.resize(300, 80)
        btn_pikachu.move(150, 170)
        btn_pikachu.clicked.connect(self.on_click_AR_Pikachu)

        btn_spring = QPushButton('봄 증강현실', self)
        btn_spring.resize(300, 80)
        btn_spring.move(150, 270)
        btn_spring.clicked.connect(self.on_click_AR_Spring)

        btn_fall = QPushButton('가을 증강현실', self)
        btn_fall.resize(300, 80)
        btn_fall.move(150, 370)
        btn_fall.clicked.connect(self.on_click_AR_Fall)

        btn_Snow = QPushButton('설원 증강현실', self)
        btn_Snow.resize(300, 80)
        btn_Snow.move(150, 470)
        btn_Snow.clicked.connect(self.on_click_AR_Snow)

        self.setStyleSheet("background-image: url(pika_pic.jpg);")
        self.show()

    @pyqtSlot()
    def on_click_AR_Drive_Mode(self):
        os.system('Drive_Mode.py')

    @pyqtSlot()
    def on_click_AR_Pikachu(self):
        os.system('pikachu.py')

    @pyqtSlot()
    def on_click_AR_Spring(self):
        os.system('spring.py')

    @pyqtSlot()
    def on_click_AR_Fall(self):
        os.system('fall.py')

    @pyqtSlot()
    def on_click_AR_Snow(self):
        os.system('snow.py')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
