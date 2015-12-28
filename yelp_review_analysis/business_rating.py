#!/usr/bin/python

from parse_review import loadReviewByRe
from user_generator import loadUsers
from user import User
from stats import variance
from business import Business
from parse_business import loadBusiness
import scipy
import scipy.stats
from operator import itemgetter
def rank_Variance(business,reviews,cutoff= 10):
	filtered_bus = dict([(k,v) for k,v in business.items() if len(v.get('myreviews')) >= cutoff])
	ratings = {}
	for k,v in filtered_bus.items():
		tmp = []
		for r in v.get('myreviews'):
			tmp.append(reviews[r].get('stars'))
		ratings[k] = tmp
	busi_variances = variance(ratings)
	sorted_busi = sorted(busi_variances.items(),key=itemgetter(1))
	return sorted_busi	


if __name__ == '__main__':
	import os
	datadir = '/home/laozzzzz/Documents/yelp/yelp_data'
	businessfile = os.path.join(datadir,'reviewed_business.json')
	reviewfile = os.path.join(datadir,'yelp_academic_dataset_review.json')
	business = loadUsers(businessfile)
	reviews = loadReviewByRe(reviewfile)
	sorted_busi = rank_Variance(business,reviews,10)
	print(len(sorted_busi))
