# detect zaps with a single bin FFT
# code date 20210115

# Contains the following:
# - an initialization function that should be called at startup time.
# - a zap counter function which returns 0 or 1.
# - a sample calculation which you can ignore.

# The counter function expects an audio array of dimension 1024.
# It also expects a threshold which you can figure out by taking some data with and without zaps and see what the FFT amplitude comes out to by uncommenting the print statement.
# This is the fastest possible FFT.   If it isn’t  fast enough, we have no choice but to get faster hardware.
# But if it is fast enough, then more bins can be added to make it more accurate.  How many can be determined by trial and error.

import numpy as np


def initializeArrays():
	global cosinesArray
	global sinesArray
	print('Starting....: Initializing DFT arrays')
	
	dt = 1/44.1e3
	ts = dt * np.arange(0, 1024, 1)
	fz = 12.1e3
	args = 2 * np.pi * fz * ts
	cosinesArray = np.cos(args)
	sinesArray   = np.sin(args)

	print('Completed...: Initializing DFT arrays')



def countZaps(v,threshold):

	print('---- Starting countZaps')
	print('Input data type: {}'.format(v.dtype))
	print('cosinesArray data type: {}'.format(cosinesArray.dtype))
	print('sinesArray data type: {}'.format(sinesArray.dtype))
	print('Input data: {}'.format(v))

	cosineInnerProduct = np.inner(cosinesArray, v)
	sineInnerProduct   = np.inner(sinesArray, v)
	amplitude          = np.sqrt( np.square(cosineInnerProduct) +  np.square(sineInnerProduct) )
	
#	print('amplitude          = ', amplitude)
#	print('threshold          = ', threshold)
	
	if amplitude>threshold:
		return 1
	else:
		return 0
		

###############################################################################
# SAMPLE CALCULATION
###############################################################################

# # pre-compute arrays needed for DFT
# initializeArrays()

# #fileName = 'LoudMusicArray.csv'
# fileName = 'LoudMusicAll.csv'
# print('input file: ', fileName)

# # read in audio data from csv file
# myFile = np.genfromtxt(fileName, delimiter=',')
# print('myFile: ', myFile[20000:20100])

# # partition data into segments of length 1024
# lSeg = 1024
# N    = len(myFile)
# print("N = ", N)

# numSegs = N // lSeg

# print("numSegs: ", numSegs)

# # Create an array of the desired size
# w, h = lSeg, numSegs;
# M = [[0 for x in range(w)] for y in range(h)]

# myLen = len(M)
# print("length(M): ", myLen)

# zapCount = 0
# for segNum in range(h):
# 	start = lSeg * segNum
# 	end   = start + lSeg
# #	print("segNum: ", segNum)
	
# 	segData = myFile[start:end]
# #	print("length segData: ", len(segData))
	
# 	zaps = countZaps(segData,1.0)
# #	print("zaps               = ", zaps)
	
# 	zapCount += zaps
	
# print("final zap count: ", zapCount)







