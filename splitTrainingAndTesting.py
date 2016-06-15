from random import shuffle
import csv
import sys

try:
	sys.argv[1]
	sys.argv[2]
	sys.argv[3]
except:
	print "Error: takes three arguments. \nex: splitTrainingAndTesting.py training_and_testing_fa.csv training_fa.csv testing_fa.csv"

allData = []
trainingData = []
testingData = []

inputObject = open(sys.argv[1])
csvReader = csv.reader(inputObject)
for line in csvReader:
	allData.append(line)
shuffle(allData)


trainingCutoff = int(len(allData)*0.75)

count = 0
for line in allData:
	if count < trainingCutoff:
		trainingData.append(line)
	else:
		testingData.append(line)
	count += 1

trainingOutput = open(sys.argv[2], 'wb')
trainingCSV = csv.writer(trainingOutput)
trainingCSV.writerows(trainingData)

testingOutput = open(sys.argv[3], 'wb')
testingCSV = csv.writer(testingOutput)
testingCSV.writerows(testingData)



