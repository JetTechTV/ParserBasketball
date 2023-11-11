import traceback

import requests
from PyQt5.QtCore import *

from Database import Data
from Factory import *
import configparser

class Thread_2(QThread):
    signal_thread_2 = pyqtSignal(int)

    def __init__(self,mainwindow, parent = None):
        QThread.__init__(self, parent)
        self.running = False
        self.mainwindow = mainwindow


    def run(self):
        count = 0
        config = configparser.ConfigParser()
        config.read('settings.ini',encoding='utf-8')
        try:
            self.running = True
            try:
                databasa = Data(config['Database']['road'])
                self.mainwindow.ui.label_4.setText('')
                databasa.clear_table()
            except:
                print(traceback.format_exc())
                self.mainwindow.ui.label_4.setText('База данных не выбрана!')
                return

            league_id = config['League'][self.mainwindow.ui.comboBox.currentText()]

            # Вставляем команды

            res = parse_league_team(league_id)
            for i in res:
                #  print(i)
                # Инфа для вставки в Teams
                TeamID = i['TeamID']
                TeamName = i['CompTeamName']['CompTeamShortNameRu']
                TeamNameEng = i['CompTeamName']['CompTeamNameEn']

                # Вставляем команду
                try:
                    value = databasa.insert_teams(TeamName,TeamNameEng,TeamID)
                except:
                    print(traceback.format_exc())
                # Вставляем игроков

                players = parse_players(TeamID,league_id)

                for j in players['Players']:
                                    count += 1
                                    self.signal_thread_2.emit(count)
                                    databasa.insert_in_players(j, value)


                # Вставляем тренеров
                for j in players['Coaches']:
                    databasa.insert_in_players(j, value)

        except:
            print(traceback.format_exc())