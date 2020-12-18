"""
Created on Mon Sep 16 17:53:05 2019
@author: KClause
"""
import random
import sys
import struct
from datetime import date
from midiutil import MIDIFile
from collections import deque

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

def newSong(songNum):
	tempo	= random.randint(50,90)	  # In BPM
	volume	 = 100	# 0-127, as per the MIDI standard
	#notes = deque(['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'])
	noteNums = deque([57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68])
	tkey = random.randint(0,11)
	noteNums.rotate(tkey)
	nprog = []

	#Notes in the Key
	majmin = random.randint(0,1)
	if (majmin == 1):
		noteNums.remove(noteNums[10])
		noteNums.remove(noteNums[8])
	else:
		noteNums.remove(noteNums[11])
		noteNums.remove(noteNums[9])
	noteNums.remove(noteNums[6])
	if (majmin == 1):
		noteNums.remove(noteNums[3])
		majmin = "maj"
	else:
		noteNums.remove(noteNums[4])
		majmin = "min"
	noteNums.remove(noteNums[1])

	notestr = ""

	for c in noteNums:
		notestr = notestr + str(c) + " "

	#Bass Progression
	nList = [0,1,2,3]
	if(majmin == "maj"):
		r = random.randint(0,6)
		nList[0] = r
		nprog.append(noteNums[r])
		bProg = str(noteNums[r]) + " "
		for x in range(3):
			newr = nextRandomChord(majmin, r)
			bProg = bProg + str(noteNums[newr]) + " "
			nprog.append(noteNums[newr] - 12)
			nList[x+1] = newr
			r = newr
	else:
		r = random.randint(0,6)
		nList[0] = r
		bProg = str(noteNums[r]) + " "
		nprog.append(noteNums[r])
		for x in range(3):
			newr = nextRandomChord(majmin, r)
			bProg = bProg + str(noteNums[newr]) + " "
			nprog.append(noteNums[newr] - 12)
			nList[x+1] = newr
			r = newr	

	#Melody Progression
	melProg = [None] * 16
	melTime = [None] * 16
	melDur = [None] * 16
	noteNums = list(noteNums)
	time = 0
	dur = 0.25
	r = 1
	i = 0
	f = 16
	while i < f:
		if r==0:
			f -= 1
			melProg.pop(i)
			melTime.pop(i)
			melDur.pop(i)
		try:
			melProg[i] = noteNums[random.randint(0,6)]
			
			melTime[i] = time
			
			r = random.randint(0,1)
			if r==1:
				melDur[i] = dur
				time = time + melDur[i]			
			if r==0:
				melDur[i] = dur+dur
				time = time + melDur[i]
				
			i += 1
		except:
			i += 1			

	#Percussuion Track
	if i%2 == 0:
		percussTrack = [35,55,35,55]
	if i%2 == 1:
		percussTrack = [35,38,35,38]

	#MIDI Creation
	track	= 0
	channel	 = 0	#piano 0, bass 1, percussion 9
	time	 = 0	# In beats
	duration = 1	# In beats
	
	#track settings
	MyMIDI = MIDIFile(10)  # MIDIFile(num tracks in song)
	MyMIDI.addProgramChange(0, 0, 0, 33)
	MyMIDI.addProgramChange(0, 1, 0, 80)
	MyMIDI.addProgramChange(0, 9, 0, 91)
	MyMIDI.addTempo(track, time, tempo)
	
	#bass
	for j in range(0,4):#number of measures
		for i, pitch in enumerate(nprog):
			MyMIDI.addNote(track, channel, pitch-12, (time+j*len(nprog)) + i, duration, 75)
	
	time = 0
	#melody
	for j in range(0,4):	
		for i, pitch in enumerate(melProg):
			MyMIDI.addNote(track+1, channel+1, pitch, melTime[i] + j*len(nprog), melDur[i], 100)
	
	time = 0
	#percussion
	for j in range(0,4):
		for i, pitch in enumerate(percussTrack):
			beat = (time+j*len(percussTrack)) + i
			MyMIDI.addNote(track+2, channel+9, pitch, beat, duration, 50)







	#save as
	with open("song" + str(songNum) + ".mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)

	return [tempo, melProg, bProg]
	
def PROGRAM():
	lib_file = open("songList.txt", "w")
	lib_file.write("Keaton Clause\n" + str(date.today()))
	runs = sys.argv[1]
	
	for i in range(int(runs)):
		[tempo, melProg, bProg] = newSong(i)
		lib_file.write("\n\n<song" + str(i) + ">\ntempo: " + str(tempo) + "\npiano: ")
		for e in melProg:
			lib_file.write(str(e) + " ")
		lib_file.write("\nbass: ")
		for e in bProg:
			lib_file.write(str(e))
		lib_file.write("\n")
	
	print("Done!")
	
PROGRAM()