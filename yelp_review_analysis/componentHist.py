#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_pdf import PdfPages 
from drawHistogram import drawhistogram
from drawScatter import drawScatter
from identifyComponents import parseComponents
import math
import numpy as np
#draw the histogram of the size of the connected components
def networkHist(componentfile,outPrefix):
	components = parseComponents(componentfile)
	original = map(lambda x: len(x[1]),components.items())
	original.sort(reverse=True)
	maxsz = original[0]
	size = [float(x)/maxsz for x in original]
#	print(map(math.log,size[0:11]))
	outfilehandler = PdfPages(outPrefix+'.pdf')	
	
	drawhistogram(size,10,(0,1),outfilehandler,False,False,outPrefix+'_original')
	drawhistogram(size,10,(0,1),outfilehandler,True,True,outPrefix+'_loglog')
	drawhistogram(size,10,(0,1),outfilehandler,False,True,outPrefix+'_semilog')
	#hist,bins = np.histogram(size,bins = 10, range = (0,1))
	#print(bins,hist)
	#bins = setBins([0,1])
	freq = countFrequency(original)
	bins,sz = zip(*freq)
	print(bins,sz)
	drawScatter(bins,sz,outfilehandler,'scatter_plot_componentsize','componentSize','Frequency',True,True)	
	outfilehandler.close()
def countFrequency(data):
	freq = {}
	for k in data:
		freq.setdefault(k,0)
		freq[k] += 1
	return freq.items()
	'''
	freq = np.zeros(len(bins))
	for d in data:
		ind = 0
		while d > bins[ind]:
			ind += 1
		freq[ind-1] += 1  
	return freq			  
	'''
		
def setBins(range):
	step = []
	lowbound = 0.0000001
	start = range[1]
	while start > lowbound:
		step.append(start)
		start = start*0.1
	step.append(range[0])
	step.reverse()
	return step
def center(bins):
	res = []
	if len(bins) <= 1:
		return res
	start = bins[0]

	for b in bins[1:]:
		res.append((b+start)/2)
		start = b
	return res
if __name__ == '__main__':
	componentfile = 'user_component.csv'
	outPrefix = 'user_component_hist'
	networkHist(componentfile,outPrefix)
		
