"""
Created on Mon Sep 16 17:53:05 2019
@author: KClause
"""
"""
	Driver for MM functions and unit tests

"""
import random
import sys
import struct
from datetime import date
from midiutil import MIDIFile
from collections import deque

from MM_songbuild import *

numsongs = 0
flag = None
unitTest = ""
marktxt = []

"""
MM.py numSongs testFlag unitTestNum textInput
flags "-u"
unitTestNum "r" "m"
"""
def GetCommandLine():
	L = len(sys.argv)
	if(L > 0):
		global numsongs 
		numsongs = int(sys.argv[1])
	if(L > 2):
		global flag 
		flag = sys.argv[2]
	if(L > 3):
		global unitTest 
		unitTest = sys.argv[3]
	if(unitTest is "m"):
		global marktxt 
		marktxt = MarkhovTxt(sys.argv[4], 4)

def PROGRAM():
	if(flag == None):
		for i in range(numsongs):
			basicSong(i)
	
	if(flag == "TEST"):
		SONGTEST(1)
	
	if(flag == "-u"):
		for i in range(numsongs):
			newSong3(i, unitTest)
	
	print("Done!")
	
GetCommandLine()
PROGRAM()