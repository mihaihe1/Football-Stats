from bs4 import BeautifulSoup
from future.moves import tkinter
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
import requests
import player_manager_class as PMC
import squad_class as SC
import lists


root = Tk()

test = Label(root, text="Select a team and then press the button to show more info", width=50, height=5)
test.pack()
arrow = Label(root, text="|")
arrow.pack()
arrow2 = Label(root, text="|")
arrow2.pack()
arrow3 = Label(root, text="|")
arrow3.pack()
arrow4 = Label(root, text="V")
arrow4.pack()

##################### SECOND WINDOW #################################

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

def getManager(name):
    for obj in lists.managerList:
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

    for obj in lists.squadList:
        if obj.name == squadName:
            playersList = []
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

                playersList.append(PMC.Player(playerName, playerAge, playerNationality, squadName, playerMP, playerGoals, playerAssists,
                                         playerPositions))
                my_tree2.insert(parent='', index='end', iid=count, text='', values=(playerName, playerAge, playerNationality, playerMP,
                                                                    playerGoals, playerAssists, playerPositions))
                count = count+1
            break
    
    def selectAttacker():
        att = []
        cnt = 0
        for obj in playersList:
            if obj.isAttacker(obj.positions):
                att.append(cnt)
            cnt += 1
        #tree = my_tree2.get_children()
        #my_tree2.focus(tree[att[0]])
        my_tree2.selection_set(tuple(att))

    def selectMidfielder():
        mid = []
        cnt = 0
        for obj in playersList:
            if obj.isMidfielder(obj.positions):
                mid.append(cnt)
            cnt += 1
        #tree = my_tree2.get_children()
        #my_tree2.focus(tree[att[0]])
        my_tree2.selection_set(tuple(mid))

    def selectDefender():
        dfd = []
        cnt = 0
        for obj in playersList:
            if obj.isDefender(obj.positions):
                dfd.append(cnt)
            cnt += 1
        #tree = my_tree2.get_children()
        #my_tree2.focus(tree[att[0]])
        my_tree2.selection_set(tuple(dfd))
    
    def selectGK():
        gk = []
        cnt = 0
        for obj in playersList:
            if obj.isGoalkeeper(obj.positions):
                gk.append(cnt)
            cnt += 1
        #tree = my_tree2.get_children()
        #my_tree2.focus(tree[att[0]])
        my_tree2.selection_set(tuple(gk))

    def reset():
        my_tree2.selection_set(())
    att = Label(newWindow, text="FILTER PLAYERS", width=15, height=1, bg="#668D9E", font="bold")
    att.pack()
    buttonAtt = Button(newWindow, text="Select Attackers", fg="blue", width=20, command=selectAttacker)
    buttonAtt.pack()
    buttonMid = Button(newWindow, text="Select Midfielders", fg="orange", width=20,command=selectMidfielder)
    buttonMid.pack()
    buttonDef = Button(newWindow, text="Select Defenders", fg="green", width=20, command=selectDefender)
    buttonDef.pack()
    buttonGK = Button(newWindow, text="Select Goalkeepers", fg="#099FDF", width=20, command=selectGK)
    buttonGK.pack()
    buttonRESET = Button(newWindow, text="Reset filter", fg="red", width=10, command=reset)
    buttonRESET.pack()
    
    my_tree2.pack()

################# BACK TO MAIN WINDOW ############################


button = Button(root, command=createWindow)
button.pack()

root.title('Football Standings')
root.geometry("1000x1000+600+600")

theme = ThemedStyle(root)
theme.set_theme("radiance")

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
for obj in lists.squadList:
    name = obj.name.lower().split()
    if len(name) == 2:
        name2 = "_".join(name)
    else:
        name2 = name[0]
    path = "resources/"+str(name2)+".png"
    img = tkinter.PhotoImage(file=path)
    imgList.append(img)


count = 0
for obj in lists.squadList:
    my_tree.insert(parent='', index='end', iid=count, text='', image=imgList[count], values=(obj.currentRank, obj.name, obj.matchesPlayed,
                                                                    obj.wins, obj.draws, obj.losses, obj.goalsFor,
                                                                    obj.goalsAgainst, obj.points))
    count += 1

my_tree.pack()
root.mainloop()