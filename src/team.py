class Team:
    def __init__(self):
        self.year = 0
        self.winRate = 0
        self.winRatePred = 0
        self.name = ""
        self.stats = []
        self.opponent = []
        self.misc = []
        self.number = 0
        self.longName = ""
        self.players = []

    def getStats(self, numbers):
        return [self.stats[n] for n in numbers]

    def getOpponent(self, numbers):
        return [self.opponent[n] for n in numbers]

    def getMisc(self, numbers):
        return [self.misc[n] for n in numbers]

    def __str__(self):
     return "name: " + str(self.name) + ", longName: " + str(self.longName) + ", number: " + str(self.number) + ", year: " + str(self.year) + ", winRate: " + str(self.winRate) + ", stats: " + str(self.stats) + ", opponent: " + str(self.opponent) + ", misc: " + str(self.misc)