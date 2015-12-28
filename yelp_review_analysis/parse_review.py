#!/usr/bin/python

import os
import sys
import json
import glob
from json_generator import jsonIterator
from review import Review
def getReviewStars(file,threshold):
	review = set()
	itor = jsonIterator(file) 
	for rec in itor:
		if float(rec['stars']) >= threshold:
			review.add(rec['user_id'])	
	return review 
# load the review records, by the author ID
# return a dictionary with key = author ID, value = instance of review class
def loadReviewByAuthor(file):
	res = {}
	for r in jsonIterator(file):
		review = Review(r)
		res.setdefault(review.get('user_id'),[])
		res[review.get('user_id')].append(review)	
	return res
# load the review file by the key specified key

def loadReview(file,attribute):
	res = {}
	for r in jsonIterator(file):
		review = Review(r)
		res.setdefault(review.get(attribute),[])
		res[review.get(attribute)].append(review)
	return res
# load the review records by the review ID
# return a dictionary with key = review ID, value = instance of review class 		
def loadReviewByRe(file):
	res = {}
	for r in jsonIterator(file):
		review = Review(r)
		res[review.get('review_id')]	=  review
	return res
# load the review records by the review ID
if __name__ == '__main__':
	directory = '*.json'
	for f in glob.glob(directory):
		if 'review' in f:
			print(len(getReviewStars(f,5)) )
