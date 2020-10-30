from bs4 import BeautifulSoup
import requests

goalkeeperPosition = ["GK"]
defenderPositions = ["DF", "FB", "LB", "RB", "CB"]
midfielderPositions = ["MF", "DM", "CM", "LM", "RM", "WM"]
attackerPositions = ["FW", "LW", "RW", "AM"]


class Person:

    def __init__(self, name, age, nationality):
        self.name = name
        self.age = age
        self.nationality = nationality


class Player(Person):

    def __init__(self, name, age, nationality, minutesPlayed, goals, assists, positions=None):
        super().__init__(name, age, nationality)
        self.minutesPlayed = minutesPlayed
        self.goals = goals
        self.assists = assists
        self.positions = positions
        #self. pastTeams = pastTeams

    @staticmethod
    def isGoalkeeper(position):
        return position in goalkeeperPosition

    @staticmethod
    def isDefender(position):
        return position in defenderPositions

    @staticmethod
    def isMidfielder(position):
        return position in midfielderPositions

    @staticmethod
    def isAttacker(position):
        return position in attackerPositions


class Manager(Person):

    def __init__(self, name, age, nationality, debut):
        super().__init__(name, age, nationality)
        self.debut = debut


class Squad:

    link = []

    def __init__(self, currentRank, name, matchesPlayed, wins, draws, losses, goalsFor, goalsAgainst, points):
        self.currentRank = currentRank
        self.name = name
        self.matchesPlayed = matchesPlayed
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goalsFor = goalsFor
        self.goalsAgainst = goalsAgainst
        self.points = points
        #self. players = players

    def setLink(self, link):
        self.link = link

sourceStandings = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text

soupStandings = BeautifulSoup(sourceStandings, 'lxml')
#print(soup.prettify())
tbodyStandings = soupStandings.find('tbody')
rowsStandings = tbodyStandings.find_all('tr')

'''
for i in range(0,30):
    print('-',end='')
print('-')
'''

squadList = []

for i in range(len(rowsStandings)):
    rank = i+1
    name = rowsStandings[i].td.a.text
    mp = rowsStandings[i].find('td', attrs={'data-stat': 'games'}).text
    wins = rowsStandings[i].find('td', attrs={'data-stat': 'wins'}).text
    draws = rowsStandings[i].find('td', attrs={'data-stat': 'draws'}).text
    losses = rowsStandings[i].find('td', attrs={'data-stat': 'losses'}).text
    gf = rowsStandings[i].find('td', attrs={'data-stat': 'goals_for'}).text
    ga = rowsStandings[i].find('td', attrs={'data-stat': 'goals_against'}).text
    pts = rowsStandings[i].find('td', attrs={'data-stat': 'points'}).text
    squadList.append(Squad(rank, name, mp, wins, draws, losses, gf, ga, pts))
    link = rowsStandings[i].find('a', href=True)
    squadList[i].setLink('https://fbref.com'+link['href'])
    #print(rowsStandings[i].td.a.text + ": " + wins.text + " W")

def printTable():
    for obj in squadList:
        print(obj.currentRank, obj.name, obj.wins, obj.losses, obj.goalsFor, obj.points, sep=' ')

playersList = []

search = "Liverpool"
for obj in squadList:
    if obj.name == search:
        sourceSquad = requests.get(obj.link).text
        soupSquad = BeautifulSoup(sourceSquad, 'lxml')
        tbodySquad = soupSquad.find('tbody')
        rowsSquad = tbodySquad.find_all('tr')
        for i in range(len(rowsSquad)):
            playerName = rowsSquad[i].th.a.text
            playerAge = int(rowsSquad[i].find('td', attrs={'data-stat': 'age'}).text.split('-')[0])
            playerNationality = rowsSquad[i].find('td', attrs={'data-stat': 'nationality'}).a.span.text.split()[1]
            playerMP = rowsSquad[i].find('td', attrs={'data-stat': 'minutes'}).text
            playerGoals = rowsSquad[i].find('td', attrs={'data-stat': 'goals'}).text
            if len(playerGoals) == 0:
                playerGoals = 0
            playerAssists = rowsSquad[i].find('td', attrs={'data-stat': 'assists'}).text
            playerPositions = rowsSquad[i].find('td', attrs={'data-stat': 'position'}).text.split(",")
            playersList.append(Player(playerName, playerAge, playerNationality, playerMP, playerGoals, playerAssists,
                                      playerPositions))

def printPlayers():
    for obj in playersList:
        print(obj.name, obj.age, obj.nationality, obj.minutesPlayed, obj.goals, obj.positions)

printPlayers()

#test test test