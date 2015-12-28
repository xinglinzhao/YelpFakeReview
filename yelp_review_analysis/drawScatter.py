#!/usr/bin/python
import math
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def drawScatter(x,y,outfile,suptitle =  '',xlabel = '',ylabel =  '',xlog = False,ylog = False):
	'''
	hist,bins = np.histogram(data,range = range,bins= bin)
	
	width = 0.7*(bins[1]- bins[0])
	center = (bins[:-1] + bins[1:])/2
	'''
	fig = plt.figure()
	fig.suptitle(suptitle,fontsize=14,fontweight='bold')
	plt.plot(x,y,',',color='black')	
	if xlog:
		plt.xscale('log')
	if ylog:
		plt.yscale('log')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	if outfile:
		plt.savefig(outfile,format = 'pdf')
	else:
		plt.show()

def drawHistogramBylogScale(data,bin,range,outfile,suptitle =  '',xlabel = '',ylabel =  ''):
	hist,bins = np.histogram(data,range = range,bins= bin)
	width = 0.7*(bins[1]- bins[0])
	center = (bins[:-1] + bins[1:])/2
	fig = plt.figure()
		
	fig.suptitle(suptitle,fontsize=14,fontweight='bold')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.bar(center,hist,align='center',width=width)
	plt.yscale('log',nonposy='clip')
	plt.xscale('log',nonposy='clip')
	plt.savefig(outfile,format = 'pdf')

if __name__ == '__main__':
	file = 'combine_normalized_pos.csv'
	data = loadNormalizedFile(file)
	bins = [ 50,100,200,500,700,1000,2000]
	range=(0,1)
	outfile = PdfPages('overall_startPos_histogram.pdf')
	for b in bins:
		drawhistogram(data,b,range,outfile) 
	outfile.close()
