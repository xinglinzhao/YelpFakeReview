#!/usr/bin/python

import pickle
from user import User
from review import Review
import numpy as np

def getTimeInterval(timePoints):
	res = []
	if len(timePoints) > 1:
		res.append(0)
		for ind in range(1,len(timePoints)):
			res.append(timePoints[ind-1] - timePoints[ind])
	return res
	
def findComplteReviewUser(users,reviews):
	result = {}
	for uid,u in users.items():
		myr = u.get('myreviews')
		recCount = int(u.get('review_count'))
		if len(myr) and len(myr) == recCount :
			reviewTime = []
			for r in myr:
				p = reviews[r].get('period')
				if not p:
					raise RuntimeError('invalid period')
				reviewTime.append(p)
			reviewTime.sort(reverse=True)
			result[uid] = getTimeInterval(reviewTime)
	return result



if __name__ == '__main__':
	'''
	timepoint = np.random.randint(0,100,size=10)
	timepoint = sorted(timepoint,reverse=True)
	print(timepoint)
	print(getTimeInterval(timepoint))
	'''
	userf = 'user_pick.txt'
	review = 'review_pick.txt'
	completeUser = findComplteReviewUser(pickle.load(open(userf,'r')),pickle.load(open(review,'r')))
	pickle.dump(completeUser,open('complete_review_users_pick.txt','w'))
