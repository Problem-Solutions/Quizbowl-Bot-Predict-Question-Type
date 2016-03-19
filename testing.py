# Author: Paul Hamilton
# Project: Quizbowl Question Analysis
# Task: Predict Question Type
# Umich Unique Name: phamilt
# ----Subject: Fine Arts

import csv
import json
import re
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from string import punctuation
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter

#############################################
# STEP 1: Read in data and extract features #
#############################################

#########################################################################################################
# INPUTS: A filename; a list of desired features; the label for the desired question type 				#
# OUTPUTS: A list of tuples, where each tuple contains a dictionary of features and a question label 	#
# PURPOSE: Read in training or testing data, then generate a dictionary of features for each question. 	#
#	The keys of the dictionary are the ngrams used in the question, and the values are the number of 	#
#	times those ngrams occur. Each dictionary is paired with a human-generated label in a tuple. 		#
#########################################################################################################

def read_in_data(filename, desiredFeatures, desiredLabel):

	fileObject = open(filename, 'r')
	csvReaderObject = csv.reader(fileObject)

	header = True
	dictionaryAndLabels = []
	for line in csvReaderObject:

		# Skip header row
		if header == True:
			header = False
			continue
		
		question = line[0]
		label = line[3]
		questionDictionaryAndLabel = extract_features(question, label, desiredLabel, desiredFeatures)
		dictionaryAndLabels.append(questionDictionaryAndLabel)

	return dictionaryAndLabels

#########################################################################################
# INPUTS: An entire question as a string and a human-generated label for that question; #
#	a list of the features desired; the label for the desired question type				#
# OUTPUTS: A tuple containing a dictionary of features and a human-generated label 		# 		
# PURPOSE: Turn a question string into a dictionary of features (ngrams) 				#
#########################################################################################

def extract_features(questionString, questionType, desiredLabel, desiredFeatures):

	# Turn a question string into a list of lemmetized words
	questionList = process_question(questionString)

	includeMonogram = False
	includeBigram = False
	includeTrigram = False

	for feature in desiredFeatures:
		if feature == "monogram":
			includeMonogram = True
		elif feature == "bigram":
			includeBigram = True
		elif feature == "trigram":
			includeTrigram = True

	dictOfNGrams = Counter({})

	dictOfMonograms = Counter(get_monograms(questionList))
	if includeMonogram == True:
		dictOfNGrams = dictOfNGrams + dictOfMonograms

	dictOfBigrams = Counter(get_bigrams(questionList))
	if includeBigram == True:
		dictOfNGrams = dictOfNGrams + dictOfBigrams

	dictOfTrigrams = Counter(get_trigrams(questionList))
	if includeTrigram == True:
		dictOfNGrams = dictOfNGrams + dictOfTrigrams

	newQuestionType = questionType
	if newQuestionType != desiredLabel:
		newQuestionType = "other"

	dictTypeTuple = (dictOfNGrams, newQuestionType)
	return dictTypeTuple

#############################################################
# INPUTS: An entire question as a string 					#
# OUTPUTS: A list of lemmetized words from the question 	#
#############################################################

def process_question(questionString):

	# Remove punctuation from the question and make every character lowercase
	PUNCTUATION_RE = re.compile(r'[^\w\s]')
	questionString = re.sub(PUNCTUATION_RE, '', questionString)
	questionString = questionString.lower()

	questionList = questionString.split(' ')

	questionListLemmetized = []
	lmtzr = WordNetLemmatizer()
	for word in questionList:
		lemmetizedWord = lmtzr.lemmatize(word)
		questionListLemmetized.append(lemmetizedWord)

	return questionListLemmetized

#########################################################################################################
# INPUTS: A list of lemmetized words from a question 													#
# OUTPUTS: A dictionary of words where each key is a unique word used in the question and each value 	#
# 	  is the number of times that word occurs 															#
#########################################################################################################

def get_monograms(questionList):

	dictOfMonograms = {}

	questionLength = len(questionList)
	for i in range(questionLength):

		word = questionList[i]

		if word not in dictOfMonograms:
			dictOfMonograms[i] = 1
		else:
			dictOfMonograms[i] += 1

	return dictOfMonograms

#########################################################################################################
# INPUTS: A list of lemmetized words from a question 													#
# OUTPUTS: A dictionary of words where each key is a unique bigram used in the question and each value 	#
# 	  is the number of times that bigram occurs 														#
#########################################################################################################

def get_bigrams(questionList):

	dictOfBigrams = {}

	questionLength = len(questionList)
	for i in range(questionLength - 1):

		bigram = questionList[i] + " " + questionList[i+1]

		if bigram not in dictOfBigrams:
			dictOfBigrams[bigram] = 1
		else:
			dictOfBigrams[bigram] += 1

	return dictOfBigrams

#########################################################################################################
# INPUTS: A list of lemmetized words from a question 													#
# OUTPUTS: A dictionary of words where each key is a unique trigram used in the question and each value #
# 	  is the number of times that trigram occurs 														#
#########################################################################################################

