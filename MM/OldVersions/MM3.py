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
		note = struct.pack('iffi', pitch, time, 1, 75)	#set .5 to d for complex timing
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
	bprog = Bass(4, noteNums)

	#Melody Progression
	melody = Melody(4, noteNums)	

	#Percussuion Track
	percussion = PercussionTrack()
	
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
		for var in bprog:
			note = struct.unpack('iff', var)
			MyMIDI.addNote(track, channel, note[0]-12, note[1]+ j*4, note[2], 75)
	
	#melody
	for j in range(0,4):	
		for var in melody:
			note = struct.unpack('iff', var)
			MyMIDI.addNote(track+1, channel+1, note[0], note[1]+ j*4, note[2], 100)
	
	#percussion
	for j in range(0,4):
		for var in percussion:
			note = struct.unpack('iff', var)
			MyMIDI.addNote(track+2, channel+9, note[0], note[1]+ j*4, note[2], 75)

	#save as
	with open("song" + str(songNum) + ".mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)

	return [tempo]

def newSong2(songNum):
	tempo	= random.randint(90, 150)	  # In BPM
	volume	 = 100	# 0-127, as per the MIDI standard
	#notes = deque(['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'])
	noteNums = deque([57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68])
	tkey = random.randint(0,11)
	noteNums.rotate(tkey)
	nprog = []
	
	ALLTRACKS = []

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
	ALLTARCKS.append(Bass(4, noteNums))
	#Melody Progression
	ALLTRACKS.append(Melody(4, noteNums))	
	#Percussuion Track
	ALLTRACKS.append(PercussionTrack())
	
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
	
	for T in ALLTRACKS:
		for j in range(0,4):
			for var in ALLTRACKS[j]:
				note = struct.unpack('iffi', var)
				MyMIDI.addNote(track, channel, note[0], note[1]+ j*4, note[2], note[3])

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