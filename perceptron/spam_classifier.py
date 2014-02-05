#!/usr/bin/env python

import sys
import os
from sets import Set
import operator
import copy

#intiate features with weight0 as {x1:0,x2:0...xn:0}
def InitWeight(filename,linenum):
	f = open(filename,'r')
	x= {}
	for j in range(0,linenum):
		words = f.readline().split()
		words_in_a_mail = Set([])
		for i in range(1,len(words)):
			words_in_a_mail.add(words[i])
		for word in words_in_a_mail:
			if word in x:
				x[word] += 1
			else:
				x[word] = 1
	for k,v in x.items():
		if v < 30:
			del x[k]
	for k in x.keys():
		x[k]=0
	f.close()
	return x
# matrix:
# [y, {x1:0/1,x2:0/1...xn:0/1};
#  ...
#  y, {x1:0/1,x2:0/1...xn:0/1};
#  y, {x1:0/1,x2:0/1...xn:0/1};
#  y, {x1:0/1,x2:0/1...xn:0/1}]
def getfx(w,filename,linenum,offset):
	matrix = []
	f = open(filename,'r')
	lines = f.readlines()
	for j in range(offset,offset+linenum):
		words = lines[j].split()
		fx = {}
		for feature in w.keys():
			if feature in words[1:]:
				fx[feature]=1
			else:
				fx[feature]=0
		matrix.append([fx,2*int(words[0])-1])
	f.close()
	return matrix
#dot of two vectors
def dot(w,fx):
	res = 0
	for x in w.keys():
			res += w[x]*fx[x]
	return res
# w:=w+multi*fx
def add(w,fx,multi):
	for x in w.keys():
			w[x] += multi*fx[x]

def scale(w,multi):
	for x in w.keys():
			w[x] = multi*w[x]
	return w

def perceptron_train(w,filename,linenum,maxiter):
	wavg = copy.deepcopy(w)
	matrix = getfx(w,filename,linenum,0)
	k = 0
	iters =0
	err=1
	while err!=0 and iters<maxiter:
		err=0
		for i in range(0,linenum):
			fx = matrix[i][0]
			r = dot(w,fx)
			if (r >=0 and matrix[i][1] <0) or (r <0 and matrix[i][1] > 0):
				add(w,fx,matrix[i][1])
				err +=1
			add(wavg,w,1)
		k += err
		iters +=1
	return [w,k,iters,scale(wavg,1/float(iters*linenum))]

# w: weight vector, linenum: number of lines to test, offset: the begin line of testfile
def perceptron_test(w,filename,linenum,offset):
	matrix = getfx(w,filename,linenum,offset)
	err=0
	for i in range(0,linenum):
		r = dot(w,matrix[i][0])
		if  (r >= 0 and matrix[i][1] <0) or (r < 0 and matrix[i][1] > 0):
			err +=1
	return float(err)/linenum

def sort_dict(x):
	sorted_x = sorted(x.iteritems(),key=operator.itemgetter(1))
	return sorted_x

def reverse_sort_dict(x):
	sorted_x = sorted(x.iteritems(),key=operator.itemgetter(1))
	return list(reversed(sorted_x))

if __name__ == '__main__':
	

	w = InitWeight('spam_train.txt',4000)
	r = perceptron_train(w,'spam_train.txt',5000,10)
	print "--- %d maximum iterations ---" %(r[2])
	print "perceptron test error:%f" %(perceptron_test(r[3],'spam_test.txt',1000,0))
	