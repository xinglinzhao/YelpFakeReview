#!/usr/bin/python
import numpy as np
from scoreObject import scoreObject
class pageRanker(object):
	def __init__(self,stop,trans,iteration):
		self.stop = 0.15
		self.trans = 0.85
		self.iteration = iteration
	def pageRanking(self,links,importanceMeasure):
		self.getInitValues(links,importanceMeasure)
		self.iterateCalculate(links,importanceMeasure)
	# initialize the importance score for each node	
	def getInitValues(self,links,importanceMeasure):
		length = len(links)
		self.scores = {}
		if length:
			for k,v in links:
				self.scores[k] = 1/length
	def iterateCalculation(self,links,importanceMeasure):
		for i in range(self.iteration):
						
