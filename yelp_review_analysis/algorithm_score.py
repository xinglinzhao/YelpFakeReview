#!/usr/bin/python
import numpy as np

import scipy
from review import Review
from business import Business
from user import User
from operator  import itemgetter
import pickle
from parse_business import loadBusiness
def reviewDeviation(reviews,business):
	for rid,r in reviews.items():
		mystar = float(r.get('stars'))
		bstar = float(business[r.get('business_id')].get('stars'))
		r.set('review_deviation',abs(mystar-bstar)/4)
	
def earlyReviewDeviation(reviews,business,cutpoint = 60):
	for bid, b in business.items():
		mystar = float(b.get('stars'))
		myreviews = [reviews[r] for r in b.get('myreviews')]
		time_reviews = sorted([ (float(r.get('period')),r) for r in myreviews],key=itemgetter(0),reverse=True)
		time_delay = [(0,time_reviews[0][1])]
		for t,r in time_reviews[1:]:
			time_delay.append((time_reviews[0][0] - t,r))
		for delay,r in time_delay:
			if delay < cutpoint:
				etd = (1-delay/cutpoint)*abs(float(r.get('stars')) - mystar)/4
			else:
				etd = 0
			r.set('etd',etd)	
			
def average_shifting(myreviews,mystars,timeInterval=30,proportion=0.5):
	timePoints = [ (int(r.get('period')),r) for r in myreviews]
	timePoints = sorted(timePoints,key=itemgetter(0),reverse=True)
	bins = binTime(timePoints,timeInterval)
	sample_sz = len(bins) * proportion
	if sample_sz < 1:
		sample_sz = 1
	sampled = np.random.choice(range(len(bins)),size=sample_sz,replace=False)
	sampled_review = []
	for s in sampled:
		sampled_review += bins[s]
	if sampled_review:
		ratings =np.mean([ float(r.get('stars')) for r in sampled_review])
		return abs(ratings-mystars)/4
	else:
		return 0.0
def binTime(timePoints,timeInterval):
	oldest = timePoints[0][0]
	newest = timePoints[-1][0]	
	start = oldest - timeInterval 
	bins = [(oldest,start)]
	while start > newest:
		bins.append((start,start-timeInterval))
		start = start - timeInterval
	
	res = []
	tmp = []
	dataindex = 0
	binindex = 0
	while dataindex < len(timePoints) and binindex < len(bins):
		if timePoints[dataindex][0] <= bins[binindex][0] and timePoints[dataindex][0] > bins[binindex][1]:
			tmp.append(timePoints[dataindex][1])
			dataindex += 1
		elif timePoints[dataindex][0] <= bins[binindex][1]:
			binindex += 1
			res.append(tmp)
			tmp = []
	if tmp:
		res.append(tmp)
		
				 			
	if dataindex < len(timePoints):
		tmp = []
		for i in timePoints[dataindex:]:
			tmp.append(i[1])	
		res.append(tmp)				
	return res
def calculateMrss(business,windows = 7):
	for bid,b in business.items():
		mss = {}
		for uid,c in b.get('reviewers').items():
			mss[uid] = 1/float(c)
		b.set('mrss',mss)			
def calculateMNRW(users,reviews,window = 1,threshold = 3):
	for uid, u in users.items():
		myreviews = [reviews[r].get('period') for r in u.get('myreviews')]
		if myreviews:
			count = {}
			for p in myreviews:
				count.setdefault(p,0)
				count[p] += 1
			
			frequency = zip(*(count.items()))[1]
			maxf = max(frequency)
			if maxf >= threshold:
				u.set('mnrw',maxf) 
			else:
				u.set('mnrw',1)
		else:
			u.set('mnrw',1)		
		
def calculateAPER(users,reviews):
	for uid, u in users.items():
		myreviews = [float(reviews[r].get('stars')) for r in u.get('myreviews')]
		fives = 0.0
		ones = 0.0
		if myreviews:
			for s in myreviews:
				if s == 5.0:
					fives += 1
				elif s == 1.0:
					ones += 1
			u.set('aper',(fives + ones)/len(myreviews))
		else:
			u.set('aper',0.0)		
	
def updateBusiness(business,users,reviews):
	for bid,b in business.items():
		myreviews = []
		earlyreviews = []
		for r in b.get('myreviews'):
			myreviews.append((1-float(reviews[r].get('review_deviation')))*float(reviews[r].get('honesty')))
			if float(reviews[r].get('etd')) != 0.0:
				earlyreviews.append((1-float(reviews[r].get('etd')))*float(reviews[r].get('honesty')))
		mrss = b.get('mrss')
		av_mrss = 0.0
		for uid,m in mrss.items():
			av_mrss += float(m)*float(users[uid].get('trustiness'))
		av_mrss /= len(mrss)	
		#pdb.set_trace()
		if earlyreviews and myreviews:
			s = 0.25*(1-float(b.get('as')) + sum(myreviews)/len( myreviews) + sum(earlyreviews)/len(earlyreviews) + av_mrss)
		else:
			s = -1
		b.set('reliability',s)

