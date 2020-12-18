#Note generator functions for MM
import random
import sys
import struct
from midiutil import MIDIFile
from collections import deque

def MarkhovTxt(intxt, strlen):
	fin = open(intxt, "r")
	fulltext = fin.readlines()

	wordList = []
	wordProbs = []
	AllProbs = []

	for line in fulltext:
		xL = line.split()
		for i in range(0,len(xL)):
			if xL[i] not in wordList:
				wordList.append(xL[i])

	for w in wordList:
		wordProbs = []
		for line in fulltext:
			xL = line.split()
			for i in range(0,len(xL)):
				if(i+1 < len(xL)):
					if(xL[i] == w):
						wordProbs.append(xL[i+1])
		AllProbs.append(wordProbs)

	newChain = []
	newChain.append(wordList[rnd.randint(0,len(wordList))])
	for i in range(1, strlen):
		ind = wordList.index(newChain[i-1])
		ML = AllProbs[ind]
		if(ML != []):
			Mword = ML[rnd.randint(0,len(ML)-1)]
			newChain.append(Mword)
		else:
			newChain.append(wordList[rnd.randint(0,len(wordList))])

	fin.close()
	return newChain

def nextRandomChord(majmin, r):
	if(majmin == "maj"):
		if(r==0):
			newr = random.randint(0,6)
		if(r==1):
			q = random.randint(0,1)
			if(q == 0):
				newr = 4
			else:
				newr = 6
		if(r==2):
			newr = 5
		if(r==3):
			q = random.randint(0,1)
			if(q == 0):
				newr = 4
			else:
				newr = 6
		if(r==4):
			newr = 0
		if(r==5):
			q = random.randint(0,1)
			if(q == 0):
				newr = 0
			else:
				newr = 2
		if(r==6):
			q = random.randint(0,1)
			if(q == 0):
				newr = 0
			else:
				newr = 2	  
	
	if(majmin == "min"):
		if(r==0):
			newr = random.randint(0,6)
		if(r==1):
			q = random.randint(0,1)
			if(q == 0):
				newr = 4
			else:
				newr = 6
		if(r==2):
			newr = 5
		if(r==3):
			q = random.randint(0,1)
			if(q == 0):
				newr = 4
			else:
				newr = 6
		if(r==4):
			newr = 0
		if(r==5):
			q = random.randint(0,1)
			if(q == 0):
				newr = 0
			else:
				newr = 2
		if(r==6):
			q = random.randint(0,1)
			if(q == 0):
				newr = 0
			else:
				newr = 2	  
	return newr

def Bass(m, noteNums):
	bprog = []
	noteL = list(noteNums)
	time = 0
	while time < m:		
		pitch = noteL[random.randint(0,6)]		
		r = random.randint(0,2)
		if r==0:
			d = 0.25		
		if r==1:
			d = 0.5
		if r==2:
			d = 1
		note = struct.pack('iffi', pitch-12, time, 1, 75)	#set .5 to d for complex timing
		bprog.append(note)
		time = time + 1
	return bprog

def Melody(m, noteNums):
	melody = []
	noteL = list(noteNums)
	time = 0
	while time < m:		
		pitch = noteL[random.randint(0,6)]		
		r = random.randint(0,2)
		if r==0:
			d = 0.25		
		if r==1:
			d = 0.5
		if r==2:
			d = 1
		note = struct.pack('iffi', pitch, time, d, 100)
		melody.append(note)
		time = time + d	
	return melody

def Bass2(m, noteNums):
	bprog = []
	bpack = []
	noteL = list(noteNums)
	time = 0
	while time < m:		
		pitch = noteL[random.randint(0,6)]		
		note = struct.pack('iffi', pitch-12, time, 1, 75)	#set .5 to d for complex timing
		bpack.append(note)
		bprog.append(pitch)
		time = time + 1
	return [bpack, bprog]

