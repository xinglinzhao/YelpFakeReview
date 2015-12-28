#!/usr/bin/python

import os
import sys
import json
from dataStruct import dataStruct
from json_generator import jsonIterator
class User(dataStruct):
	def __init__(self,dictionary):
		dataStruct.__init__(self,dictionary)
	def __eq__(self,other):
		return type(other)==User and self.get('user_id') == other.get('user_id')
	def __hash__(self):
		return hash(self.get('user_id'))
if __name__ == '__main__':
	'''
	reviewfile = 'yelp_academic_dataset_user.json'
	itor = jsonIterator(reviewfile)
	n =  1
	for r in itor:
		u = User(r)
		print(u.get('user_id'))
	'''
	u1 = User({'user_id':21,'name' : 'mike'})
	u2 = User({'user_id':21,'name' : 'hello'})
	print(u1== u2)