def get_trigrams(questionList):

	dictOfTrigrams = {}

	questionLength = len(questionList)
	for i in range(questionLength - 2):

		trigram = questionList[i] + " " + questionList[i+1] + " " + questionList[i+2]

		if trigram not in dictOfTrigrams:
			dictOfTrigrams[trigram] = 1
		else:
			dictOfTrigrams[trigram] += 1

	return dictOfTrigrams

#############################
# STEP 2: Train classifiers #
#############################

# This is done in main()

#########################################################
# STEP 3: Print classifier predictions for testing data #
#########################################################

#########################################################################################################
# INPUTS: A filename; a list of multiple classifiers 													#
# OUTPUTS: A csv file containing the classifiers' maximum probability prediction for each question in 	#
#	the testing data 																					#
#########################################################################################################

def predict_testing_examples(filename, listOfClassifiers):

	fileObject = open(filename)
	csvReaderObject = csv.reader(fileObject)

	predictedLabels = []
	for line in csvReaderObject:

		unprocessedQuestion = line[0]
		features = ["monogram", "bigram", "trigram"]
		featureDict = extract_features(unprocessedQuestion, "", "", features)[0]

		listOfPredictions = []
		# Apply each classifier to a question and add each classifier's prediction, along with the	
		#	prediction's probability, to the list
		for classifier in listOfClassifiers:

			dist = classifier.prob_classify(featureDict)
			predictedLabel = classifier.classify(featureDict)
			probability = dist.prob(predictedLabel)
			listOfPredictions.append((predictedLabel, probability))

		# Add the prediction made by whatever classifier offered the highest probability to the list
		maxProbabilityLabel = ''
		maxProbability = 0
		for predictedLabel in listOfPredictions:

			if predictedLabel[0] != 'other':

				if predictedLabel[1] > maxProbability:
					maxProbability = predictedLabel[1]
					maxProbabilityLabel = predictedLabel[0]

		predictedLabels.append([maxProbabilityLabel])

	fileOutputObject = open('Testing Predictions.csv', 'wb')
	csvOutputObject = csv.writer(fileOutputObject)
	csvOutputObject.writerows(predictedLabels)

#####################################################################################################################################################

def main():
	
	trainingFile = "Training.csv"
	testingFile = "Testing.csv"
	
	# Train and evaluate a Naive Bayes classifier that classifies questions as either "artist" or "other"
	desiredFeaturesArtist = ["monogram", "trigram"] 	# Highest accuracy features, see "Accuracy of Different Features.csv"
	trainingExamplesArtist = read_in_data(trainingFile, desiredFeaturesArtist, "artist")
	testingExamplesArtist = read_in_data(testingFile, desiredFeaturesArtist, "artist")
	artistClassifier = NaiveBayesClassifier.train(trainingExamplesArtist)
	print 'artist accuracy: ' + str(nltk.classify.util.accuracy(artistClassifier, testingExamplesArtist))
	artistClassifier.show_most_informative_features()

	# Train and evaluate a Naive Bayes classifier that classifies questions as either "artwork" or "other"
	desiredFeaturesArtwork = ["bigram"] 	# Highest accuracy features, see "Accuracy of Different Features.csv"
	trainingExamplesArtwork = read_in_data(trainingFile, desiredFeaturesArtwork, "artwork")
	testingExamplesArtwork = read_in_data(testingFile, desiredFeaturesArtwork, "artwork")
	artworkClassifier = NaiveBayesClassifier.train(trainingExamplesArtwork)
	print 'artwork accuracy: ' + str(nltk.classify.util.accuracy(artworkClassifier, testingExamplesArtwork))
	artworkClassifier.show_most_informative_features()

	# Train and evaluate a Naive Bayes classifier that classifies questions as either "composer" or "other"
	desiredFeaturesComposer = ["monogram", "trigram"] # Highest accuracy features, see "Accuracy of Different Features.csv"
	trainingExamplesComposer = read_in_data(trainingFile, desiredFeaturesComposer, "composer")
	testingExamplesComposer = read_in_data(testingFile, desiredFeaturesComposer, "composer")
	composerClassifier = NaiveBayesClassifier.train(trainingExamplesComposer)
	print 'composer accuracy: ' + str(nltk.classify.util.accuracy(composerClassifier, testingExamplesComposer))
	composerClassifier.show_most_informative_features()

	# Train and evaluate a Naive Bayes classifier that classifies questions as either "composition" or "other"
	desiredFeaturesComposition = ["bigram"] # Highest accuracy features, see "Accuracy of Different Features.csv"
	trainingExamplesComposition = read_in_data(trainingFile, desiredFeaturesComposition, "composition")
	testingExamplesComposition = read_in_data(testingFile, desiredFeaturesComposition, "composition")
	compositionClassifier = NaiveBayesClassifier.train(trainingExamplesComposition)
	print 'composition accuracy: ' + str(nltk.classify.util.accuracy(compositionClassifier, testingExamplesComposition))
	compositionClassifier.show_most_informative_features()

	classifiers = [artistClassifier, artworkClassifier, composerClassifier, compositionClassifier]

	# Output the highest probability label for each element in the testing data to a csv
	predict_testing_examples('Testing Check.csv', classifiers)

if __name__ == "__main__":
    main()