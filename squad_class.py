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