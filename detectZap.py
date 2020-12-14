import numpy as np
from scipy import signal
import audioop

#------------------------------------------------------------------------------
# Calculates full FFT but only inspects high bins
#------------------------------------------------------------------------------
def fullFft(v,threshold):

	fs = 44.1e3
	N  = len(v)
	print('-------------------------------------------------------')
	print('Length of input array = {}'.format(N))
	print('The array: {}'.format(v))
	print('-------------------------------------------------------')
	int_values = [x for x in v]
	print('Length of int array = {}'.format(len(int_values)))
	print('The array: {}'.format(int_values))
	print('-------------------------------------------------------')



	f, Pxx_den = signal.periodogram(v, fs)

	myAvg = sum(Pxx_den[344:500])/len(Pxx_den[344:500])
	# print('mean value = ', myAvg)
	# print('threshold  = ', threshold)
	
	print("myAvg: {}".format(myAvg))

	if myAvg>threshold:
		return 1
	else:
		return 0

#------------------------------------------------------------------------------
# Just a test; detects hand claps or anything loud
#------------------------------------------------------------------------------
def justRms(data, threshold):
	rms   = audioop.rms(data, 2)  # shows volume
	if (rms >= threshold):
		print("RMS level detected: {}".format(rms))
		return 1
	else:
		return 0

