#!/usr/bin/python
import matplotlib as mpl
mpl.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
from parse_review import loadReviewByRe
from drawScatter import drawScatter
import datetime as dt

def extractDate(reviewfile):
	reviews = loadReviewByRe(reviewfile)
	now = dt.datetime.now()
	for k,v in reviews.items():
		date = v.get('date')
		postTime = dt.datetime.strptime(date,'%Y-%m-%d')
		period = (now - postTime).days
		v.set('period',period)
	return reviews
def getPeriod(u):
	return u.get('period')
def outputReview(reviews,outfile):
	users = reviews.values()
	users.sort(reverse=True,key = getPeriod)
	open(outfile,'w').write('\n'.join([u.__str__() for u in users]))

def plotVotesVsTime(users,outfile):
	x = []
	y = []
	for k,v in users.items():
		period = int(v.get('period'))
		x.append(period)
		t = 0
		for cat,count in v.get('votes').items():
			t += int(count)
		y.append(t)
	outfile = PdfPages(outfile)
	drawScatter(x,y,outfile,'Time vs vote count in original scale',' Time in day', 'votes counted')	
	drawScatter(x,y,outfile,'Time vs vote count in semilog_scale',' Time in day', 'votes counted',True)	
	drawScatter(x,y,outfile,'Time vs vote count in loglog scale',' Time in day', 'votes counted',True,True)	
	outfile.close()
	
if __name__ == '__main__':
	reviewfile = 'yelp_academic_dataset_review.json'
	#reviews = extractDate(reviewfile)
	#outputReview(reviews,'review_time.json')
	reviews = loadReviewByRe('review_time.json')
	plotVotesVsTime(reviews,'time2votes.pdf')	
