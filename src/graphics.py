import matplotlib.pyplot as plt
import numpy as np
from main import predict
import sys

def graficar_listas(teamsFuturos, predicted_winRates, actual_winRates):
	labels = [team.name for team in teamsFuturos]
	#ffactors = [team.fourFactors for team in teamsFuturos]
	#per = [team.per for team in teamsFuturos]
	plt.plot(actual_winRates, 'ro', label='Winrate real')
	plt.plot(predicted_winRates, 'bs', label='Winrate modelado')
	plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
	plt.xticks(range(0, len(actual_winRates)), labels)	
	plt.margins(0.2)
	plt.show()

def graficar(lista):
	labels = range(2, 28)
	plt.plot(lista, 'r')
	plt.xticks(range(1, len(lista)), labels)
	plt.margins(0.2)
	plt.show()
	plt.close()

def scatter_listas(teamsFuturos, predicted_winRates, actual_winRates):
	labels = [team.name for team in teamsFuturos]
	ffactors = [team.fourFactors for team in teamsFuturos]
	per = [team.per for team in teamsFuturos]
	print "PER:"
	print per
	#plt.xticks(range(1, len(actual_winRates)), labels, rotation='vertical')
	plt.title('ffactors')
	plt.scatter(ffactors, predicted_winRates, c='b', alpha=0.5)
	#plt.scatter(ffactors, actual_winRates, c='r', alpha=0.5)
	for label, x, y in zip(labels, ffactors, predicted_winRates):
		plt.annotate(
		label, 
		xy = (x, y), xytext = (-20, 20),
		textcoords = 'offset points', ha = 'right', va = 'bottom',
		bbox = dict(boxstyle = 'round,pad=0.1', fc = 'yellow', alpha = 0.5),
		arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	# for label, x, y in zip(labels, ffactors, actual_winRates):
		# plt.annotate(
		# label, 
		# xy = (x, y), xytext = (-20, 20),
		# textcoords = 'offset points', ha = 'right', va = 'bottom',
		# bbox = dict(boxstyle = 'round,pad=0.1', fc = 'yellow', alpha = 0.5),
		# arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	plt.margins(0.2)
	plt.show()
	plt.title('per')
	plt.scatter(per, predicted_winRates, c='b', alpha=0.5)
	#plt.scatter(per, actual_winRates, c='r', alpha=0.5)
	for label, x, y in zip(labels, per, predicted_winRates):
		plt.annotate(
		label, 
		xy = (x, y), xytext = (-20, 20),
		textcoords = 'offset points', ha = 'right', va = 'bottom',
		bbox = dict(boxstyle = 'round,pad=0.1', fc = 'yellow', alpha = 0.5),
		arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	# for label, x, y in zip(labels, per, actual_winRates):
	# 	plt.annotate(
	# 	label, 
	# 	xy = (x, y), xytext = (-20, 20),
	# 	textcoords = 'offset points', ha = 'right', va = 'bottom',
	# 	bbox = dict(boxstyle = 'round,pad=0.1', fc = 'yellow', alpha = 0.5),
	# 	arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	plt.margins(0.2)
	plt.show()


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

def graficarPrediccion(teamsActuales, teamsFuturos, coeficients):
	teamsFuturos.sort(key = lambda x: x.winRate)
	fig = plt.figure()
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	wr = []
	wr_pred = []
	labels = []
	for teamFuturo in teamsFuturos:
		found = False
		for teamActual in teamsActuales:
			if teamFuturo.name == teamActual.name:
				teamFuturo.winRatePred = predict(teamActual, coeficients)
				found = True
		if found:
			wr.append(teamFuturo.winRate)
			wr_pred.append(teamFuturo.winRatePred)
			labels.append(teamFuturo.name)

	plt.plot(wr, 'ro')
	plt.xticks(range(1, len(wr)), labels, rotation='vertical')
	plt.plot(wr_pred, 'bs')
	plt.margins(0.2)
	plt.show()



#Ordena la lista teams por winrate y grafica las metricas para ver si existe correlacion entre los valores
def graficarMetricas(teams):
	fig = plt.figure()
	#names = ['fg%vsWinRate', '3p%vsWinRate', '2p%vsWinRate', 'ptsvsWinRate', 'ptsPerGameVsWinRate', 'drbVsWinRate']
	names = ['fg%againstvsWinRate', '2p%againstvsWinRate', 'astvsWinRate','ptsAgainsVsWinRate', 'ptsAgainsPerGameVsWinRate']

	teams.sort(key = lambda x: x.winRate)
	j=0
	#for i in [4, 7, 10, 22, 23, 15]:
	for i in [4, 10, 17, 22, 2]:
		xs = []
		ys = []
		for t in teams:
			plt.xlabel('Estadistica')
			plt.ylabel('WinRate')
			#print t.misc
			#print t.stats[i]
			xs.append(t.opponent[i])
			ys.append(t.winRate)
		plt.plot(xs, ys, 'ro')
		plt.savefig(names[j] + '.png')
		fig.clear()
		j = j+1
	#fig.suptitle('Precision: '+str(precision)+'\ne='+str(e), fontsize=15)
	#teams.sort(key = lambda x: x.winRate)
	# wr = []
	# sts = [[] for y in range(len(teams[0].stats))]
	# opponents = [[] for y in range(len(teams[0].opponent))]
	# miscs = [[] for y in range(len(teams[0].misc))]
	
	#normalizarStats(teams)
	
	# for team in teams:
	# 	wr.append(team.winRate)
	# 	for i in xrange(0,len(team.stats)):
	# 		sts[i].append(team.stats[i])
	# 	for i in xrange(0,len(team.opponent)):
	# 		opponents[i].append(team.opponent[i])
	# 	for i in xrange(0,len(team.misc)):
	# 		miscs[i].append(team.misc[i])

	# for i in xrange(0,len(sts)):
	# 	#print i
	# 	plt.plot(wr, 'r')
	# 	plt.plot(sts[i], 'b')
	# 	plt.show()

	# for i in xrange(0,len(opponents)):
	# 	print i
	# 	plt.plot(wr, 'r')
	# 	plt.plot(opponents[i], 'b')
	# 	plt.show()

	# for i in xrange(0,len(miscs)):
	# 	print i
	# 	plt.plot(wr, 'r')
	# 	plt.plot(miscs[i], 'b')
	# 	plt.show()



def normalizarStats(teams):
	minStats = np.zeros(len(teams[0].stats))
	minStats[:] = teams[0].stats
	maxStats = np.zeros(len(teams[0].stats))
	maxStats[:] = teams[0].stats
	meanStats = np.zeros(len(teams[0].stats))
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	print 'meanStats: ', meanStats
	minOpponent = np.zeros(len(teams[0].opponent))
	minOpponent[:] = teams[0].opponent
	maxOpponent = np.zeros(len(teams[0].opponent))
	maxOpponent[:] = teams[0].opponent
	meanOpponent = np.zeros(len(teams[0].opponent))
	print 'minOpponent: ', minOpponent
	print 'maxOpponent: ', maxOpponent
	print 'meanOpponent: ', meanOpponent
	minMisc = np.zeros(len(teams[0].misc))
	minMisc[:] = teams[0].misc
	maxMisc = np.zeros(len(teams[0].misc))
	maxMisc[:] = teams[0].misc
	meanMisc = np.zeros(len(teams[0].misc))
	print 'minMisc: ', minMisc
	print 'maxMisc: ', maxMisc
	print 'meanMisc: ', meanMisc
	for team in teams:
		for i in xrange(0,len(team.stats)):
			stat = team.stats[i]
			if stat < minStats[i]:
				minStats[i] = stat
			if stat > maxStats[i]:
				maxStats[i] = stat
			meanStats[i] += stat/len(teams)
		for i in xrange(0,len(team.opponent)):
			opponent = team.opponent[i]
			if opponent < minOpponent[i]:
				minOpponent[i] = opponent
			if opponent > maxOpponent[i]:
				maxOpponent[i] = opponent
			meanOpponent[i] += opponent/len(teams)
		for i in xrange(0,len(team.misc)):
			misc = team.misc[i]
			if misc < minMisc[i]:
				minMisc[i] = misc
			if misc > maxMisc[i]:
				maxMisc[i] = misc
			meanMisc[i] += misc/len(teams)
	print 'minStats: ', minStats
	print 'maxStats: ', maxStats
	print 'meanStats: ', meanStats
	print 'minOpponent: ', minOpponent
	print 'maxOpponent: ', maxOpponent
	print 'meanOpponent: ', meanOpponent
	print 'minMisc: ', minMisc
	print 'maxMisc: ', maxMisc
	print 'meanMisc: ', meanMisc
	for team in teams:
		for i in xrange(0,len(team.stats)):
			team.stats[i] = ((team.stats[i] - minStats[i]) / (maxStats[i] - minStats[i]))
			media_normalizada_stats = ((meanStats[i] - minStats[i]) / (maxStats[i] - minStats[i]))
		for i in xrange(0,len(team.opponent)):
			team.opponent[i] = ((team.opponent[i] - minOpponent[i]) / (maxOpponent[i] - minOpponent[i]))
			media_normalizada_opponent = ((meanOpponent[i] - minOpponent[i]) / (maxOpponent[i] - minOpponent[i]))
		for i in xrange(0,len(team.misc)):
			team.misc[i] = ((team.misc[i] - minMisc[i]) / (maxMisc[i] - minMisc[i]))
			media_normalizada_misc = ((meanMisc[i] - minMisc[i]) / (maxMisc[i] - minMisc[i]))
			#team.stats[i] = podar(team.stats[i], media_normalizada, 80)

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