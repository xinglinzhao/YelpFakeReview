#!/usr/bin/python
import pickle
from user import User
from business import Business
from review import Review
from operator import itemgetter
def rating_smoothing(reviews):
	if not reviews:
		return 0
	reviews.sort(key=itemgetter(1))
	return reviews[0][0].get('stars')
def drive(ufile,bfile,rfile,outfile):
	users = pickle.load(open(ufile,'r'))
	business = pickle.load(open(bfile,'r'))
	reviews = pickle.load(open(rfile,'r'))
	preference={}
	for uid,u in users.items():
		busi = {}
		preference.setdefault(uid,{})
		for r in u.get('myreviews'):
			busi.setdefault(reviews[r].get('business_id'),[])
			busi[reviews[r].get('business_id')].append((reviews[r],reviews[r].get('period')))
		for bid,rvs in busi.items():
			rating = rating_smoothing(rvs)
			preference[uid][bid] = rating
	pickle.dump(preference,open(outfile,'w'))
def transformPreference(prefs):
	result = {}
	for person,pref in prefs.items():
		for item,rating in pref.items():
			result.setdefault(item,{})
			result[item][person] = rating
	return result
if __name__ == '__main__':
	'''
	ufile = 'user_pick.txt'
	rfile = 'review_pick.txt'
	bfile = 'business_pick.txt'
	outfile='preference_pick.txt'
	drive(ufile,bfile,rfile,outfile)
	'''
	prefs = pickle.load(open('preference_pick.txt','r'))
	b_prefs = transformPreference(prefs)
	pickle.dump(b_prefs,open('business_preference_pick.txt','w'))



	 
			
