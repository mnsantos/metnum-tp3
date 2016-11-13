import matplotlib.pyplot as plt
import numpy as np
import sys

#Para mejor visualizacion se espera que la primera lista este ordenada por winRate y la segunda mantenga el orden de la primera.
def graficarAproximacion(resultados, esperados):
	fig = plt.figure()
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	plt.plot(esperados)
	plt.plot(resultados)
	plt.legend(['esperados_calefaccion', 'esperados_refrigeracion', 'resultados_calefaccion', 'resultados_refrigeracion'], loc='upper left')
	plt.show()
	#plt.savefig('results/'+fname+'.png', format='png')

#Ordena la lista teams por winrate y grafica las metricas para ver si existe correlacion entre los valores
def graficarMetricas(teams):
	fig = plt.figure()
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	teams.sort(key = lambda x: x.winRate)
	wr = []
	sts = []
	minStats = np.zeros(len(teams[0].stats))
	minStats[:] = teams[0].stats
	maxStats = np.zeros(len(teams[0].stats))
	maxStats[:] = teams[0].stats
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	for team in teams:
		for i in xrange(0,len(team.stats)):
			stat = team.stats[i]
			if stat < minStats[i]:
				minStats[i] = stat
			if stat > maxStats[i]:
				maxStats[i] = stat
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	for team in teams:
		wr.append(team.winRate)
		for i in xrange(0,len(team.stats)):
			#print minStats[i]
			#print maxStats[i]
			team.stats[i] = ((team.stats[i] - minStats[i]) / (maxStats[i] - minStats[i]))
			#print i
			#print team.stats[i]
			#print stat
			#input = sys.stdin.readline()
		sts.append(team.stats)
	#print 'len(wr): ', len(wr)
	#print 'len(sts): ', len(sts)
	plt.plot(wr, 'r')
	plt.plot(sts)
	#plt.legend(['esperados_calefaccion', 'esperados_refrigeracion', 'resultados_calefaccion', 'resultados_refrigeracion'], loc='upper left')
	plt.show()
	#plt.savefig('results/'+fname+'.png', format='png')

def sortByWinRate(teams):
	teams.sort(key = lambda x: x.winRate)