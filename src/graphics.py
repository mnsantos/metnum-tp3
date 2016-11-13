import matplotlib.pyplot as plt
import numpy as np
import sys

#Para mejor visualizacion se espera que la primera lista este ordenada por winRate y la segunda mantenga el orden de la primera.
def graficarAproximacion(teams, esperados):
	fig = plt.figure()
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	wr = []
	for team in teams:
		wr.append(team.winRate)
	plt.plot(wr)
	plt.plot(esperados)
	plt.show()
	#plt.savefig('results/'+fname+'.png', format='png')

#Ordena la lista teams por winrate y grafica las metricas para ver si existe correlacion entre los valores
def graficarMetricas(teams):
	fig = plt.figure()
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	teams.sort(key = lambda x: x.winRate)
	wr = []
	sts = [[] for y in range(len(teams[0].stats))]
	minStats = np.zeros(len(teams[0].stats))
	minStats[:] = teams[0].stats
	maxStats = np.zeros(len(teams[0].stats))
	maxStats[:] = teams[0].stats
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	for team in teams:
		for i in xrange(1,len(team.stats)):
			stat = team.stats[i]
			if stat < minStats[i]:
				minStats[i] = stat
			if stat > maxStats[i]:
				maxStats[i] = stat
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	for team in teams:
		wr.append(team.winRate)
		for i in xrange(1,len(team.stats)):
			team.stats[i] = ((team.stats[i] - minStats[i]) / (maxStats[i] - minStats[i]))
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


def sortByWinRate(teams):
	teams.sort(key = lambda x: x.winRate)