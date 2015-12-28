# coding: utf-8
from parse_business import loadBusiness
import matplotlib
matplotlib.use('Agg')
import numpy
import scipy
import pickle
buss_var = pickle.load(open('variance_business','r'))
buss_var = pickle.load(open('variance_business.txt','r'))
from business import Business
len(buss_var)
buss_var[-1]
from review import Review
from parse_review import loadReviewByRe
reviews = loadReviewByRe('yelp_academic_dataset_review.json')
len(reviews)
from user_generator import loadUsers
from user import User
users = loadUsers('final_user.json')
print(reviews.items()[0])
print(reviews.items()[0][1])
reviews = loadReviewByRe('review_time.json')
len(buss)
dir()
from parse_business import loadBusiness
business = loadBusiness('reviewed_business.json')
get_ipython().magic(u'whos ')
def findAllReviews(bussiness,reviews,key):
    revs = []
    for r in business[key].get('myreviews'):
        revs += reviews[r]
    return revs
last_reviews = findAllReviews(business,reviews,buss_var[-1][0])
from review impor Review
from review import Review
last_reviews = findAllReviews(business,reviews,buss_var[-1][0])
len(business)
business.items()[0][0]
business.items()[0][1]
print(business.items()[0][1])
dir()
get_ipython().magic(u'who ')
dir(findAllReviews)
def findAllReviews(bussiness,reviews,key):
    revs = []
    for r in business[key].get('myreviews'):
        revs += reviews[r]
    return revs
findAllReviews(business,reviews,buss_var[-1][0])
len(reviews)
print(reviews.items()[1][1])
print(buss_var[-1][0])
def findAllReviews(business,reviews,key):
    revs = []
    for r in business[key].get('myreviews'):
        print(r)
        print(reviews[r])
        revs += reviews[r]
        
findAllReviews(business,reviews,buss_var[-1][0])
def findAllReviews(business,reviews,key):
    revs = []
    for r in business[key].get('myreviews'):
        revs.append(reviews[r])
    return revs
last_reviews = findAllReviews(business,reviews,buss_var[-1][0])
last_reviews
time_rating = [(r.get('period'),r.get('stars')) for r in last_reviews]
time_rating
from operator import itemgetter
time_rating.sort(key=itemgetter(0),reverse=True)
time_rating
time,rating = zip(*time_rating)
from drawScatter import drawScatter
from matplotlib.backends.backend_pdf import PdfPages
outfile = PdfPages('time_rating.pdf')
get_ipython().magic(u'whos ')
drawScatter(time,rating,outfile,"time vs rating of" + buss_var[-1][0],time,rating)
outfile.close()
time
raing
rating
drawScatter(time,rating,outfile,"time vs rating of" + buss_var[-1][0],'time in day','rating from 1 to 5')
outfile = PdfPages('time_rating.pdf')
drawScatter(time,rating,outfile,"time vs rating of" + buss_var[-1][0],'time in day','rating from 1 to 5')
outfile.close()
time
rating
cutoff = 100
buss_var.reverse()
def findnext(buss_var,business):
    for bid,var in buss_var:
        	
        
        
        
        
        
        
        
        
        
        
      dfd  
      sdf
      sfds
      s
      
varcutoff = 3
def findnext(buss_var,bussiness,rcutoff,vcutoff):
	res = []
	for bid,var in buss_var:
		if var >= vcutoff and len(business[bid].get('myreviews')) >= rcutoff:
			res.append(bid)
	return res
abbuss = findnext(buss_var,business,cutoff,varcutoff)
len(abbuss)
def findnext(buss_var,bussiness,rcutoff,vcutoff):
	res = []
	for bid,var in buss_var:
		if var >= vcutoff and len(business[bid].get('myreviews')) >= rcutoff:
			res.append(bid)
	return res
def findnext(buss_var,bussiness,rcutoff,vcutoff):
	res = []
	for bid,var in buss_var:
		if var >= vcutoff and len(business[bid].get('myreviews')) >= rcutoff:
			res.append(bid)
	return res
def findAll(buss_var,business,rcutoff,vcutoff):
	res = []
	for bid,var in buss_var:
		print(bid,var)
		if var >= vcutoff or len(business[bid].get('myreviews')) >= rcutoff:
			res.append(bid)
	return res
abbuss = findAll(buss_var,business,cutoff,varcutoff)
abbuss
def findAll(buss_var,business,rcutoff,vcutoff):
	res = []
	for bid,var in buss_var:
		#print(bid,var)
		if var >= vcutoff and len(business[bid].get('myreviews')) >= rcutoff:
			res.append(bid)
	return res
abbuss = findAll(buss_var,business,cutoff,varcutoff)
len(abbuss)
def findAll(buss_var,business,rcutoff,vcutoff):
	res = []
	for bid,var in buss_var:
		#print(bid,var)
		if var >= vcutoff:
			res.append(bid)
	return res
abbuss = findAll(buss_var,business,cutoff,varcutoff)
len(abbuss)
abbusiness = [v for v in business.values() if len(v.get('myreviews')) > 50]
len(abbusiness)
abbusiness = [v for v in abbuss if len(business[v].get('myreviews')) > 50]
abbusiness
abnormal_set = []
for k in abbusiness:
	abnormal_set.append(findAllReviews(business,reviews,k))
abnormal_set
len(abnormal_set)
time_rating = []
for k in abnormal_set:
	time_rating.append([(v.get('period'),v.get('stars')) for v in k])
len(time_rating)
time_rating[0]
pickle.dump(open('abnormal_business.txt','w'),time_rating)
pickle.dump(time_rating,open('abnormal_business.txt','w'))
