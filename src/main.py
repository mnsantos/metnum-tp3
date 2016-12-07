import numpy as np
from graphics import *
from reader import *
import matplotlib.pyplot as plt
import os
import sys
import scipy
from scipy.linalg import lstsq
from sklearn.metrics import mean_squared_error

def filterStats(teamsStats, statsToUse, opponentStatsToUse, miscStatsToUse):
    for t in teamsStats:
        if len(statsToUse) != None:
            t.stats = t.getStats(statsToUse)
        if len(opponentStatsToUse) != None:
            t.opponent = t.getOpponent(opponentStatsToUse)
        if len(miscStatsToUse) != None:
            t.misc = t.getMisc(miscStatsToUse)


def cmlGrado1(teamsStats):
    print len(teamsStats)
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
    tamMinimo = 0
    for teamActual in teamsActuales:
        for teamAnterior in teamsAnteriores:
            if (teamAnterior.name == teamActual.name):
                teamActual.stats = teamActual.stats + teamAnterior.stats
                teamActual.opponent = teamActual.opponent + teamAnterior.opponent
                teamActual.misc = teamActual.misc + teamAnterior.misc
        tamListas = (len(teamActual.stats)+len(teamActual.opponent)+len(teamActual.misc))
        if tamMinimo < tamListas:
            tamMinimo = tamListas
    for teamActual in teamsActuales:
        tamListas = (len(teamActual.stats)+len(teamActual.opponent)+len(teamActual.misc))
        if tamListas < tamMinimo:
            teamsActuales.remove(teamActual)
        #else:
            #print len(teamActual.stats)
            #print len(teamActual.opponent)
            #print len(teamActual.misc)
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
    
    teams = read()

    #filterStats(teams, [], [], [6, 7])
    
    # teamsAnteriores = [x for x in teams if(2009 <= x.year <= 2014)]
    # teamsActuales = [x for x in teams if(x.year == 2015)]
    # teamsFuturos = [x for x in teams if(x.year == 2016)]
    # acumularListas(teamsActuales, teamsAnteriores)
    # #filterStats(teams, [4, 7, 10, 14, 22, 23])
    # #filterStats(v, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])6
    # #for t in teams:
    # #    t.stats[3] = t.stats[3]**3
    # #for t in teams:
    # #    t.stats = [x **3 for x in t.stats]
    # #normalizarStats(teams)
    # coeficients = cmlGrado1(teamsActuales)
    # print coeficients
    # print mse(coeficients, teamsActuales)
    # #print coeficients
    # #graficarMetricas(teams)
    # #graficarAproximacion(teamsActuales, coeficients)
    # graficarPrediccion(teamsActuales, teamsFuturos, coeficients)
    #team = buildTeamStatsFromParams()[0]
    #print team.getStats([1,2,3])
    #coeficients = cmlGrado1(teams)
    #print mse(coeficients, teams)
    #buildPlayerStatsFromParams()
