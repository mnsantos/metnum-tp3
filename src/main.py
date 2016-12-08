import numpy as np
from graphics import *
from reader import *
import matplotlib.pyplot as plt
import os
import sys
import scipy
from scipy.linalg import lstsq
from sklearn.metrics import mean_squared_error
import copy
from collections import defaultdict

def filterStats(teamsStats, statsToUse, opponentStatsToUse, miscStatsToUse):
    for t in teamsStats:
        if len(statsToUse) != None:
            t.stats = t.getStats(statsToUse)
        if len(opponentStatsToUse) != None:
            t.opponent = t.getOpponent(opponentStatsToUse)
        if len(miscStatsToUse) != None:
            t.misc = t.getMisc(miscStatsToUse)

def filterStatsPlayer(playerStats, statsToUse):
    for t in playerStats:
        if len(statsToUse) != None:
            t.stats = t.getStats(statsToUse)

def cmlGrado1(teamsStats):
    #print len(teamsStats)
    stats = [ x.stats + x.opponent + x.misc for x in teamsStats]
    winRates = [ x.winRate for x in teamsStats]

    A = np.vstack(stats)
    #print A
    #print winRates
    coeficients = np.linalg.lstsq(A, winRates)[0]
    return coeficients

def mse(coeficients, teamsActuales, teamsFuturos):
    predictedWinRates = [ predict(team, coeficients) for team in teamsActuales ]
    actualWinRates = [ team.winRate for team in teamsFuturos ]
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

def filtrarTeamsPorYears(teamsAnteriores, years):
    filtrados = []
    for team in teamsAnteriores:
        apariciones = 0
        for team2 in teamsAnteriores:
            if team.name == team2.name:
                apariciones += 1
        if apariciones == years:
            filtrados.append(team)
    return filtrados

def filtrarTeamsPorNombres(teamsAnteriores, teamsActuales):
    filtradosAnteriores = []
    filtradosActuales = []
    for team in teamsAnteriores:
        for team2 in teamsActuales:
            if team.name == team2.name:
                filtradosAnteriores.append(team)
    for team in teamsActuales:
        for team2 in teamsAnteriores:
            if team.name == team2.name:
                filtradosActuales.append(team)
    return filtradosAnteriores, filtradosActuales

def crossvalidation_por_equipo(teams, years):
    MSE = []
    cantidad_bloques_a_testear = int((2016-1987) / years)
    tamanio_bloque = years
    for actual_a_testear in range(1987 + tamanio_bloque, 2017):
        teams_local = copy.deepcopy(teams)
        teamsAnteriores = []
        teamsActuales = []
        teamsFuturos = []
        inicio_periodo_a_estudiar = actual_a_testear - tamanio_bloque
        fin_periodo_a_estudiar = actual_a_testear - 1
        teamsAnteriores = [x for x in teams_local if(inicio_periodo_a_estudiar <= x.year <= fin_periodo_a_estudiar-1)]
        #teamsAnteriores = filtrarTeamsPorYears(teamsAnteriores, years-1)
        teamsActuales = [x for x in teams_local if(x.year == fin_periodo_a_estudiar)]
        teamsFuturos = [x for x in teams_local if(x.year == actual_a_testear)]
        teamsFuturos, teamsActuales = filtrarTeamsPorNombres(teamsFuturos, teamsActuales)
        coeficients = cmlGrado1(teamsAnteriores)
        year_mse = mse(coeficients, teamsActuales, teamsFuturos)
        if year_mse > 1:
            print actual_a_testear, coeficients
            graficarPrediccion(teamsActuales, teamsFuturos, coeficients)
        else:
            MSE.append(year_mse)
    #return MSE
    return np.average(MSE)

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
    teams = read()
    #filterStats(teams, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [6, 7])
    #MSE = crossvalidation_por_equipo(teams, 3)
    #print MSE

    #Aca el copipaste de arriba pero para players
    players = [];
    for team in teams:
        filterStatsPlayer(team.players,[17,19,20,21,22,23]);
        for player in team.players:
            player.stats.append(team.winRate)
        players = players+team.players
    #MSE = crossvalidation_por_jugador(players,3)
    #print MSE
