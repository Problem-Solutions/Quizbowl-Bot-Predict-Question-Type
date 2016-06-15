import csv
import sys
import json

try:
	sys.argv[1]
except:
	print "Error: takes one argument. \nex: easyAndMediumTossups.py fa_q_answ_difficulties_JSON.txt"

questionData = []

fileObject = open(sys.argv[1])

for line in fileObject:
	question = json.loads(line)
	tossup = question[0].encode('utf8')
	answerLine = question[1].encode('utf8')
	difficulty = question[2].encode('utf8')

	if difficulty == "M" or difficulty == "E":
		questionData.append([tossup, answerLine])

fileOutput = open('all_tossups_easy_and_medium_fa.csv', 'wb')
csvOutput = csv.writer(fileOutput)
csvOutput.writerows(questionData)



	



