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
	for team in teams:
		wr.append(team.winRate)
		wr_pred.append(predict(team, coeficients))
	plt.plot(wr, 'r')
	plt.plot(wr_pred, 'b')
	plt.show()
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
		sts[i].append(team.stats[i])

	for i in xrange(1,len(sts)):
		print i
		plt.plot(wr, 'r')
		plt.plot(sts[i])
		plt.show()

	plt.plot(wr, 'r')
	plt.plot(sts[4], 'k')
	plt.plot(sts[10], 'b')
	plt.plot(sts[23], 'g')
	plt.plot(sts[20], 'c')
	plt.show()

def normalizarStats(teams):
	minStats = np.zeros(len(teams[0].stats))
	minStats[:] = teams[0].stats
	maxStats = np.zeros(len(teams[0].stats))
	maxStats[:] = teams[0].stats
	#print 'minStats: ', minStats
	#print 'maxStats: ', maxStats
	for team in teams:
		for i in xrange(0,len(team.stats)):
			stat = team.stats[i]
			if stat < minStats[i]:
				minStats[i] = stat
			if stat > maxStats[i]:
				maxStats[i] = stat
	#print 'minStats: ', minStats
	#print 'maxStats: ', maxStats
	for team in teams:
		for i in xrange(0,len(team.stats)):
			team.stats[i] = ((team.stats[i] - minStats[i]) / (maxStats[i] - minStats[i]))
			#team.stats[i] = (team.stats[i]) / (maxStats[i])
			#print team

def sortByWinRate(teams):
	teams.sort(key = lambda x: x.winRate)