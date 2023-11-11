import traceback
from datetime import datetime
import pyodbc
from random import *
from Factory import *
class Data:
    def __init__(self, road):
        self.static_road = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + road
        self.conn = pyodbc.connect(self.static_road)


    def insert_in_players(self,player:tuple,team_id:str):
        cursor = self.conn.cursor()
        # Проверяем есть ли в БД игрок
        sql_check = """Select ID FROM Players Where PlayerID_EXT_Str = ?"""
        cursor.execute(sql_check, (player[0]))
        try:
            res = cursor.fetchone()[0]
            return res
        except:
            pass


        ampluas = {
            'Разыгрывающий': 9,
            'Атакующий защитник': 10,
            'Легкий форвард': 7,
            'Центровой':6,
            'Тяжелый форвард':8,
            'Игрок':0,
            'Тренер': 2
        }

        sql = """
                                                    SELECT ID FROM  Players
                                              """
        cursor.execute(sql)
        values = cursor.fetchall()
        try:
            value = max([int(i[0]) for i in values]) + 1
        except:
            value = 1

        # (PlayerID,F,I,F_ENG,I_ENG,Birthday,PlayerRole,PlayerNumber,Country,Height,Weight)
        sql_insert = """
                                                                Insert into Players (ID,SportID,F,I,F_Eng,I_Eng,TeamID,PlayerID_EXT_Str,PlayerNumber,PlayerRoleID,CountryID,CityID,BirthDay,Height,Weight)
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                     """
        #                                  F         I         F_ENG     I_ENG             ID_EXT    Number    RoleID
        cursor.execute(sql_insert,(value,1,player[1],player[2],player[3],player[4],team_id,player[0],player[7],ampluas[player[6]],self.select_countryID(player[8]),0,player[5],player[-2],player[-1]))
        cursor.commit()
        cursor.close()


    def insert_teams(self,team_name,team_name_eng,team_id_ext):
        cursor = self.conn.cursor()

        # Проверяем есть ли там команда
        sql_check = """Select ID FROM Teams Where ExtID = ?"""
        cursor.execute(sql_check,(team_id_ext))
        try:
            res = cursor.fetchone()[0]
            return res
        except:
            pass
        sql = """
                            SELECT ID FROM  Teams
                      """

        cursor.execute(sql)
        values = cursor.fetchall()
        try:
            value = max([int(i[0]) for i in values]) + 1
        except:
            value = 1

        sql_insert = """
                                        Insert into Teams (ID,SportID,TeamName,TeamName_Eng,ExtID,CountryID,CityID)
                                        VALUES (?,?,?,?,?,?,?)
                                      """
        if team_name == 'Локомотив-К':
            team_name = 'Локомотив-Кубань'
        cursor.execute(sql_insert, (str(value), '1', team_name,team_name_eng, team_id_ext,'41','48'))
        cursor.commit()
        cursor.close()
        return value




    def select_countryID(self,name:str):
        cursor = self.conn.cursor()

        sql_select = """
                                Select ID FROM Countries Where  CountryName = ?
                     """

        cursor.execute(sql_select, (name))
        res = cursor.fetchone()
        try:
            return res[0]
        except:
            # Вставляем страну в таблицу
            sql_id = """Select ID From Countries"""
            ID = max([int(i[0]) for i in cursor.execute(sql_id).fetchall()]) + 1
            print(ID)
            sql_insert = """Insert into Countries (ID,CountryName)
                                    VALUES (?,?)"""
            cursor.execute(sql_insert, (ID, name))
            cursor.commit()
            cursor.close()
            return ID

    def insert_standings(self,item:tuple):
        cursor = self.conn.cursor()

        # Проверяем есть ли там команда
        sql_check = """Select RANK FROM TeamStandings Where TEAM = ?"""

        sql_update = """
                        UPDATE TeamStandings SET RANK = ?, GAMES = ?,WINS =?,LOST=?,PROCENT=?,PTS_OPTS=?,PLUS_MINUS=?,PPG_OPPG=?,Place=? WHERE TEAM = ?
                     """
        sql_insert = """
                        Insert into TeamStandings  (RANK,TEAM,GAMES,WINS,LOST,PROCENT,PTS_OPTS,PLUS_MINUS,PPG_OPPG,Place,Stage)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)
                     """
        if item[1] ==     'Локомотив-К':
            team_name  = 'Локомотив-Кубань'
        else:
            team_name = item[1]
        cursor.execute(sql_check, (team_name))

        try:
            res = cursor.fetchone()[0]
            cursor.execute(sql_update,(item[0],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[0],item[1]))
        except:
            cursor.execute(sql_insert,(item[0],team_name,item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[0],'Regular'))

        cursor.commit()
        cursor.close()

        
    def clear_table(self):
        cursor = self.conn.cursor()

        sql_2 = """
                    DELETE * from Players
                """
        sql_3 = """
                    DELETE * FROM MatchPlayers
                """
        sql_4 = """
                    DELETE * FROM MatchStatistics
                """
        cursor.execute(sql_3)
        cursor.execute(sql_4)
        cursor.execute(sql_2)
        cursor.commit()
        cursor.close()

    def clear_standigs(self):
        cursor = self.conn.cursor()
        sql = """
                                DELETE * from TeamStandings
                              """

        cursor.execute(sql)
        cursor.commit()
        cursor.close()



    def select_current_teams(self):
        cursor = self.conn.cursor()
        sql = """
                 Select TeamName,TeamID FROM Teams,Players WHERE Teams.ID = Players.TeamID
              """
        cursor.execute(sql)
        return set([(i[0].strip(),i[1].strip()) for i in cursor.fetchall()])

    def update_photo(self,Photo_link:str,teamID:str,playerNumber:str):
        cursor = self.conn.cursor()
        sql = """
                UPDATE Players SET Foto_big = ? WHERE TeamID = ? and PlayerNumber = ?
              """
        cursor.execute(sql,(Photo_link,teamID,playerNumber))
        cursor.commit()

    
# data = Data('C:\\Users\\biggvladik\\Downloads\\BasketBall_21_Mtv.mdb')
# print(data.select_current_teams())