def updateReviewFromBusiness(business,reviews):
	for rid,r in reviews.items():
		score = 0.5*(2- r.get('etd') - r.get('review_deviation'))*business[r.get('business_id')].get('reliability')
		r.set('honesty',score)

def updateUserFromReview(users,reviews):
	for uid,u in users.items():
		myreviews = [reviews[r] for r in u.get('myreviews')]
		if myreviews:
			mtrd = 0.0
			metd = 0.0
			etd_count = 0
			for r in myreviews:
				if r.get('etd') != 0:
					etd_count += 1
					metd += (1-r.get('etd'))*float(r.get('honesty'))
				mtrd += (1-r.get('review_deviation'))*r.get('honesty')
			mtrd /= len(myreviews)
			if etd_count:	
				metd = metd / etd_count 
			else:
				metd = 1.0
			score = 1/(float(u.get('mnrw')) + 1 - u.get('aper') + mtrd + metd )
			u.set('trustiness',score)  
			
		else:
			u.set('trustiness',-1)
def updateReviewFromUsers(users,reviews,alpha = 5):
	for rid,r in reviews.items():
		trustiness = users[r.get('user_id')].get('trustiness')
		grd = r.get('review_deviation')
		etd = r.get('etd')
		score = trustiness/(1+np.exp(alpha*(1 - grd - etd)))
		r.set('honesty',score) 
def updateUserFromUser(users,gamma = 0.3):
	trustiness = {}
	for uid,u in users.items():
		trustiness[uid] = u.get('trustiness')
	for uid,u in users.items():
		score = (1-gamma)*trustiness[uid] 
		tmp = 0.0
		friends = u.get('friends')
		for f in friends:
			tmp += trustiness[f]
		if friends:
			score += gamma*tmp/len(friends)		
		u.set('trustiness',score)
			
def initialization(users,reviews):
	for uid,u in users.items():			
		u.set('trustiness',0.5)
	for rid,r in reviews.items():
		r.set('honesty',0.5)
		 
# main process of the algorithm
def algorithm_process(business,reviews,users,iteration = 20,alpha = 5,gamma = 0.3):
	initialization(users,reviews)
	for i in range(iteration):
		print('Current step : %s\n' %(i))		
		
		updateBusiness(business,users,reviews)
		
		updateReviewFromBusiness(business,reviews)
		
		updateUserFromReview(users,reviews)
		updateUserFromUser(users,gamma)
		updateReviewFromUsers(users,reviews,alpha)
	
def drive():
	business_file = 'reviewed_business.json'
	review_file = 'review_pick.txt'
	user_file = 'user_pick.txt'
	business = loadBusiness(business_file)
	users = pickle.load(open(user_file,'r'))
	reviews = pickle.load(open(review_file,'r'))
	#calculateMNRW(users,reviews)
	#calculateAPER(users,reviews)
	for bid,b in business.items():
		myreviews = [reviews[r] for r in b.get('myreviews')]
		average_shift = average_shifting(myreviews,float(b.get('stars')))
		b.set('as',average_shift)
	#reviewDeviation(reviews,business)
	calculateMrss(business)
	#earlyReviewDeviation(reviews,business)
	#pickle.dump(reviews,open(review_file,'w')) 
	pickle.dump(business,open(business_file,'w')) 
	#pickle.dump(users,open(user_file,'w'))
def algorithm_drive(userfile,businessfile,reviewfile):
	users = pickle.load(open(userfile,'r'))
	business = pickle.load(open(businessfile,'r'))
	reviews = pickle.load(open(reviewfile,'r'))
	algorithm_process(business,reviews,users)		
	outfile = 'oursuser_trustiness.csv'
	res = []
	for uid, u in users.items():
		res.append('%s,%s'%(uid,u.get('trustiness')))
	open(outfile,'w').write('\n'.join(res))
	
	outfile = 'oursbusiness_reliability.csv'
	res = []
	for uid, u in business.items():
		res.append('%s,%s'%(uid,u.get('reliability')))

	open(outfile,'w').write('\n'.join(res))
	outfile = 'oursreview_honesty.csv'
	res = []
	for uid, u in reviews.items():
		res.append('%s,%s'%(uid,u.get('honesty')))

	pickle.dump(users,open(userfile,'w'))
	pickle.dump(business,open(businessfile,'w'))
	pickle.dump(reviews,open(reviewfile,'w'))
if __name__ == '__main__':
	#drive()
	business_file = 'business_pick.txt'
	review_file = 'review_pick.txt'
	user_file = 'user_pick.txt'
	algorithm_drive(user_file,business_file,review_file)
