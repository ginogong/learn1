#coding:utf-8
import matplotlib.pyplot as plt 
import numpy as np

def createDataSet():
	postingList = [['my','dog','has','flea','problems','help','please'],
					['maybe','not','take','him','to','dog','park','stupid'],
					['my','dalmation','is','so','cute','I','love','him'],
					['stop','posting','stupid','worthless','garbage'],
					['mr','licks','ate','my','steak','how','to','stop','him'],
					['quit','buying','worthless','dog','food','stupid']]
	classVec = [0, 1, 0, 1, 0, 1]
	return postingList,classVec 

def createVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set (document)
	return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
	returnVec = [0] *len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else: print 'the word: %s is not in my Vocabulary!' % word
	return returnVec

def trainNB0(trainMatrix,trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = np.sum(trainCategory) / float(numTrainDocs) # insult prob
	p0Num = np.ones(numWords) ; p1Num = np.ones(numWords)
	p0Denom = 2.0; p1Denom = 2.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += np.sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += np.sum(trainMatrix[i])
	p1Vect = np.log(p1Num / p1Denom) 
	p0Vect = np.log(p0Num/ p0Denom )
	return p0Vect,p1Vect,pAbusive 

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
	p1 = np.sum(vec2Classify * p1Vec) + np.log(pClass1)
	p0 = np.sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)
	if p1 > p0: 
		return 1
	else: return 0

def testingNB():
	listOPosts, listClasses = createDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
	p0V,p1V,pAb =  trainNB0(np.array(trainMat),np.array(listClasses))
	testEntry = ['love','my','dalmation']
	thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classifide as:',classifyNB(thisDoc,p0V,p1V,pAb)
	testEntry = ['stupid','garbage']
	thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classifide as:',classifyNB(thisDoc,p0V,p1V,pAb)

def bagOfWords2VecMN(vocabList,inputSet):
	returnVec = [0] * len(inputSet)
	for word in vocabList:
		returnVec[vocabList.index(word)] += 1
	return returnVec

def textParse(bigString):
	import re
	listOfTokens = re.split(r'\W*',bigString)
	return [tok.lower() for tok in listOfTokens if len(tok) > 2]


def spamTest(): 
	path = 'D:\\Ml\\machinelearninginaction\\Ch04\\'
	docList = [];classList=[];fullText = []
	for i in range(1,26):
		wordList = textParse(open(path + 'email/spam/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open(path + 'email/ham/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = createVocabList(docList)
	trainingSet = range(50);testSet = []
	for i in range(20):
		randIndex = int(np.random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat = []; trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V ,p1V,pSpam = trainNB0(trainMat,trainClasses)
	errorCount = 0.0
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList,docList[docIndex])
		if classifyNB(wordVector,p0V,p1V,pSpam) != classList[docIndex]:
			errorCount += 1.0
	print 'the error rate is :', errorCount/len(testSet)
spamTest()








