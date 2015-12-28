#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
import os
import sys

from business import Business
from parse_business import  loadBusiness
import random
from parse_review import loadReviewByRe
from matplotlib.backends.backend_pdf import PdfPages
from drawHistogram import drawhistogram as drawhist
def getReviewStars(business,reviews):
	res = []
	for k,v in business.items():
		myreviews = v.get('myreviews')
		scores = map(lambda x: float(reviews[x].get('stars')), myreviews)
		res.append((k,scores))
	return res
def drive(businessfile,reviewfile,outfile,cutoff = 20,total = 10):
	business = loadBusiness(businessfile)
	reviews = loadReviewByRe(reviewfile)
	scorepairs = getReviewStars(business,reviews)
	
	scorep = sorted([ (k,s) for k,s in scorepairs if len(s) > cutoff],key=len,reverse=True)	
	length = len(scorep)
	#ids = set() 
	print(length)
	for i in range(total):
		'''
		if len(ids) == length:
			break
		newp = random.randint(0,length -1)
		while newp in ids:
			newp = random.randint(0,length-1)
		print(newp)
		drawhist(scorep[newp][1],20,(0,5),outfile,scorep[newp][0],'score','freqency')
		'''
		drawhist(scorep[i][1],20,(0,5),outfile,scorep[i][0],'score','freqency')
		#ids.add(newp)

if __name__ == '__main__':
	outfile = 'business_start_hist.pdf'
	outfilehandler = PdfPages(outfile)
	business_file = 'reviewed_business.json'
	review_file = 'yelp_academic_dataset_review.json'
	drive(business_file,review_file,outfilehandler)
	outfilehandler.close()
	

				
	
	
