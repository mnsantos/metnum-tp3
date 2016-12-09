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
    for p in playerStats:
        if len(statsToUse) != None:
            p.stats = p.getStats(statsToUse)

def cmlGrado1Players(teams):
    #print len(teamsStats)
    playersStats = [ player.stats for team in teams for player in team.players]
    winRates = [ team.winRate for team in teams for player in team.players]

    A = np.vstack(playersStats)
    #print A
    #print winRates
    coeficients = np.linalg.lstsq(A, winRates)[0]
    return coeficients

def cmlGrado1(teamsStats):
    #print len(teamsStats)
    stats = [ x.stats + x.opponent + x.misc for x in teamsStats]
    winRates = [ x.winRate for x in teamsStats]

    A = np.vstack(stats)
    #print A
    #print winRates
    coeficients = np.linalg.lstsq(A, winRates)[0]
    return coeficients

def cmlGrado1verTeams(teams, offset):
    stats = []
    winRates = []
    for team in teams:
        for team2 in teams:
            if team.name == team2.name and team.year+offset == team2.year:
                stats.append(team.stats + team.opponent + team.misc)
                winRates.append(team2.winRate)
    A = np.vstack(stats)
    coeficients = np.linalg.lstsq(A, winRates)[0]
    return coeficients

def cmlGrado1verPlavers(teams, offset):
    players = []
    winRates = []
    for team in teams:
        for team2 in teams:
            if team.year+offset == team2.year:
                for player in team.players:
                    for player2 in team2.players:
                        players.append(player.stats)
                        winRates.append(team2.winRate)
                        break
    A = np.vstack(players)
    coeficients = np.linalg.lstsq(A, winRates)[0]
    return coeficients

def mse(coeficients, teamsActuales):
    predictedWinRates = [ predict(team, coeficients) for team in teamsActuales ]
    actualWinRates = [ team.winRate for team in teamsActuales ]
    #print max((np.asarray(predictedWinRates) - np.asarray(actualWinRates)) * (np.asarray(predictedWinRates) - np.asarray(actualWinRates)))
    return mean_squared_error(actualWinRates, predictedWinRates)

def msePlayers(coeficients, teamsActuales):
    predictedWinRates = [ predictPlayers(team, coeficients) for team in teamsActuales ]
    actualWinRates = [ team.winRate for team in teamsActuales ]
    #print predictedWinRates
    #print actualWinRates
    #print max((np.asarray(predictedWinRates) - np.asarray(actualWinRates)) * (np.asarray(predictedWinRates) - np.asarray(actualWinRates)))
    return mean_squared_error(actualWinRates, predictedWinRates)

def predict(team, coeficients):
    return np.dot((team.stats + team.opponent + team.misc), coeficients)

def predictPlayers(team, coeficients):
    wr_players = []
    for player in team.players:
        wr_player = np.dot(player.stats, coeficients)
        if wr_player > 0.2 and wr_player < 0.9:
            wr_players.append(wr_player)
    return np.average(wr_players)

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
        teamsAnteriores = []
        teamsActuales = []
        teamsFuturos = []
        inicio_periodo_a_estudiar = actual_a_testear - tamanio_bloque
        fin_periodo_a_estudiar = actual_a_testear - 1
        teamsAnteriores = [x for x in teams if(inicio_periodo_a_estudiar <= x.year < fin_periodo_a_estudiar)]
        teamsActuales = [x for x in teams if(x.year == fin_periodo_a_estudiar)]
        #teamsFuturos = [x for x in teams if(x.year == actual_a_testear)]
        #teamsFuturos, teamsActuales = filtrarTeamsPorNombres(teamsFuturos, teamsActuales)
        coeficients = cmlGrado1(teamsAnteriores)
        year_mse = mse(coeficients, teamsActuales)
        if year_mse > 1:
            #print actual_a_testear
            one = 1
        else:
            actualWinRates = [team.winRate for team in teamsActuales]
            predictedWinRates = [predict(team, coeficients) for team in teamsActuales]
            graficar_listas(teamsFuturos, predictedWinRates, actualWinRates)
            #scatter_listas(teamsFuturos, predictedWinRates, actualWinRates)
        print year_mse
        MSE.append(year_mse)
    return np.average(MSE)

def crossvalidation_por_players(teams, years):
    MSE = []
    cantidad_bloques_a_testear = int((2016-1987) / years)
    tamanio_bloque = years
    for actual_a_testear in range(1987 + tamanio_bloque, 2017):
        teamsAnteriores = []
        teamsActuales = []
        inicio_periodo_a_estudiar = actual_a_testear - tamanio_bloque
        fin_periodo_a_estudiar = actual_a_testear - 1
        teamsAnteriores = [x for x in teams if(inicio_periodo_a_estudiar <= x.year < fin_periodo_a_estudiar)]
        teamsActuales = [x for x in teams if(x.year == fin_periodo_a_estudiar)]
        #teamsFuturos = [x for x in teams if(x.year == actual_a_testear)]
        #teamsFuturos, teamsActuales = filtrarTeamsPorNombres(teamsFuturos, teamsActuales)
        coeficients = cmlGrado1Players(teamsAnteriores)
        year_mse = msePlayers(coeficients, teamsActuales)
        if year_mse > 1:
            #print actual_a_testear
            one = 1
        else:
            actualWinRates = [team.winRate for team in teamsActuales]
            predictedWinRates = [predictPlayers(team, coeficients) for team in teamsActuales]
            graficar_listas(teamsActuales, predictedWinRates, actualWinRates)
            scatter_listas(teamsActuales, predictedWinRates, actualWinRates)
        print year_mse
        MSE.append(year_mse)
    return np.average(MSE)

def obtenerJugadorPromedio(teams):
    # for t in teams:
    #     #print [p.stats for p in t.players]
    #     newPlayers = [p for p in t.players if not(p.stats[0]==0)]
    #     t.players = newPlayers
    
    statsLen = len(teams[0].players[0].stats)
    for t in teams:
        newPlayer = Player()
        for i in range(0,statsLen):
            statsi = []
            for p in t.players:
                #print p.stats
                #print "entre con i" + str(i)
                statsi.append(p.stats[i])
            newStat = np.average(statsi)
            #print newStat
            newPlayer.stats.append(newStat)
        t.players = [newPlayer]

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
    # filterStats(teams, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [], [])
    # #filterStats(teams, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [6, 7])
    # MSE = crossvalidation_por_equipo(teams, 9)
    # print MSE

    teams = [t for t in teams if not(len(t.players)==0)]

    #Aca el copipaste de arriba pero para players
    # for team in teams:
    #     #filterStatsPlayer(team.players,[17,19,20,21,22,23]);
    #     #5 8 11 12 15
    #     filterStatsPlayer(team.players,[2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,24])


    for team in teams:
        #filterStatsPlayer(team.players,[17,19,20,21,22,23]);
        #5 8 11 12 15
        filterStatsPlayer(team.players,[2,3,4,6,7,9,10,13,14,16,17,18,19,20,21,22,23,24])

    obtenerJugadorPromedio(teams)

    MSE = crossvalidation_por_players(teams, 9)
    print MSE
