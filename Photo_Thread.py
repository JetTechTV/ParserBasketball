import traceback

import requests
from PyQt5.QtCore import *

from Database import Data
from Factory import *
import configparser
import os

class Thread_4(QThread):
    signal_thread_2 = pyqtSignal(int)

    def __init__(self,mainwindow, parent = None):
        QThread.__init__(self, parent)
        self.running = False
        self.mainwindow = mainwindow


    def run(self):
        config = configparser.ConfigParser()
        config.read('settings.ini',encoding='utf-8')
        try:
            self.running = True
            try:
                databasa = Data(config['Database']['road'])
                self.mainwindow.ui.label_4.setText('')
            except:
                print(traceback.format_exc())
                self.mainwindow.ui.label_4.setText('База данных не выбрана!')
                return

        except:
            print(traceback.format_exc())
            return

        road_league = config['Photo_road'][self.mainwindow.ui.comboBox.currentText()]
        teams = databasa.select_current_teams()
        for team in teams:
            try:
                players = os.listdir(road_league+team[0])

                for i in players:
                    if not '.' in i:
                        continue
                    photo_link = road_league + team[0] + '\\' + i
                    TeamID = team[1]
                    PlayerNumber = self.factory_number(i)
                    print(PlayerNumber,photo_link)
                    databasa.update_photo(photo_link,TeamID,PlayerNumber)


            except:
                pass


    @staticmethod
    def factory_number(s:str):
        if '_' in s:
            number = s.split('_')[0]
            if number.isdigit():
                return number
        elif ' ' in s:
            number = s.split(' ')[0]
            if number.isdigit():
                return number
        else:
            return s.split('.')[0]


