import sys
import traceback
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import  QMainWindow,QApplication,QTableWidgetItem,QFileDialog,QApplication
from pathlib import Path
from window import Ui_MainWindow
from Database import Data
from Factory import *
from Thread_2 import Thread_2
from Thread_Tour import Thread_3
from Photo_Thread import Thread_4
class ImageDialog(QMainWindow):

    def __init__(self):
        super().__init__()
        self.settings = QSettings('Parser', 'Parser')

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.launch_thread)
        self.ui.pushButton_3.clicked.connect(self.launch_tour_update)
        self.ui.pushButton_4.clicked.connect(self.launch_photo_thread)
        self.fill_league()


    def closeEvent(self, event):
        self.settings.setValue('road_file', self.ui.lineEdit_2.text())


    def launch_thread(self):
        try:
            if self.mythread_2.isRunning():
                self.mythread_2.terminate()
                self.mythread_2 = Thread_2(mainwindow=self)
                self.mythread_2.start()
                self.mythread_2.signal_thread_2.connect(self.show_status)
            else:
                self.mythread_2 = Thread_2(mainwindow=self)
                self.mythread_2.start()
                self.mythread_2.signal_thread_2.connect(self.show_status)

        except:
            self.mythread_2 = Thread_2(mainwindow=self)
            self.mythread_2.start()
            self.mythread_2.signal_thread_2.connect(self.show_status)

    def fill_league(self):
        config = configparser.ConfigParser()
        config.read('settings.ini',encoding='utf-8')
        for key in config['League']:
            self.ui.comboBox.addItem(key)

    def show_status(self,count):
        s = f'Вставлено {count} игроков'
        self.ui.label_3.setText(s)

    def launch_tour_update(self):
        try:
            if self.mythread_3.isRunning():
                self.mythread_3.terminate()
                self.mythread_3 = Thread_3(mainwindow=self)
                self.mythread_3.start()
            else:
                self.mythread_3 = Thread_3(mainwindow=self)
                self.mythread_3.start()

        except:
            self.mythread_3 = Thread_3(mainwindow=self)
            self.mythread_3.start()


    def launch_photo_thread(self):
        try:
            if self.mythread_4.isRunning():
                self.mythread_4.terminate()
                self.mythread_4 = Thread_4(mainwindow=self)
                self.mythread_4.start()
            else:
                self.mythread_4 = Thread_4(mainwindow=self)
                self.mythread_4.start()

        except:
            self.mythread_4 = Thread_4(mainwindow=self)
            self.mythread_4.start()

app = QApplication(sys.argv)
window = ImageDialog()
window.show()

sys.exit(app.exec())