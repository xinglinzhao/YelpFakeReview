#!/usr/bin/python

import os
import sys
import json
from dataStruct import dataStruct
from json_generator import jsonIterator
class Business(dataStruct):
	def __init__(self,data):
		dataStruct.__init__(self,data)
	def __eq__(self,other):
		return type(other) == Business and other.get('business_id') == self.get('business_id')
	def __hash__(self):
		return hash(self.get('business_id'))
if __name__ == '__main__':
	reviewfile = 'yelp_academic_dataset_business.json'
	itor = jsonIterator(reviewfile)
	for r in itor:
		re = Business(r)
		print(re.get('business_id'))
		break
