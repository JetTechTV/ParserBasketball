import traceback

from PyQt5.QtCore import *
from Database import Data
from Factory import *

class Thread_3(QThread):
    signal_thread_2 = pyqtSignal(int)

    def __init__(self,mainwindow, parent = None):
        QThread.__init__(self, parent)
        self.running = False
        self.mainwindow = mainwindow


    def run(self):
        config = configparser.ConfigParser()
        config.read('settings.ini', encoding='utf-8')
        try:
            self.running = True
            try:
                databasa = Data(config['Database']['road'])
                self.mainwindow.ui.label_4.setText('')

                databasa.clear_standigs()
            except:
                print(traceback.format_exc())
                self.mainwindow.ui.label_4.setText('База данных не выбрана!')
                return
            config = configparser.ConfigParser()
            config.read('settings.ini')
            league_id = config['League'][self.mainwindow.ui.comboBox.currentText()]

            # Вставляем команды

            res = parse_league_team(league_id)
            for i in res:

                # Инфа для вставки в турнирку
                item = (i['Place'], i['CompTeamName']['CompTeamShortNameRu'], i['Standings']['StandingGame'],
                        i['Standings']['StandingWin'], i['Standings']['StandingLose'],
                        i['Standings']['VictoryPercent'],
                        str(i['Standings']['StandingGoalPlus']) + '/' + str(i['Standings']['StandingGoalMinus']),
                        i['Standings']['StandingGoalPlus'] - i['Standings']['StandingGoalMinus'],
                        round(i['Standings']['StandingGoalPlus'] / i['Standings']['StandingGoalMinus'], 2))
                databasa.insert_standings(item)
        except:
            print(traceback.format_exc())