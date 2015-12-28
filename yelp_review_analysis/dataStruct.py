#!/usr/bin/python

import os
import sys
import json
from json_generator import jsonIterator
class dataStruct(object):
	def __init__(self,data):
		self.dict = data
	def get(self,attr):
		if attr in self.dict:
			return self.dict[attr]
		else:
			return None
	def set(self,attr,value):
		self.dict[attr] = value
	def __str__(self):
		return json.dumps(self.dict)
	def keys(self):
		return self.dict.keys()

if __name__ == '__main__':
	reviewfile = 'yelp_academic_dataset_review.json'
	itor = jsonIterator(reviewfile)
	for r in itor:
		re = review(r)
		print(re.get('review_id'))
		break
