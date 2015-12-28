#!/usr/bin/python

import os
import sys
import json
from json_generator import jsonIterator
class review(object):
	def __init__(self,votes,user_id,review_id,stars,date,text,type,business_id):
		self.__votes = votes
		self.__authorID = user_id		
		self.__reviewID = review_id
		self.__rating = stars
		self.__date = date
		self.__text = text
		self.__type = type
		self.__businessID = business_id
	def getReviewID(self):
		return self.__reviewID
	def getAuthor(self):
		return self.__authorID
	def getDate(self):
		return self.__date
	def getStars(self):
		return self.__rating
	def getType(self):
		return self.__text
	def getBusinessID(self):
		return self.__businessID
	def getVote(self):
		return self.__votes
	def __str__(self):
		res = {}
		res['votes'] = self.__votes
		res['user_id'] = self.__authorID
		res['review_id'] = self.__reviewID
		res['stars'] = self.__rating
		res['date'] = self.__date
		res['text'] = self.__text
		res['type'] = self.__type
		res['business_id'] = self.__businessID
		return json.dumps(res)

if __name__ == '__main__':
	reviewfile = 'yelp_academic_dataset_review.json'
	itor = jsonIterator(reviewfile)
	n =  1
	for r in itor:
		r = review(**r)
		print(r.getReviewID())
		print(r.getDate())
		print(r.__str__())
		break
