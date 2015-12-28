#!/usr/bin/python

import os
import sys
from json_generator import jsonIterator
from operator import itemgetter 
from business import Business
from user import User
from review import Review 
import resource
from parse_review import loadReview
from parse_business import loadBusiness
from drawHistogram import drawHistogramBylogScale as drawHist
import math

import pickle
#page ranking scoring function

def starsScore(values):
	total = 0
	for v in values:
		total += v/5
	return total	

		
# for each reviewer,  add its own review ids and the businessIDs that they write review for
def addReviewIDAndReviewerID(business,reviews):
	for k,v in business.items():
		if not v.get('business_id') in reviews:
			v.set('myreviews',[])
			v.set('reviewers',[])
			continue
		myreviews = reviews[v.get('business_id')]
		myreviewids = [(e.get('review_id'),e.get('user_id')) for e in myreviews]
		ids = zip(*myreviewids)
		v.set('myreviews',ids[0])
		authorlog = {}
		for aid in ids[1]:
			authorlog.setdefault(aid,0)
			authorlog[aid] += 1
		v.set('reviewers',authorlog)
# drive for updating the reviewid and business id 
def updateDrive(businessfile,reviewfile,reviewedBusinessFile,noreviewBusinessfile):
	reviews = loadReview(reviewfile,'business_id')
	business = loadBusiness(businessfile)
	addReviewIDAndReviewerID(business,reviews)
	noReviewBusiness = ''
	reviewedBusiness = ''
	for k,v in business.items():
		if not len(v.get('myreviews')):
			noReviewBusiness += ('%s\n'%(v.__str__()))
		else:
			reviewedBusiness += ('%s\n'%(v.__str__()))	
	open(reviewedBusinessFile,'w').write(reviewedBusiness) 
	open(noreviewBusinessfile,'w').write(noReviewBusiness)
def normalized(userfile):
	users = loadUsers(userfile)
	maxScore= 0
	for k,v in users.items():
		if v.get('popularity') > maxScore:
			maxScore = v.get('popularity')
	popularityScores = [v.get('popularity')/maxScore for v in users.values()]
	bin = 100	
	filename = 'popularity_score_hist_loglog.pdf'
	drawHist(popularityScores,bin,(0,1),filename)		
if  __name__ == '__main__':
	resource.setrlimit(resource.RLIMIT_STACK,(2**29,-1))
	sys.setrecursionlimit(10**6)
	businessfile = 'yelp_academic_dataset_business.json'
	reviewedBusinessfile = 'reviewed_business.json'	
	noReviewBusiness = 'no_review_business.json'
	reviewfile = 'yelp_academic_dataset_review.json'
	reviews = loadReview(reviewfile,'business_id')
	business = loadBusiness(reviewedBusinessfile)
	addReviewIDAndReviewerID(business,reviews)
	pickle.dump(business,open('business_pick.txt','w'))	
#	DupdateDrive(businessfile,reviewfile,reviewedBusinessfile,noReviewBusiness)





