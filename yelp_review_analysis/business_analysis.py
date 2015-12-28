# coding: utf-8
import sys
import os
from parse_business import loadBusiness
business = loadBusiness('reviewed_business.json')
len(business)
from parse_review import loadReviewByRe
reviews = loadReviewByRe('yelp_academic_dataset_review.json')
reviews = loadReviewByRe('yelp_academic_dataset_review.json')
len(reviews)
from business_rating import rate_Variance
from business_rating import rate_Variance
from business_rating import rank_Variance
cutoff = 10
sorted_bus = rank_Variance(business,reviews)
len(sorted_bus)
sorted_bus[0]
sorted_bus[1]
sorted_bus[-1]
print(business[sorted_bus[0][0]])
print(business[sorted_bus[-1][0]])
import scipy.var
import scipy
import scipy.var
import numpy as np
len(sorted_bus)
ratings = [reviews[k].get('stars') for k in business[sorted_bus[0][0]].get('myreviews')]
ratings
ratings = [reviews[k].get('stars') for k in business[sorted_bus[-1][0]].get('myreviews')]
ratings
ratings = [reviews[k].get('stars') for k in business[sorted_bus[-2][0]].get('myreviews')]
ratings
business[sorted_bus[-1][0]]
print(business[sorted_bus[-1][0]])
last_review = [reviews[k] for k in business[sorted_bus[-1][0]].get('myreviews')]
print(last_review[0])
print(last_review[1])
print(last_review[2])
print(last_review[3])
print(last_review[4])
print(last_review[5])
from user_generator import loadUsers
users = loadUsers('final_user.json')
pops = [r.get('user_id').get('popularity') for r in last_review]
from review import Review
pops = [r.get('user_id').get('popularity') for r in last_review]
print(last_review)
last_review[1].get('user_id')
pops = [users[r.get('user_id')].get('popularity') for r in last_review]
pops
pairs = zip(ratings,pops)
pairs
laste_review[1:3]
last_review[1:3]
print(last_review[1:3])
print(last_review[1],last_review[2])
print(last_review[1].__str__(),last_review[2].__str__())
print(last_review[1])
print(last_review[2])
pairs
sorted_bus[-1]
last_reviews
last_review
pops = [ (r.get('user_id'),users[r.get('user_id')].get('popularity'),r.get('stars')) for r in last_review]
pops
average_stars = [users[k].get('average_stars') for k in pops]
average_stars = [users[k].get('average_stars') for k,p,r in pops]
average_stars
zip(pop,average_stars)
zip(pops,average_stars)
import pickle
len(sorted_bus)
pickle.dump(sorted_bus,open(variance_business.txt,'w'))
pickle.dump(sorted_bus,open('variance_business.txt','w'))
objs = pickle.load('variance_business.txt')
objs = pickle.load(open('variance_business.txt','r'))
len(objs)
ojs[0]
