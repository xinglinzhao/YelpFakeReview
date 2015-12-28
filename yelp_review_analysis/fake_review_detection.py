#!/usr/bin/python

import numpy as np
import pickle
from parse_review import loadReviewByRe
import scipy
# smootch function 
def sigmoid(x,coeff):
	return 2/(1+np.exp(x*coeff)) - 1

# update the trustiness for the specific user 
def updateTrustiness(reviewHonestiness,coeff):
	h = sum(reviewHonestiness)
	return sigmoid(h,coeff)
# update the reiability of the producte
def updateReliability(info,mean,coeff):
	validRec = [ (t,r) for t,r in info if t > 0]
	theta = sum([t*(r-mean) for t,r in validRec])
	return sigmoid(theta,coeff)
# update the honesty of the review
def updateHonesty(userRec,thisReview,reliability,timeSlot,agreement,coeff):
	timePoint = int(thisReview.get('period'))
	star = float(thisReview.get('stars'))
	# filter out those review time that falls out the valid time slot
	userRecValid = [ (r,t) for r,t in userRec if abs(int(r.get('period')) - timePoint) <= timeSlot]
	# find those agreed reviewer's trustiness
	agree = [ t for r,t in userRecValid if abs(float(r.get('stars')) - star) <= agreement]
	disagree = [ t for r,t in userRecValid if abs(float(r.get('stars')) - star) > agreement]
	a = sum(agree) - sum(disagree)
	a = sigmoid(a,coeff)
	return abs(reliability)*a
# initialize the honesty,trustiness and reliability for each review,reviewer and product
# initially we assume all reviewer and business are positive
# but the review is neutral
def initialization(users,business,reviews):
	for uid,u in users.items():
		u.set('trustiness',1.0)
	for bid,b in business.items():
		b.set('reliability',1.0)
	for rid,r in reviews.items():
		r.set('honesty',0.0)
# initialize the honesty,trustiness and reliability for each review,reviewer and product
# initially we assume all reviewer and business are positive
# but the review is neutral
def another_initialization(users,business,reviews):
	for bid,b in business.items():
		myreview = [float(reviews[r].get('stars')) for r in b.get('myreviews')]
		variance = scipy.var(myreview)
		mystar = b.get('stars')
		b.set('reliability',0.5*(mystar-3)/(variance+1))
	for rid,r in reviews.items():
		b_star = float(business[r.get('business_id')].get('stars'))
		mystar = float(r.get('stars'))
		diff = mystar - b_star
		r.set('honesty',-1*(abs(diff)-1)/3)	
	for uid,u in users.items():
		myreviews = u.get('myreviews')
		honesty = [reviews[r].get('honesty') for r in myreviews]
		u.set('trustiness',updateTrustiness(honesty,-1))	
		
def detection_algorithm(users,business,reviews,agreement = 1,ucoeff=-1,bcoeff=-1,rcoeff=-1,timeslot=40.0,iter = 10):
	another_initialization(users,business,reviews)
	for i in range(iter):
		for bid,b in business.items():
			info = [(reviews[rid].get('stars'),users[reviews[rid].get('user_id')].get('trustiness')) for rid in b.get('myreviews')]
			#b.set('reliability',updateReliability(info,float(b.get('stars')),bcoeff))
			b.set('reliability',updateReliability(info,3.0,bcoeff))
		for rid,r in reviews.items():
			userRec = [ (reviews[other],users[reviews[other].get('user_id')].get('trustiness')) for other in business[r.get('business_id')].get('myreviews') if other != rid ]
			relia = business[r.get('business_id')].get('reliability')
			r.set('honesty',updateHonesty(userRec,r,relia,timeslot,agreement,rcoeff))
		for uid,u in users.items():
			honestiness = [reviews[rid].get('honesty') for rid in u.get('myreviews')]
			u.set('trustiness',updateTrustiness(honestiness,ucoeff))
def output(data,key,outfile):
	handler = open(outfile,'w')
	for k,v in data.items():
		handler.write(','.join([k,str(v.get(key))]) + '\n')
	handler.close()

def drive(userfile,businessfile,reviewfile):
	users = pickle.load(open(userfile,'r'))
	business = pickle.load(open(businessfile,'r'))
	reviews = pickle.load(open(reviewfile,'r'))
	detection_algorithm(users,business,reviews)
	'''
	output(users,'trustiness','user_trustiness_init.csv')
	output(business,'reliability','business_reliability_init.csv')
	output(reviews,'honesty','review_honesty_init.csv')
	'''
	output(users,'trustiness','user_trustiness.csv')
	output(business,'reliability','business_reliability.csv')
	output(reviews,'honesty','review_honesty.csv')		


if __name__ == '__main__':
	userfile = 'user_pick.txt'
	businessfile = 'business_pick.txt'
	reviewfile = 'review_pick.txt'
	#reviews = loadReviewByRe('review_time.json')
	#pickle.dump(reviews,open(reviewfile,'w'))
	drive(userfile,businessfile,reviewfile)
		


		
	

