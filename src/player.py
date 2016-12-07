class Player:
    def __init__(self):
        self.year = 0
        self.team = ""
        self.age = 0
        self.name = ""
        self.position = ""
        self.stats = []

    def getStats(self, numbers):
        return [self.stats[n] for n in numbers]

    def __str__(self):
        return "name: " + str(self.name) + ", age: " + str(self.age) + ", position: " + str(self.position) + ", team: " + str(self.team) + ", year: " + str(self.year) + ", stats: " + str(self.stats)