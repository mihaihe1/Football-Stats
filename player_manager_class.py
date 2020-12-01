class Person:

    def __init__(self, name, age, nationality):
        self.name = name
        self.age = age
        self.nationality = nationality

goalkeeperPosition = ["GK"]
defenderPositions = ["DF", "FB", "LB", "RB", "CB"]
midfielderPositions = ["MF", "DM", "CM", "LM", "RM", "WM"]
attackerPositions = ["FW", "LW", "RW", "AM"]

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
        for i in position:
            if i in goalkeeperPosition:
                return True

    @staticmethod
    def isDefender(position):
        for i in position:
            if i in defenderPositions:
                return True

    @staticmethod
    def isMidfielder(position):
        for i in position:
            if i in midfielderPositions:
                return True

    @staticmethod
    def isAttacker(position):
        for i in position:
            if i in attackerPositions:
                return True


class Manager(Person):

    def __init__(self, name, age, nationality, club, debut):
        super().__init__(name, age, nationality)
        self.club = club
        self.debut = debut