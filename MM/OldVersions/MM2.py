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
	tempo	= random.randint(90, 150)	  # In BPM
	volume	 = 100	# 0-127, as per the MIDI standard
	#notes = deque(['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'])
	noteNums = deque([57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68])
	tkey = random.randint(0,11)
	noteNums.rotate(tkey)
	nprog = []

	#Notes in the Key
	#majmin = random.randint(0,1)
	majmin = 1 #EVERYTHING IS MAJOR FOR NOW
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
		for x in range(3):
			newr = nextRandomChord(majmin, r)
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
	melody = []
	noteNums = list(noteNums)
	time = 0
	r = 1
	i = 0
	while time < len(nprog):		
		pitch = noteNums[random.randint(0,6)]		
		r = random.randint(0,2)
		if r==0:
			d = 0.25		
		if r==1:
			d = 0.5
		if r==2:
			d = 1
		note = struct.pack('iff', pitch, time, d)
		melody.append(note)
		time = time + d
		i += 1		

	#Percussuion Track
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
	while time < len(nprog):
		for hit, d in zip(pH, pD):
			newbeat = struct.pack('iff', hit, time, d)
			percussion.append(newbeat)
			time = time + d
	
	#MIDI Creation
	track	= 0
	channel	 = 0	#piano 0, bass 1, percussion 9
	time	 = 0	# In beats
	duration = 1	# In beats
	
	#track settings
	MyMIDI = MIDIFile(10)  # MIDIFile(num tracks in song)
	#random melody instrument
	instMel = [1, 7, 10, 26]
	instBass = [1, 4, 5, 33, 34, 38, 39]
	MyMIDI.addProgramChange(0, 0, 0, random.choice(instBass))
	MyMIDI.addProgramChange(0, 1, 0, random.choice(instMel))
	MyMIDI.addProgramChange(0, 9, 0, 91)
	MyMIDI.addTempo(track, time, tempo)
	
	#bass
	for j in range(0,4):#number of measures
		for i, pitch in enumerate(nprog):
			MyMIDI.addNote(track, channel, pitch-12, (time+j*len(nprog)) + i, .5, 75)
	
	#melody
	for j in range(0,4):	
		for var in melody:
			note = struct.unpack('iff', var)
			MyMIDI.addNote(track+1, channel+1, note[0], note[1]+ j*len(nprog), note[2], 100)
	
	#percussion
	for j in range(0,4):
		for var in percussion:
			note = struct.unpack('iff', var)
			MyMIDI.addNote(track+2, channel+9, note[0], note[1]+ j*len(nprog), note[2], 75)


	#save as
	with open("song" + str(songNum) + ".mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)

	return [tempo]

def PROGRAM():
	lib_file = open("songList.txt", "w")
	lib_file.write("Keaton Clause\n" + str(date.today()))
	runs = sys.argv[1]
	
	for i in range(int(runs)):
		tempo = newSong(i)
		lib_file.write("\n\n<song" + str(i) + ">\ntempo: " + str(tempo))
	print("Done!")
	
PROGRAM()