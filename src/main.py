import numpy as np
from graphics import *
import matplotlib.pyplot as plt
import csv
import os
import sys
import scipy
from scipy.linalg import lstsq
from sklearn.metrics import mean_squared_error

paramsDir="../stats/params.txt"
toolsDir="../tools"
playerStatsScript=toolsDir + "/obtenerStatsJugadores.sh"
teamStatsScript=toolsDir + "/obtenerStatsEquipos.sh"
opponentTeamStatsDir="../estadisticasOponentes/statsOponentes"
miscTeamStatsDir="../estadisticasMiscelanias/statsMisc"
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
        self.opponent = []
        self.misc = []
        self.number = 0
        self.longName = ""

    def getStats(self, numbers):
        return [self.stats[n] for n in numbers]

    def getOpponent(self, numbers):
        return [self.opponent[n] for n in numbers]

    def getMisc(self, numbers):
        return [self.misc[n] for n in numbers]

    def __str__(self):
     return "name: " + str(self.name) + ", longName: " + str(self.longName) + ", number: " + str(self.number) + ", year: " + str(self.year) + ", winRate: " + str(self.winRate) + ", stats: " + str(self.stats) + ", opponent: " + str(self.opponent) + ", misc: " + str(self.misc)

class PlayerStats:
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
    return players

def buildTeamStatsFromParams():
    fo = open(paramsDir, "r")
    line = fo.readline()
    fo.close()
    startEnd = [int(x) for x in line.split(" ")]
    years = range(startEnd[0], startEnd[1]+1)
    i = -1
    teamsWithStats = []
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
                teamsWithStats.append(team)
    i = -1  
    teamsWithOpStats = []
    with open(opponentTeamStatsDir, 'rb') as csvfile:
        teamOpponentStats = csv.reader(csvfile, delimiter=',')
        for row in teamOpponentStats:
            if (row[0]=="Rk"):
                i = i+1
            else:
                team = TeamStats()
                team.year = years[i]
                team.name, team.number = findName(row[1], team.year)
                team.longName = row[1]
                team.opponent = [ float(x) for x in row[2:] ]
                teamsWithOpStats.append(team)
    i = -1  
    teamsWithMiscStats = []
    with open(miscTeamStatsDir, 'rb') as csvfile:
        teamMiscStats = csv.reader(csvfile, delimiter=',')
        for row in teamMiscStats:
            if (row[0]=="Rk"):
                i = i+1
            else:
                team = TeamStats()
                team.year = years[i]
                team.name, team.number = findName(row[1], team.year)
                team.longName = row[1]
                team.misc = [ float(x) for x in row[2:22] ]
                team.misc.append(float(row[23]))
                teamsWithMiscStats.append(team)
    for t in teamsWithStats:
        for t1 in teamsWithOpStats:
            if (t1.year == t.year and t1.name == t.name):
                t.opponent = t1.opponent
                break
        for t2 in teamsWithMiscStats:
            if (t2.year == t.year and t2.name == t.name):
                t.misc = t2.misc
                #print t
                break
#    for t in teamsWithStats:
#        if (len(t.misc)==0 or len(t.opponent)==0):
#            print "OJO"
    for team in teamsWithStats:
        with open(winRateDir+"/leagues_NBA_"+str(team.year)+"_winrate.csv", 'rb') as csvfile:
            winRateStats = csv.reader(csvfile, delimiter=',')
            for row in winRateStats:
                if (int(row[0]) == team.number):
                    team.winRate = float(row[1])
                    break
    return teamsWithStats

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

def filterStats(teamsStats, statsToUse, opponentStatsToUse, miscStatsToUse):
    for t in teamsStats:
        if len(statsToUse) != 0:
            t.stats = t.getStats(statsToUse)
        if len(opponentStatsToUse) != 0:
            t.opponent = t.getOpponent(opponentStatsToUse)
        if len(miscStatsToUse) != 0:
            t.misc = t.getMisc(miscStatsToUse)


def cmlGrado1(teamsStats):
    stats = [ x.stats + x.opponent + x.misc for x in teamsStats]
    winRates = [ x.winRate for x in teamsStats]
    A = np.vstack(stats)
    #print A
    #print winRates
    coeficients = np.linalg.lstsq(A, winRates)[0]
    return coeficients

def mse(coeficients, teamsStats):
    predictedWinRates = [ predict(teamStat, coeficients) for teamStat in teamsStats ]
    actualWinRates = [ teamStat.winRate for teamStat in teamsStats ]
    #print max((np.asarray(predictedWinRates) - np.asarray(actualWinRates)) * (np.asarray(predictedWinRates) - np.asarray(actualWinRates)))
    return mean_squared_error(actualWinRates, predictedWinRates)

def predict(team, coeficients):
    return np.dot((team.stats + team.opponent + team.misc), coeficients)

def predictTeam(preTeam, statss, opponents, miscs, s_coeficients, o_coeficients, m_coeficients, w_coeficients):
    team = TeamStats()
    team.year = preTeam.year + 1
    team.name, team.number = preTeam.name, preTeam.number
    team.longName = preTeam.longName
    team.stats = predict(statss, s_coeficients)
    team.opponent = predict(opponents, o_coeficients)
    team.misc = predict(miscs, m_coeficients)
    team.winRate = predict(stats, w_coeficients)

def acumularListas(teamsActuales, teamsAnteriores):
    teamsAnteriores.sort(key = lambda x: x.year)
    for teamActual in teamsActuales:
        for teamAnterior in teamsAnteriores:
            if (teamAnterior.name == teamActual.name):
                teamActual.stats = teamActual.stats + teamAnterior.stats
                teamActual.opponent = teamActual.opponent + teamAnterior.opponent
                teamActual.misc = teamActual.misc + teamAnterior.misc

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
    #print m,c
    plt.plot(x, y, 'o', label='Original data', markersize=10)
    plt.plot(x, m*x + c, 'r', label='Fitted line')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    #print findName("PhoenixSuns", 2016)
    #print team.getStats([1,2,3])
    
    teams = buildTeamStatsFromParams()
    teamsAnteriores = [x for x in teams if(2012 <= x.year <= 2014)]
    teamsActuales = [x for x in teams if(x.year == 2015)]
    acumularListas(teamsActuales, teamsAnteriores)
    #filterStats(teams, [4, 7, 10, 14, 22, 23])
    #filterStats(v, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])6
    #filterStats(teams, [4, 7, 10, 22, 23, 2, 5, 15], [4, 10, 2, 17, 22, 23], [1, 2, 3, 5, 6, 7, 11, 12, 16])
    #for t in teams:
    #    t.stats[3] = t.stats[3]**3
    #for t in teams:
    #    t.stats = [x **3 for x in t.stats]
    #normalizarStats(teams)
    coeficients = cmlGrado1(teamsActuales)
    #print coeficients
    print mse(coeficients, teamsActuales)
    #print coeficients
    #graficarMetricas(teams)
    graficarAproximacion(teamsActuales, coeficients)
    #team = buildTeamStatsFromParams()[0]
    #print team.getStats([1,2,3])
    #coeficients = cmlGrado1(teams)
    #print mse(coeficients, teams)
    #buildPlayerStatsFromParams()
