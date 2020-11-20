from bs4 import BeautifulSoup
from future.moves import tkinter
from tkinter import *
from tkinter import ttk
# from tkinter.ttk import *
import requests

goalkeeperPosition = ["GK"]
defenderPositions = ["DF", "FB", "LB", "RB", "CB"]
midfielderPositions = ["MF", "DM", "CM", "LM", "RM", "WM"]
attackerPositions = ["FW", "LW", "RW", "AM"]

fgDict = {"Leicester City":"#1C51AE", "Tottenham":"#0B105F",
          "Liverpool":"#DB2846", "Southampton":"#DF0025",
          "Chelsea":"#2D1DC6", "Aston Villa":"#7D74CD",
          "Everton":"#4639B7", "Crystal Palace":"#2F239C",
          "Wolves":"#B7AC0C", "Manchester City":"#6E9AC6",
          "Arsenal":"#EE0303", "West Ham":"#7A2B2B",
          "Newcastle Utd":"#B5B0B0", "Manchester Utd":"#E91717",
          "Leeds United":"#E8F70B", "Brighton":"#0B81F7",
          "Fulham":"#232A30", "West Brom":"#194F84",
          "Burnely":"#E0E95C", "Sheffield Utd":"#DF1D1D"}


class Person:

    def __init__(self, name, age, nationality):
        self.name = name
        self.age = age
        self.nationality = nationality


class Player(Person):

    def __init__(self, name, age, nationality, squadName, minutesPlayed, goals, assists, positions=None):
        super().__init__(name, age, nationality)
        self.squadName = squadName
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

    def __init__(self, name, age, nationality, club, debut):
        super().__init__(name, age, nationality)
        self.club = club
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


playersList = []
managerList = []

sourceManager = requests.get("https://www.thesackrace.com/managers/premier-league").text
soupManager = BeautifulSoup(sourceManager, 'lxml')
divManager = soupManager.find_all('div', attrs={'class': 'container'})[4]
#print(divManager)
div2 = divManager.find('div', attrs={'class': 'breaking-news'})
#print(div2.prettify())
div3 = div2.find('div', attrs={'id': 'premier-league'})
#print(div3)
rowsManager = div3.find_all('div', attrs={'class': 'job-man'})
#print(rowsManager)

for j in range(len(rowsManager)):
    club = rowsManager[j].find('h2').text
    if(club.split()[0] == "Tottenham"):
        club = "Tottenham"
    if(len(club.split()) > 1):
        if(club.split()[1] == "United" and club.split()[0] != "Leeds"):
            clubcopy = club.split()
            clubcopy[1] = "Utd"
            club = " ".join(clubcopy)
    
    if(len(club.split()) > 2):
        if(club.split()[2] == "United"):
            club = "West Ham"
    if(club == "West Bromwich Albion"):
        club = "West Brom"
    if(club == "Brighton & Hove Albion"):
        club = "Brighton"
    if(club == "Wolverhampton Wanderers"):
        club = "Wolves"

    managerName = rowsManager[j].find('h1').text
    paragraphs = rowsManager[j].find_all('p')
    parAge = paragraphs[0].text.split()[1]
    parTime = paragraphs[1].text.split(':')[1].lstrip()
    managerList.append(Manager(managerName, parAge, "ENG", club, parTime))


def printPlayers():
    for obj in playersList:
        print(obj.name, obj.age, obj.nationality, obj.minutesPlayed, obj.goals, obj.positions)


def printManagers():
    for obj in managerList:
        print(obj.name, obj.age, obj.nationality, obj.club, obj.debut)


def printTable():
    for obj in squadList:
        print(obj.currentRank, obj.name, obj.wins, obj.losses, obj.goalsFor, obj.points, sep=' ')

printManagers()
# printPlayers()
# printTable()
root = Tk()

test = Label(root, text="Select a team and then press the button to show more info", width=50, height=10)
test.pack()
arrow = Label(root, text="|")
arrow.pack()
arrow2 = Label(root, text="|")
arrow2.pack()
arrow3 = Label(root, text="|")
arrow3.pack()
arrow4 = Label(root, text="V")
arrow4.pack()

# entry = Entry(root, width=20)
# entry.pack()

def getManager(name):
    for obj in managerList:
        if(obj.club == name):
            return obj

