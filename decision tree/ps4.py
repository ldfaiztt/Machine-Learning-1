import math
from sklearn import tree
from random import shuffle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals.six import StringIO
import pydot
import os
def DealMissVal(filename):
	r = open(filename,'r').readlines()
	countlist = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
	for i in range(0,len(r)):
		data = [x.strip() for x in r[i].split(',')]
		for j in range(0,12):
			if data[j] in countlist[j].keys():
				countlist[j][data[j]]+=1
			else:
				countlist[j][data[j]]=1
	res = []
	for i in range(0,12):
		if i==0 or i==8 or i==9 or i==10:
			res.append(avg(countlist[i]))
		else:
			res.append(mode(countlist[i]))
	return res

def avg(dictionary):
	tsum=0
	tcount=0
	for i in dictionary.keys():
		if i!='?':
			tsum+=int(dictionary[i])*int(i)
			tcount+=int(dictionary[i])		
	return tsum/tcount

def mode(dictionary):
	maxVal=''
	maxCount=float('-inf')
	for i in dictionary.keys():
		if i!='?' and int(dictionary[i])> maxCount:
			maxVal=i
			maxCount= int(dictionary[i])
	return maxVal

def getdict(filename):
	bigdict=[]
	r = open(filename,'r').readlines()
	for j in range(0,len(r)):
		toAdd={}
		line=r[j]
		comma=line.find(':')
		pd = line.find('.')
		ft = line[(comma+1):pd].split(',')
		ft = [x.strip() for x in ft]
		if not (j==0 or j==8 or j==9 or j==10):
			for i in range(0,len(ft)):
				toAdd[ft[i]]=i
			bigdict.append(toAdd)
		else:
			bigdict.append(toAdd)
	return bigdict
def preprocess(filename):
	X=[]
	Y=[]
	missVal= DealMissVal(filename)
	bigdict= getdict('features.txt')
	r = open(filename,'r').readlines()
	shuffle(r)
	for j in range(0,len(r)):
		row = []
		data = [x.strip() for x in r[j].split(',')]
		for i in range(0,12):
			if data[i] == '?':
				data[i] = missVal[i]
			if i ==0 or i==8 or i==9 or i==10:
				row.append(int(data[i]))
			else:
				row.append(int(bigdict[i][data[i]]))
		X.append(row)		
		if len(data[12])>4:
			Y.append(1)
		else:
			Y.append(0)
	return [X,Y]

if __name__=='__main__':
	[X,Y] = preprocess('adult_train.txt')
	[testX,testY]= preprocess('adult_test.txt')
	X= np.array(X)
	Y = np.array(Y)
	trainX = X[0:len(X)*0.7]
	trainY = Y[0:len(Y)*0.7]
	validX = X[len(X)*0.7:]
	validY = Y[len(Y)*0.7:]
	clf = RandomForestClassifier(n_estimators=21,max_depth=11,min_samples_leaf=27)
	clf = clf.fit(X,Y)
	print clf.score(testX,testY)
	clf = tree.DecisionTreeClassifier(max_depth=11,min_samples_leaf=27)
	clf = clf.fit(X,Y)
	print clf.score(testX,testY)

