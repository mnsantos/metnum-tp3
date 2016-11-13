import numpy as np


def crossValidation(TSs, WRs):

	for x in range(0,len(TSs)):
		# TS = [ ts  for ts in TSs not in [TSs[x]]]
		# WR = [ wr  for wr in WRs not in [WRs[x]]]
		TS = []
		WR = []
		testTS = TSs[x]
		testWR = WRs[x]		
		#print testTS
		
		for ts in TSs:
			if ts != testTS:
				if(len(TS) == 0):
					TS = ts
				else:
					TS = np.concatenate((TS, ts), axis=0)
		for wr in WRs:
			if wr != testWR:
				if(len(WR) == 0):
					WR = wr
				else:
					WR = np.concatenate((WR, wr), axis=0)
		coeficients = np.linalg.lstsq(TS, WR)[0]
#		A = [[1,100],[1,4]]
#		B = [[3,9],[7,0]]

#		TS = np.concatenate((TS, B), axis=0)		
		#print coeficients
		
		expected = np.dot(testTS,coeficients)
		diferencia = expected - testWR
		mse = np.dot(diferencia , diferencia) / len(diferencia)
		print mse
		
		

