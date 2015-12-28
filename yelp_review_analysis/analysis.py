#!/usr/bin/python

import pickle
import numpy as np
from loadcsv import loaddata
from drawScatter import drawScatter
from drawHistogram import drawhistogram
#extract 
def extractReviews(entry,source,target,sourcekey,targetkey):
	candidates = source[entry].get(sourcekey)
	result = [float(target[r].get(targetkey)) for r in candidates]
	return result 
def businessAnalysis(business,review,candidate):
	skey = 'myreviews'
	tkey = 'stars'
	result = []
	for c in candidate:
		result.append(extractReviews(c,business,review,skey,tkey))
	return result

def plotCorr(result,outfile):
	bin = 5
	range = (1,5)
	for r in result:
		drawhistogram(r,bin,range,outfile)			 

def drive(scorefile,businessfile,reviewfile,n,outfile):
	score = loaddata(scorefile)
	score = [ (k,s)  for k,s in score if s > -1]
	part = score[0:n]
	print(part)
	business = {}#pick.load(open(businessfile,'r'))
	reviews  = {}#pick.load(open(reviewfile,'r'))
	result = businessAnalysis(business,reviews,zip(*part)[0])
	print(result)
	plotCorr(result,outfile)
if __name__ == '__main__':
	scorefile = 'oursbusiness_reliability.csv'
	businessfile = 'business_pick.txt'
	reviewfile = 'review_pick.txt'
	outfile = 'business_review.pdf'
	n = 20
	drive(scorefile,businessfile,reviewfile,n,outfile)
		
