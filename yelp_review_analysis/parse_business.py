#!/usr/bin/python

import os
import sys
import json
import glob
from json_generator import jsonIterator
from business import Business
from operator import itemgetter
def getCities(file):
	cities = set()
	itor = jsonIterator(file) 
	for rec in itor:
		for k,v in rec.items():
			if k == 'categories':
				for e in v:
					cities.add(e)
	return cities
# load the business records

def loadBusiness(file):
	res = {}
	for rec in jsonIterator(file):
		b = Business(rec)
		res[b.get('business_id')] = b
	return res	
if __name__ == '__main__':
	busifile = 'yelp_academic_dataset_business.json'
	buss = loadBusiness(busifile)
	cities = {}
	for k,v in buss.items():
		cities.setdefault(v.get('city'),0)
		cities[v.get('city')] += 1
	res = sorted(cities.items(),key = itemgetter(1),reverse=True)
	print(res)
	
	
