import traceback
import configparser
import requests
from bs4 import BeautifulSoup
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_team_links():
        response = requests.get('https://vtb-league.com/')
        soup = BeautifulSoup(response.text, 'lxml')

        columns = soup.find('ul', class_='hidden-xs dropdown-menu teams columns-3').find_all('a')

        links = []
        for column in columns:
                links.append(column.get('href').split('/')[-2])

        return links


def parse_players(team_id:str,compId:str):

        patternURL = f'https://org.infobasket.su/Widget/TeamRoster/{team_id}?compId={compId}&format=json&lang=ru'
        print(patternURL)
        response = requests.get(patternURL).json()
        """PatternPLayers = {
        TeamID:str,
        Players: [(PlayerID,F,I,F_ENG,I_ENG,Birthday,PlayerRole,PlayerNumber,Country,Height,Weight)]
        }
        """
        print(response)
        res = {
                'TeamID': response['TeamID'],
                'TeamName': response['TeamName']['CompTeamNameRu'],
                'TeamName_Eng': response['TeamName']['CompTeamNameEn'],
                'Players': [],
                'Coaches':[]
        }
        for player in response['Players']:
                res['Players'].append((player["PersonInfo"]['PersonID'],player["PersonInfo"]['PersonLastNameRu'],
                               player["PersonInfo"]['PersonFirstNameRu'],
                               player["PersonInfo"]['PersonLastNameEn'],player["PersonInfo"]['PersonFirstNameEn'],
                               player["PersonInfo"]['PersonBirth'],player["Position"],
                               player['PlayerNumber'],player['CountryName'],player['Height'],player['Weight']))
        try:
                for player in response["Coaches"]:
                        res['Coaches'].append((
                                player["PersonInfo"]['PersonID'], player["PersonInfo"]['PersonLastNameRu'],
                                player["PersonInfo"]['PersonFirstNameRu'], player["PersonInfo"]['PersonLastNameEn'],
                                player["PersonInfo"]['PersonFirstNameEn'],player["PersonInfo"]['PersonBirth'],'Тренер',
                                -999, player['CountryName'], 0, 0)
                        )

        except:
                print(traceback.format_exc())
        return res





def parse_coach(team_id:str,compId:str):
        patternURL = f'https://org.infobasket.su/Widget/TeamRoster/{team_id}?compId={compId}&format=json&lang=ru'
        print(patternURL)
        response = requests.get(patternURL).json()
        """PatternPLayers = {
        TeamID:str,
        Players: [(PlayerID,F,I,F_ENG,I_ENG,Birthday,PlayerRole,PlayerNumber,Country,Height,Weight)]
        }
        """
        print(response)
        res = {
                'TeamID': response['TeamID'],
                'TeamName': response['TeamName']['CompTeamNameRu'],
                'TeamName_Eng': response['TeamName']['CompTeamNameEn'],
                'Players': []
        }
        for player in response['Players']:
                res['Players'].append((player["PersonInfo"]['PersonID'], player["PersonInfo"]['PersonLastNameRu'],
                                       player["PersonInfo"]['PersonFirstNameRu'],
                                       player["PersonInfo"]['PersonLastNameEn'],
                                       player["PersonInfo"]['PersonFirstNameEn'],
                                       player["PersonInfo"]['PersonBirth'], player["Position"],
                                       player['PlayerNumber'], player['CountryName'], player['Height'],
                                       player['Weight']))

        return res





def get_team_id(url:str):
        urls = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        res = soup.find('div',class_='wrap-bottom').find('div',class_='general-fot').find_all('li')[3].find_all('a')
        for i in res:
                try:
                        q = urls.append(i.get('href').split('/')[2].split('?')[0])
                except:
                        pass
        return urls




def parse_league_team(league_id:str):
        response  = requests.get(f'https://org.infobasket.su/Widget/CompTeamResults/{league_id}?format=json')

        return response.json()

# leagues = []
# config = configparser.ConfigParser()
# config.read('settings.ini')
# for key in config['League']:
#     leagues.append(config['League'][key])




# res = parse_league_team('42911')
# for i in res:
#       #  print(i)
#         # Инфа для вставки в Teams
#         TeamID = i['TeamID']
#         TeamName = i['CompTeamName']['CompTeamShortNameRu']
#         TeamNameEng = i['CompTeamName']['CompTeamNameEn']
#         print(TeamID,TeamName,TeamNameEng)
#
#         # Инфа для вставки в турнирку
#         item = (i['Place'], i['CompTeamName']['CompTeamShortNameRu'], i['Standings']['StandingGame'],
#                 i['Standings']['StandingWin'], i['Standings']['StandingLose'],
#                 i['Standings']['VictoryPercent'],
#                 str(i['Standings']['StandingGoalPlus']) + '/' + str(i['Standings']['StandingGoalMinus']),
#                 i['Standings']['StandingGoalPlus'] - i['Standings']['StandingGoalMinus'],
#                 round(i['Standings']['StandingGoalPlus'] / i['Standings']['StandingGoalMinus'], 2))
#         print(item)
