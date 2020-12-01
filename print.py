import lists

def printManagers():
    for obj in lists.managerList:
        print(obj.name, obj.age, obj.nationality, obj.club, obj.debut)


def printTable():
    for obj in lists.squadList:
        print(obj.currentRank, obj.name, obj.wins, obj.losses, obj.goalsFor, obj.points, sep=' ')

printManagers()
# printPlayers()
# printTable()