def RhythmG(m, noteNums, bprog):
	bprog = []
	noteL = list(noteNums)
	time = 0
	while time < m:
		pitch = noteL[random.randint(0,6)]		
		note = struct.pack('iffi', pitch, time, 1, 75)	#set .5 to d for complex timing
		bprog.append(note)
		note = struct.pack('iffi', pitch+7, time, 1, 75)	#set .5 to d for complex timing
		bprog.append(note)
		time = time + 1
	return bprog

def Riff(m, noteNums, bprog):
	riff = []
	noteL = list(noteNums)
	time = 0	
	
	while time < m:	
		#RIFF TYPE

		#Key Scaling
		
		#Single Chord Play
		
		#Two Chord Play
		
		#Random
		pitch = noteL[random.randint(0,6)]	

		r = random.randint(0,4)
		d = 0.25 * r
		note = struct.pack('iffi', pitch, time, d, 100)
		riff.append(note)
		time = time + d
	return riff

def MarkhovRiff():
	MRiff = []
	return MRiff
	
def PercussionTrack():
	percussion = []
	k = random.choice([35, 60])
	c = random.choice([38, 55, 71])
	r = random.randint(0,2)
	if r == 0:
		pH = [k, c,  k,  k, c]
		pD = [1, 1, .5, .5, 1]
	if r == 1:
		pH = [k, c, k, c]
		pD = [1, 1, 1, 1]
	if r == 2:
		pH = [k,  c, k,  k, c]
		pD = [1, .5, 1, .5, 1]	
			
	time = 0
	while time < 4:
		for hit, d in zip(pH, pD):
			newbeat = struct.pack('iffi', hit, time, d, 75)
			percussion.append(newbeat)
			time = time + d
	return percussion

#TODO WRITE TEST FUNCTION FOR ADVBUILD
def AdvTrackBuild(BL, RiffK, CR, VR):
	AT = []
	struc =[]
	nBL = []
	nRiffK = []
	nCR = [] 
	nVR = []
	#Decide on structure
	#Riff 0 Verse 1 Bridge 2 Chorus 3 
	songLen = random.randint(5,10)
	for i in range(songLen):
		struc.append(random.randint(0,4))

	#[pitch time dur vol]
	m = 0
	for p in struc:
		m += 1
		if(p is 0):
			for var in BL:
				note = struct.unpack('iffi', var)
				note = list(note)
				note[1] *= m
				note = struct.pack('iffi', note[0], note[1], note[2], note[3])
				nBL.append(note)
			for var in RiffK:
				note = struct.unpack('iffi', var)
				note = list(note)
				note[1] *= m
				note = struct.pack('iffi', note[0], note[1], note[2], note[3])
				nRiffK.append(note)

		if(p is 1):
			for var in BL:
				note = struct.unpack('iffi', var)
				note = list(note)
				note[1] *= m
				note = struct.pack('iffi', note[0], note[1], note[2], note[3])
				nBL.append(note)
			for var in VR:
				note = struct.unpack('iffi', var)
				note = list(note)
				note[1] *= m
				note = struct.pack('iffi', note[0], note[1], note[2], note[3])
				nVR.append(note)

		if(p is 2):
			for var in BL:
				note = struct.unpack('iffi', var)
				note = list(note)
				note[1] *= m
				note = struct.pack('iffi', note[0], note[1], note[2], note[3])
				nBL.append(note)

		if(p is 3):
			for var in BL:
				note = struct.unpack('iffi', var)
				note = list(note)
				note[1] *= m
				note = struct.pack('iffi', note[0], note[1], note[2], note[3])
				nBL.append(note)
			for var in CR:
				note = struct.unpack('iffi', var)
				note = list(note)
				note[1] *= m
				note = struct.pack('iffi', note[0], note[1], note[2], note[3])
				nCR.append(note)

	AT.append(nBL)
	AT.append(nRiffK)
	AT.append(nCR)
	AT.append(nVR)

	return AT