def createWindow():
    currentItem = my_tree.focus()
    squadName = my_tree.item(currentItem)['values'][1]
    newWindow = Toplevel(root)
    newWindow.geometry("1000x1000+300+300")
    title = Label(newWindow, text=squadName, font='times 24 bold underline', fg=fgDict[squadName])
    title.pack()
    manager = getManager(squadName)
    managerTitle = Label(newWindow, text="Manager: " + manager.name + "    Age: " + manager.age + "   Debut: " + manager.debut, font='bold')
    managerTitle.pack()
    style2 = ttk.Style()
    style2.configure('Treeview', rowheight=70)
    tree_frame2 = Frame(newWindow)
    tree_frame2.pack(pady=20)
    tree_scroll2 = Scrollbar(tree_frame2)
    tree_scroll2.pack(side = RIGHT, fill=Y)

    my_tree2 = ttk.Treeview(tree_frame2, yscrollcommand=tree_scroll2.set)

    tree_scroll2.config(command=my_tree2.yview)
    my_tree2['columns'] = ("Name", "Age", "Nationality", "MinutesPlayed", "Goals", "Assists", "Positions")
    my_tree2.column("#0", width=50)
    my_tree2.column("Name", width=200, minwidth=25)
    my_tree2.column("Age", anchor=CENTER, width=40)
    my_tree2.column("Nationality", anchor=CENTER, width=100)
    my_tree2.column("MinutesPlayed", anchor=CENTER, width=130)
    my_tree2.column("Goals", anchor=CENTER, width=50)
    my_tree2.column("Assists", anchor=CENTER, width=60)
    my_tree2.column("Positions", anchor=W, width=100)

    my_tree2.heading("Name", text="Name", anchor=W)
    my_tree2.heading("Age", text="Age", anchor=CENTER)
    my_tree2.heading("Nationality", text="Nationality", anchor=CENTER)
    my_tree2.heading("MinutesPlayed", text="Minutes Played", anchor=CENTER)
    my_tree2.heading("Goals", text="Goals", anchor=CENTER)
    my_tree2.heading("Assists", text="Assists", anchor=CENTER)
    my_tree2.heading("Positions", text="Positions", anchor=W)

    for obj in squadList:
        if obj.name == squadName:
            sourceSquad = requests.get(obj.link).text
            soupSquad = BeautifulSoup(sourceSquad, 'lxml')
            tbodySquad = soupSquad.find('tbody')
            rowsSquad = tbodySquad.find_all('tr')
            count = 0
            for i in range(len(rowsSquad)):
                playerName = rowsSquad[i].th.a.text
                pA = rowsSquad[i].find('td', attrs={'data-stat': 'age'}).text.split('-')
                if(len(pA) == 1):
                    playerAge = "?"
                else:
                    playerAge = int(pA[0])
                playerNationality = rowsSquad[i].find('td', attrs={'data-stat': 'nationality'}).a.span.text.split()[1]
                playerMP = rowsSquad[i].find('td', attrs={'data-stat': 'minutes'}).text
                if playerMP == "":
                    playerMP = 0
                playerGoals = rowsSquad[i].find('td', attrs={'data-stat': 'goals'}).text
                if len(playerGoals) == 0:
                    playerGoals = 0
                playerAssists = rowsSquad[i].find('td', attrs={'data-stat': 'assists'}).text
                if playerAssists == "":
                    playerAssists = 0
                playerPositions = rowsSquad[i].find('td', attrs={'data-stat': 'position'}).text.split(",")

                # playersList.append(Player(playerName, playerAge, playerNationality, playerSquad, playerMP, playerGoals, playerAssists,
                #                         playerPositions))
                my_tree2.insert(parent='', index='end', iid=count, text='', values=(playerName, playerAge, playerNationality, playerMP,
                                                                    playerGoals, playerAssists, playerPositions))
                count = count+1
            break
    ##########################################        
    tree = my_tree2.get_children()
    my_tree2.focus(tree[3])
    my_tree2.selection_set(tree[3])
    ##########################################
    my_tree2.pack()


button = Button(root, command=createWindow)
button.pack()

root.title('Football Standings')
root.geometry("1000x1000+600+600")

style = ttk.Style()
style.configure('Treeview', rowheight=70)

tree_frame = Frame(root)
tree_frame.pack(pady=20)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side = RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)

tree_scroll.config(command=my_tree.yview)

my_tree['columns'] = ("Rank", "Name", "MatchesPlayed", "Wins", "Draws", "Losses", "GoalsFor", "GoalsAgainst", "Points")

my_tree.winfo_geometry()

my_tree.column("#0", width=100)
my_tree.column("Rank", width=50, minwidth=25)
my_tree.column("Name", anchor=W, width=130)
my_tree.column("MatchesPlayed", anchor=CENTER, width=130)
my_tree.column("Wins", anchor=W, width=50)
my_tree.column("Draws", anchor=W, width=50)
my_tree.column("Losses", anchor=W, width=60)
my_tree.column("GoalsFor", anchor=W, width=100)
my_tree.column("GoalsAgainst", anchor=W, width=120)
my_tree.column("Points", anchor=W, width=100)


my_tree.heading("Rank", text="Rank", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("MatchesPlayed", text="Matches Played", anchor=CENTER)
my_tree.heading("Wins", text="Wins", anchor=W)
my_tree.heading("Draws", text="Draws", anchor=W)
my_tree.heading("Losses", text="Losses", anchor=W)
my_tree.heading("GoalsFor", text="Goals For", anchor=W)
my_tree.heading("GoalsAgainst", text="Goals Against", anchor=W)
my_tree.heading("Points", text="Points", anchor=W)

imgList = []
for obj in squadList:
    name = obj.name.lower().split()
    if len(name) == 2:
        name2 = "_".join(name)
    else:
        name2 = name[0]
    path = "resources/"+str(name2)+".png"
    img = tkinter.PhotoImage(file=path)
    imgList.append(img)


count = 0
for obj in squadList:
    my_tree.insert(parent='', index='end', iid=count, text='', image=imgList[count], values=(obj.currentRank, obj.name, obj.matchesPlayed,
                                                                    obj.wins, obj.draws, obj.losses, obj.goalsFor,
                                                                    obj.goalsAgainst, obj.points))
    count += 1

my_tree.pack()
root.mainloop()