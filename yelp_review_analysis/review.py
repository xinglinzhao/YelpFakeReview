#!/usr/bin/python

import os
import sys
import json
from dataStruct import dataStruct
from json_generator import jsonIterator
class Review(dataStruct):
	def __init__(self,data):
		dataStruct.__init__(self,data)
	def __eq__(self,other):
		return type(other) == Review and self.get('review_id') == other.get('review_id')
	def __hash__(self):
		return hash(self.get('review_id'))
if __name__ == '__main__':
	'''
	reviewfile = 'yelp_academic_dataset_review.json'
	itor = jsonIterator(reviewfile)
	for r in itor:
		re = review(r)
		print(re.get('review_id'))
		break
	'''
	r1 = Review({'review_id':'hello','stars':5})
	r2 = Review({'review_id':'hello','stars':6})
	print(r1== r2,r1.__hash__(),r2.__hash__())
