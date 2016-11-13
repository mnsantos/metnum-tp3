import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys
from sklearn.metrics import mean_squared_error

paramsDir="../stats/params.txt"
toolsDir="../tools"
playerStatsScript=toolsDir + "/obtenerStatsJugadores.sh"
teamStatsScript=toolsDir + "/obtenerStatsEquipos.sh"
teamStatsDir="../estadisticasEquipos/teamStats"
playerStatsDir="../estadisticasJugadores/playerStats"
abreviaturasDir="../stats/abreviaturas"
equiposDir="../stats/equipos"
winRateDir="../stats/winrate"

class TeamStats:
    def __init__(self):
        self.year = 0
        self.winRate = 0
        self.name = ""
        self.stats = []
        self.number = 0
        self.longName = ""

    def __str__(self):
     return "name: " + str(self.name) + ", longName: " + str(self.longName) + ", number: " + str(self.number) + ", year: " + str(self.year) + ", winRate: " + str(self.winRate) + ", stats: " + str(self.stats)

class PlayerStats:
    def __init__(self):
        self.year = 0
        self.team = ""
        self.age = 0
        self.name = ""
        self.position = ""
        self.stats = []

    def __str__(self):
        return "name: " + str(self.name) + ", age: " + str(self.age) + ", position: " + str(self.position) + ", team: " + str(self.team) + ", year: " + str(self.year) + ", stats: " + str(self.stats)

def buildPlayerStatsFromParams():
    fo = open(paramsDir, "r")
    line = fo.readline()
    fo.close()
    startEnd = [int(x) for x in line.split(" ")]
    years = range(startEnd[0], startEnd[1]+1)
    i = -1
    players = []
    with open(playerStatsDir, 'rb') as csvfile:
        playerStats = csv.reader(csvfile, delimiter=',')
        for row in playerStats:
            if (row[0]=="Rk"):
                i = i+1
            else:
                player = PlayerStats()
                player.year = years[i]
                player.name = row[1]
                player.position = row[2]
                player.age = row[3]
                player.team = row[4]
                player.stats = [ float(x) for x in row[5:] ]
                players.append(player)
                print player
    return players

def buildTeamStatsFromParams():
    fo = open(paramsDir, "r")
    line = fo.readline()
    fo.close()
    startEnd = [int(x) for x in line.split(" ")]
    years = range(startEnd[0], startEnd[1]+1)
    i = -1
    teams = []
    with open(teamStatsDir, 'rb') as csvfile:
        teamStats = csv.reader(csvfile, delimiter=',')
        for row in teamStats:
            if (row[0]=="Rk"):
                i = i+1
            else:
                team = TeamStats()
                team.year = years[i]
                team.name, team.number = findName(row[1], team.year)
                team.longName = row[1]
                team.stats = [ float(x) for x in row[2:] ]
                teams.append(team)
    for team in teams:
        with open(winRateDir+"/leagues_NBA_"+str(team.year)+"_winrate.csv", 'rb') as csvfile:
            winRateStats = csv.reader(csvfile, delimiter=',')
            for row in winRateStats:
                if (int(row[0]) == team.number):
                    team.winRate = float(row[1])
                    print team
                    break
    return teams

def findName(longName, year):
    teamNumber = 0
    with open(equiposDir+"/equipos_"+str(year)+".txt", 'rb') as csvfile:
        equipos = csv.reader(csvfile, delimiter=',')
        for row in equipos:
            if (row[1]==longName):
                teamNumber = int(row[0])
    with open(abreviaturasDir+"/abreviaturas_"+str(year)+".txt", 'rb') as csvfile:
        abreviaturas = csv.reader(csvfile, delimiter=',')
        for row in abreviaturas:
            if (row[0]==str(teamNumber)):
                return row[1], teamNumber

def cmlGrado1(teamsStats):
    stats = [ x.stats for x in teamsStats]
    winRates = [ x.winRate for x in teamsStats]
    A = np.vstack(stats)
    coeficients = np.linalg.lstsq(A, winRates)[0]
    return coeficients

def mse(coeficients, teamStats):
    predictedWinRates = [ sum(teamsStat.stats * coeficients) for teamsStat in teamStats ]
    actualWinRates = [ teamsStat.winRate for teamStat in teamStats ]
    return mean_squared_error(actualWinRates, predictedWinRates)



# def cmlGrado1(teamsStats, factorsToUse):
#     stats = []
#     winRates = []
#     for teamStat in teamsStats:
#         teamsFactorsToUse = [ value for key,value in teamStat.stats if key in factorsToUse]
#         winRates.append(teamStat.winRate)
#         stats.append(teamsFactorsToUse)
#     A = np.vstack(stats).T
#     coeficients = np.linalg.lstsq(A, winRates)[0]
#     return coeficients

def test():
    x = np.array([0, 1, 2, 3])
    y = np.array([-1, 0.2, 0.9, 2.1])
    A = np.vstack((x, np.ones(len(x)))).T
    m, c = np.linalg.lstsq(A, y)[0]
    print m,c
    plt.plot(x, y, 'o', label='Original data', markersize=10)
    plt.plot(x, m*x + c, 'r', label='Fitted line')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    #print findName("PhoenixSuns", 2016)
    #teams = buildTeamStatsFromParams()
    #coeficients = cmlGrado1(teams)
    #print mse(coeficients, teams)
    buildPlayerStatsFromParams()
