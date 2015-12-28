#!/usr/bin/python

import pickle
import json
import sys
import urllib2
from bs4 import BeautifulSoup
from html_parsing import findTargetTag
from bs4 import NavigableString,Comment,Tag
from review_parser import review_parser
class business_parsing(object):
	def __init__(self):
		pass
	@staticmethod
	def parse(htmlblock):
		business = []
		while True:
			business += findTargetTag(htmlblock,'div','class','search-result natural-search-result biz-listing-large')	
			break
			nextpage = findTargetTag(htmlblock,'link','rel','next')
			if nextpage:
				print(nextpage[0],type(nextpage[0]))
				print(nextpage[0]['href'])
				htmlblock = urllib2.urlopen(nextpage[0]['href']).read()
			else:
				break
		return business
	@staticmethod
	def parse_each_business(soupblock):
		business = {}
		business['stars'] = business_parsing.getAverageStars(soupblock)
		link =  'http://www.yelp.com/' + soupblock.a['href']
		html =  BeautifulSoup(urllib2.urlopen(link).read())
		address = business_parsing.getAddress(soupblock)
		hours = business_parsing.getHours(html)	
		business['address'] = address
		business['Hours'] = hours
		business['business_id'] = business_parsing.getID(html)
		reviewlist = business_parsing.getReviews(html)
		for k,v in reviewlist.items():
			print(k,len(v))
		return (business,reviewlist) 
	@staticmethod
	def getAddress(soupblock):
		address = soupblock.find_all('address')
		address = list(address[0].children)[0].strip()
		return address
	@staticmethod
	def getHours(soupblock):
		table = findTargetTag(soupblock,'table','class','table table-simple hours-table')
		result = {}
		if not table:
			return result
		table = table[0]	
		for child in table.children:
			if type(child) == NavigableString:
				continue
			for c in child:
				if type(c) == Tag:
					day = c.th.contents[0]
					span = c.find_all('span')
					hour = [] 
					if span:
						for s in span:
							hour.append(s.contents[0])
					else:
						td = c.find_all('td')
						if td:
							for t in td:
								if type(t) == Tag:
									cont = t.contents[0].strip()
									if cont:
										hour = cont	
										break			
					result[day] = hour
		return result
	@staticmethod
	def getAverageStars(soupblock):
		candidates = findTargetTag(soupblock,'i','class','star-img stars_')
		stars = []
		for c in candidates:
			if type(c) == Tag and 'title' in c.attrs and 'star rating' in c['title']:
				stars.append(c['title'].split()[0])
		return stars
				
	@staticmethod
	def getID(soupblock):
		candidates = findTargetTag(soupblock,'div','class','lightbox-map hidden')
		for c in candidates:
			if type(c) == Tag and 'data-business-id' in c.attrs:
				return c['data-business-id']
				
	@staticmethod
	def getReviews(soupblock):
		filterLink = findTargetTag(soupblock,'a','class','subtle-text inline-block')
		print(filterLink)
		reviewList = {}
		if filterLink:
			for f in filterLink:
				if type(f) == Tag and 'class' in f.attrs:
					pages = BeautifulSoup(urllib2.urlopen('http://www.yelp.com' + f['href']).read())
					reviewList['filtered'] = business_parsing.getFilteredReviewsImp(pages)
					break
		reviewList['recommended'] = business_parsing.getReviewsImp(soupblock)
		return reviewList
	@staticmethod
	def getFilteredReviewsImp(soupblock):
		reviewList = []
		sourcelist = [soupblock]
		nextpage = findTargetTag(soupblock,'a','class','page-option available-number')
		print(len(nextpage))
		for p in nextpage:
			s = 'http://www.yelp.com' + p['href']
			sourcelist.append(BeautifulSoup(urllib2.urlopen(s).read()))
		for p in sourcelist:
			reviewblock = findTargetTag(p,'div','class','review-list')
			for l in reviewblock: 	
				tmp = findTargetTag(l,'div','class','review review--with-sidebar')

				reviewList += tmp
		return reviewList		
	@staticmethod
	def getReviewsImp(soupblock):
		reviewList = []
		while True:
			reviewblock = findTargetTag(soupblock,'div','class','review-list')
			for l in reviewblock: 	
				tmp = findTargetTag(l,'div','class','review review--with-sidebar')
				reviewList += tmp
			nextpage = findTargetTag(soupblock,'link','rel','next')
			
			if not nextpage:
				break
			nextpage = nextpage[0]['href']
			soupblock = urllib2.urlopen(nextpage).read()
		return reviewList 	
	
if __name__ == '__main__':
	page ='http://www.yelp.com/search?find_desc=Hotels&find_loc=Las+Vegas' 
	print(page)
	html = urllib2.urlopen(page).read()
	business = business_parsing.parse(html)
	output = open('business_block_hotel.txt','w')
	output_parsed = open('business_rec_hotel.txt','w')
	review_p = review_parser('review_block_hotel')
	for b in business:
		busi,reviews = business_parsing.parse_each_business(b)
		output.write(str(b))
		c =json.dumps(busi)
		output_parsed.write(c)
		review_p.parseReviews(reviews)	
	output.close()
	output_parsed.close()
	'''
	for b in business:
		output.write(str(b))
		
	output.close()		
	'''
