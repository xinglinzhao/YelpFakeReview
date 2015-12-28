#!/usr/bin/python

from drawHistogram import drawhistogram
from outPutMedia import outPutMedia
import pickle
def transferdata(file,key,outfile):
	data = pickle.load(open(file,'r'))
	result = []
	for k,v in data.items():
		result.append('%s,%s'%(k,v.get(key)))
	open(outfile,'w').write('\n'.join(result))	
def loaddata(file):
	res = {}
	for line in open(file,'r'):
		pair = line.strip().split(',')
		if len(pair) == 2:
			res[pair[0]] = float(pair[1])
	return res
def drive():
	file = ['business_pick.txt','user_pick.txt','review_pick.txt']
	outfile = ['business_reliability.csv','user_trustiness.csv','review_honesty.csv']
	key = ['reliability','trustiness','honesty']
	for i in range(3):
		transferdata(file[i],key[i],'ours'+outfile[i])

def plotcdf(file,suptitle = None):
	data = loaddata(file)
	key,values = zip(*(data.items()))
	maxv = max(map(abs,values))
	normalized = [e/maxv for e in values]
	drawhistogram(normalized,30,(-1,1),None,suptitle = suptitle,ylogscale=True)

if __name__ == '__main__':
	drive()
	outfile = 'distribution_log_ours.pdf'
	o = outPutMedia(outfile)
	plotcdf('oursreview_honesty.csv','review')
	o.write(None)
	plotcdf('oursuser_trustiness.csv','user')
	o.write(None)
	plotcdf('oursbusiness_reliability.csv','business')
	o.write(None)
	o.close()	
