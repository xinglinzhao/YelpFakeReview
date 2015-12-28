#!/usr/bin/python

from html_parsing import findTargetTag
from bs4 import NavigableString,Comment,Tag
from bs4 import BeautifulSoup
import urllib2


class review_parser(object):
	def __init__(self,outfile):
		self.recommended = open(outfile+'_recommended.txt','w')
		self.filtered = open(outfile+'_filtered.txt','w')
	def parseReviews(self,blockList):
		recommend = blockList['recommended']
		self.parseRecommendedReview(recommend)	
		
		filtered = blockList['filtered']
		self.parseFilteredReview(filtered)
	def parseRecommendedReview(self,block):
		self.recommended.write('\n'.join(map(str,block)))
			
	def parseFilteredReview(self,block):
		self.filtered.write('\n'.join(map(str,block)))
	def __del__(self):
		self.recommended.close()
		self.filtered.close()

if __name__ == '__main__':
	#t = review_parser('review_block_filtered.txt')
	#t.parseReviews({'recommended':[],'filtered':[]})
	file = 'review_block_filtered.txt'
	txt = open(file,'r').read()
	print(len(txt))
	soup  = BeautifulSoup(txt)
	print(soup.prettify())
	reviews = findTargetTag(soup,'div','class','review review--width-sidebar')
	print(len(reviews))

		
