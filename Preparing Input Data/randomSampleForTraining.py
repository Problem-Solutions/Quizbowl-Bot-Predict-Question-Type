from random import sample
import csv
import sys


questionList=[]
try:
	sys.argv[1]
	sys.argv[2]
except:
	print "Error: takes two arguments. \nex: randomSampleForTraining.py answerLines.csv intermediateSample.csv"

with open(sys.argv[1],'rb') as infile:
	reader = csv.reader(infile)
	for line in reader:
		questionList.append(line)
numAnswerLines = len(questionList)
answerLinesList =[]
for x in xrange(1,numAnswerLines):
	temp = [x]
	answerLinesList.extend(temp)



answerLinesSample = sample(answerLinesList,1000)

with open(sys.argv[2],'wb') as outfile:
	writer = csv.writer(outfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for line in answerLinesSample:
		writer.writerow(questionList[line])
print "All done"

