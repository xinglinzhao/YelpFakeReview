#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from operator import itemgetter
from matplotlib.backends.backend_pdf import PdfPages
def loadIsoformData(file):
	fhandler = open(file,'r')
	count = []
	freq = []
	for line in fhandler:
		rec = line.rstrip().split(',')
		rec = list(map(int,rec))
		count.append(rec[0])
		freq.append(rec[1])
	return (count,freq)
def combineCategory(count,freq,threshold):
	zipped = zip(count,freq)
	sortedzipped = sorted(zipped,key=itemgetter(0))
	updated_label = []
	updated_freq = []
	for c,f in sortedzipped:
		if c <= threshold:
			updated_label.append(c)
			updated_freq.append(f)
		else:
			updated_freq[-1] += f 
	updated_label = list(map(str,updated_label))
	updated_label[-1] = '>=%s'%(threshold)
	return (updated_label,updated_freq)
        
def drawPie(labels,freq,file):
	fig = plt.figure()
	fig.suptitle('Percentage of annotated genes in terms of the number of isoforms',fontsize = 14,fontweight='bold')
	expl = [0]*len(labels)
	expl[0] = 0.1
	explode = tuple(expl)
	plt.pie(freq,labels = labels,autopct = '%1.1f%%',explode = explode,shadow=True,startangle=90)
	plt.axis('equal')
	plt.savefig(outfile,format='pdf')
	plt.show()

if __name__ == '__main__':
	import os
	file = 'isoform_stat.csv'
	labels,freq = loadIsoformData(file)
	labels,freq = combineCategory(labels,freq,6)
	outfile = 'isoform_stat.pdf'
	drawPie(labels,freq,outfile)
    
