import numpy as np
from scipy import signal
import audioop
from struct import *

#------------------------------------------------------------------------------
# Convert PyAudio byte array into int16 array for scipy
#------------------------------------------------------------------------------
def bytes2ints(frame):
    count = len(frame)/2
    format = "%dh"%(count)
    shorts = unpack( format, frame )
	return shorts

#------------------------------------------------------------------------------
# Calculates full FFT but only inspects high bins
#------------------------------------------------------------------------------
def fullFft(v,threshold):

	fs = 44.1e3
	N  = len(v)
	print('-------------------------------------------------------')
	print('Length of input array = {}'.format(N))
	print('Type: {}'.format(type(v)))
	print('The array: {}'.format(v))
	print('-------------------------------------------------------')
	# int_values = [x for x in v]
	# int_values = int(v.encode('hex'), 16)
	# int_values = v.hex
	int_values = bytes2ints(v)
	print('Length of int array = {}'.format(len(int_values)))
	print('Type: {}'.format(type(int_values)))
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

