from team import Team
import csv
import os
import sys
from player import Player

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
fourFactorsDir="../stats/fourFactors/fourFactors_"
perDir="../stats/playerEfficiencyRate/per_"

def read():
    teams = buildTeamsFromFiles()
    players = buildPlayersFromFiles()
    merge(teams, players)
    readFourFactorsData(teams)
    readPerData(teams)
    return teams

def buildTeamsFromFiles():
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
                team = Team()
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
                team = Team()
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
                team = Team()
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

def buildPlayersFromFiles():
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
                player = Player()
                player.year = years[i]
                player.name = row[1]
                player.position = row[2]
                player.age = row[3]
                player.team = row[4]
                player.stats = [ float(x) for x in row[5:] ]
                players.append(player)
    return players

def merge(teams, players):
    i = 0
    for player in players:
        for team in teams:
            if (player.team == team.name and player.year == team.year):
                i = i+1
                team.players.append(player)
                break
    if not(i == len(players)):
        "WARN: Hay jugadores para los que no se encontro equipo"

def readFourFactorsData(teams):
    for t in teams:
        with open(fourFactorsDir+str(t.year)+".txt", 'rb') as csvfile:
            fourFactorsStats = csv.reader(csvfile, delimiter=',')
            for row in fourFactorsStats:
                if t.longName == row[0]:
                    t.fourFactors = float(row[1])

def readPerData(teams):
    for t in teams:
        with open(perDir+str(t.year)+".txt", 'rb') as csvfile:
            perStats = csv.reader(csvfile, delimiter=',')
            for row in perStats:
                if t.number == int(row[0]):
                    t.per = float(row[1])


