#!/usr/bin/python
import math
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def drawhistogram(data,bin,range,outfile,xlogscale = False,ylogscale=False,suptitle =  '',xlabel = '',ylabel =  ''):
	hist,bins = np.histogram(data,range = range,bins= bin)
	
	width = 0.7*(bins[1]- bins[0])
	center = (bins[:-1] + bins[1:])/2
	fig = plt.figure()
	fig.suptitle(suptitle,fontsize=14,fontweight='bold')
		
	plt.bar(center,hist,align='center',width=width)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	if xlogscale:
		plt.xscale('log',nonposy='clip')
	if ylogscale:
		plt.yscale('log',nonposy='clip')
	if outfile:
		plt.savefig(outfile,format = 'pdf')

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
	if outfile:
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
