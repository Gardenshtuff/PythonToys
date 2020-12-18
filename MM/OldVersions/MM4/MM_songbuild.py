import random
import sys
import struct
from midiutil import MIDIFile
from collections import deque

from MM_func import *

#used by all song funcs
def WriteToMidi(ALLTRACKS, P, songNum):
	#MIDI Creation
	tempo	= random.randint(90, 150)	  # In BPM
	track	= 0
	ch		 = 0	#piano 0, bass 1, percussion 9
	time	 = 0	# In beats
	#track settings
	MyMIDI = MIDIFile(10)  # MIDIFile(num tracks in song)
	#random melody instrument
	instMel = list(range(1,9))
	instMel.extend(range(17,33))
	instMel.extend(range(41,97))
	instMel.extend(range(105,113))
	instBass = [range(33,41)]
	MyMIDI.addProgramChange(0, 0, 0, random.choice(instBass))
	for i in range(1,9):
		MyMIDI.addProgramChange(0, i, 0, random.choice(instMel))
	MyMIDI.addProgramChange(0, 9, 0, 91)
	MyMIDI.addTempo(track, time, tempo)

	for T in ALLTRACKS:
		for j in range(0,4):
			for var in T:
				note = struct.unpack('iffi', var)
				MyMIDI.addNote(0, ch, note[0], note[1]+ j*4, note[2], note[3])
		ch += 1
		track += 1
		
	for j in range(0,4):
		for var in P:
			note = struct.unpack('iffi', var)
			MyMIDI.addNote(0, 9, note[0], note[1]+ j*4, note[2], note[3])

	#save as
	with open("song" + str(songNum) + ".mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)

def basicSong(songNum):
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
	ALLTRACKS.append(Bass(4, noteNums))
	#Melody Progression
	ALLTRACKS.append(Melody(4, noteNums))	
	#Percussuion Track
	P = PercussionTrack()
	
	WriteToMidi(ALLTRACKS, P, songNum)

def newSong3(songNum, type):
	tempo	= random.randint(90, 150)	  # In BPM
	volume	 = 100	# 0-127, as per the MIDI standard
	#notes = deque(['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'])
	noteNums = deque([57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68])
	tkey = random.randint(0,11)
	noteNums.rotate(tkey)
	nprog = []
	ALLTRACKS = []

	#Bass
	[BL, bprog] = Bass2(4, noteNums)

	#Riff
	if(type is "r"):
		RiffK = Riff(4, noteNums, bprog)
	if(type is "m"):
		RiffK = MarkhovRiff(4, noteNums)
	#Chorus Rhythm
	CR = RhythmG(4, noteNums, bprog)

	#Verse Rhythm
	VR = RhythmG(4, noteNums, bprog)

	#Percussian
	P = PercussionTrack()
	
	#Organize Tracks
	ALLTRACKS = AdvTrackBuild(BL, RiffK, CR, VR)

	WriteToMidi(ALLTRACKS, P, songNum)

def SONGTEST(songNum):
	tempo	= random.randint(90, 150)	  # In BPM
	volume	 = 100	# 0-127, as per the MIDI standard
	#notes = deque(['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'])
	noteNums = deque([57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68])
	tkey = random.randint(0,11)
	noteNums.rotate(tkey)
	nprog = []
	ALLTRACKS = []
	
	BL = Bass(4, noteNums)
	
	RiffK = Melody(4, noteNums)
	CR = Melody(4, noteNums)
	VR = Melody(4, noteNums)
	P = PercussionTrack()
	
	#Organize Tracks
	ALLTRACKS = AdvTrackBuild(BL, RiffK, CR, VR)

	WriteToMidi(ALLTRACKS, P, songNum)


