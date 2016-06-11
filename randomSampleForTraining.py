from random import sample
import csv
import sys


questionList=[]
try:
	sys.argv[1]
	sys.argv[2]
except:
	print "Error: takes two arguments. \nex: randomSampleForTraining.py answer_lines_fa.csv training_and_testing_fa.csv"

with open(sys.argv[1],'rb') as infile:
	reader = csv.reader(infile)
	for line in reader:
		question = line[0]
		answerLine = line[1]
		questionList.append([question, answerLine])

trainingTestingSample = sample(questionList,1000)

with open(sys.argv[2],'wb') as outfile:
	writer = csv.writer(outfile)
	writer.writerows(trainingTestingSample)

print "All done"

