# function countZaps
#
# inputs:
# 	1D array of 1500 audio values collected at 48 kHz
#	detection threshold
#
# returns:
#	0 or 1
#
# Method:
# computes average amplitude from 11 kHz to 16 kHz
# and compares it with threshold


import numpy as np
from scipy import signal

def countZaps(v,threshold):

	fs = 48e3
	N  = len(v)
	print('length of input array = ', N)
	
	f, Pxx_den = signal.periodogram(v, fs)

	myAvg = sum(Pxx_den[344:500])/len(Pxx_den[344:500])
	print('mean value = ', myAvg)
	print('threshold  = ', threshold)
	
	if myAvg>threshold:
		return 1
	else:
		return 0