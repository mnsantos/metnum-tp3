import matplotlib.pyplot as plt
import numpy as np
from main import predict
import sys

#Para mejor visualizacion se espera que la primera lista este ordenada por winRate y la segunda mantenga el orden de la primera.
def graficarAproximacion(teams, coeficients):
	teams.sort(key = lambda x: x.winRate)
	fig = plt.figure()
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	wr = []
	wr_pred = []
	min_wr_pred = 1
	min_wr_pred_i = 0
	max_wr_pred = 0
	max_wr_pred_i = 0
	i = 0
	for team in teams:
		wr.append(team.winRate)
		team_wr_pred = predict(team, coeficients)
		wr_pred.append(team_wr_pred)
		if team_wr_pred < min_wr_pred:
			min_wr_pred = team_wr_pred
			min_wr_pred_i = i
		if team_wr_pred > max_wr_pred:
			max_wr_pred = team_wr_pred
			max_wr_pred_i = i
		i += 1
	plt.plot(wr, 'r')
	plt.plot(wr_pred, 'b')
	plt.show()
	print 'max: ', max_wr_pred
	print teams[max_wr_pred_i]
	print 'min: ', min_wr_pred
	print teams[min_wr_pred_i]
	#plt.savefig('results/'+fname+'.png', format='png')

#Ordena la lista teams por winrate y grafica las metricas para ver si existe correlacion entre los valores
def graficarMetricas(teams):
	fig = plt.figure()
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	teams.sort(key = lambda x: x.winRate)
	wr = []
	sts = [[] for y in range(len(teams[0].stats))]
	normalizarStats(teams)
	for team in teams:
		wr.append(team.winRate)
		for i in xrange(0,len(team.stats)):
			sts[i].append(team.stats[i])

	for i in xrange(0,len(sts)):
		print i
		plt.plot(wr, 'r')
		plt.plot(sts[i], 'b')
		plt.show()


def normalizarStats(teams):
	minStats = np.zeros(len(teams[0].stats))
	minStats[:] = teams[0].stats
	maxStats = np.zeros(len(teams[0].stats))
	maxStats[:] = teams[0].stats
	meanStats = np.zeros(len(teams[0].stats))
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	print 'meanStats: ', meanStats
	for team in teams:
		for i in xrange(0,len(team.stats)):
			stat = team.stats[i]
			if stat < minStats[i]:
				minStats[i] = stat
			if stat > maxStats[i]:
				maxStats[i] = stat
			meanStats[i] += stat/len(teams)
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	print 'meanStats: ', meanStats
	for team in teams:
		for i in xrange(0,len(team.stats)):
			team.stats[i] = ((team.stats[i] - minStats[i]) / (maxStats[i] - minStats[i]))
			media_normalizada = ((meanStats[i] - minStats[i]) / (maxStats[i] - minStats[i]))
			#team.stats[i] = podar(team.stats[i], media_normalizada, 80)
			#team.stats[i] = (team.stats[i]) / (maxStats[i])
			#print team

def podar(stat, mean, perc):
	print stat
	#if stat == 0.0:
	#	stat = mean
	if stat > (mean * 100+perc) / 100:
		stat = (mean * 100+perc) / 100
	if stat < (mean * 100-perc) / 100:
		stat = (mean * 100-perc) / 100
	return stat

def sortByWinRate(teams):
	teams.sort(key = lambda x: x.winRate)