# Author: Paul Hamilton
# Project: Quizbowl Question Analysis
# Task: Predict Question Type
# Umich Unique Name: phamilt
# ----Subject: Fine Arts

import csv
import re
import itertools
import sys
#takes two command line inputs: "processRawQuestions.py inputfile.txt outfile.csv"
#########################################################################################################
# INPUTS: A file of unprocessed Fine Arts questions 													#
# OUTPUTS: A csv file where each row contains a question (as one string) and its answer line 			#
# PURPOSE: Process the raw Fine Arts questions downloaded from quinterest.com and process them into a 	#
#	csv file 																							#
#########################################################################################################

#makes sure you have valid input
try:
	sys.argv[1]
	sys.argv[2]
except:
	print "Error: takes two arguments. \nex: processRawQuestions.py inputfile.txt outputfile.csv"


# Used to remove unnecessary text from a question's answer line
BRACKET_RE = re.compile(r'\[.*')
PARANTHESES_RE = re.compile(r'\(.*')
OR_RE = re.compile(r'\s[oO][rR]\s.*')

tossups = []
with open(sys.argv[1], 'r') as fileInputObject:

	for line in fileInputObject:

		tossup = []
		if (line[0:8] == 'Question'):
			question = line[10:]
			question = question.replace('\n', '')
			tossup.append(question)

		if line[0:6]=='ANSWER':
			answerLine = line[8:]
			answerLine = re.sub(BRACKET_RE, '', answerLine)
			answerLine = re.sub(PARANTHESES_RE, '', answerLine)
			answerLine = re.sub(OR_RE, '', answerLine)
			answerLine = answerLine.replace('\n', '')
			tossup.append(answerLine)

		if len(tossup) > 0:
			tossups.append(tossup)
			
iterableList = iter(tossups)
tossups = zip(iterableList, iterableList)


with open(sys.argv[2], 'wb') as fileOutputObject: #ex: "answer_lines_lit.csv"
	csvWriterObject = csv.writer(fileOutputObject)
	csvWriterObject.writerows(tossups)

print "finished processing raw questions"
