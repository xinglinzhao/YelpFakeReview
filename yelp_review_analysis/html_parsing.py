#!/usr/bin/python
import sys
#from pysqlite2 import dbapi2 as sqlite
import urllib2
from bs4 import BeautifulSoup
from bs4.element import NavigableString,Comment,Tag

def findTargetTag(htmlblock,tag,attr=None,target=None):
	result = []
	#print(type(htmlblock))
	if type(htmlblock) == str:
		soup = BeautifulSoup(htmlblock)
	else:
		soup = htmlblock
	tags = soup.find_all(tag)
	for tag in tags: 
		recursiveParsing(tag,attr,target,result)
	return result	
def recursiveParsing(tag,attr,target,results):
	if isinstance(tag,Comment) or isinstance(tag,NavigableString):
		return None		
	else:
		c = tag.get(attr)
		if c:
			if target in ' '.join(c):
				results.append(tag)
		else:
			content = tag.contents
			if type(content) == list:
				for d in content:
					recursiveParsing(d,attr,target,results)
			else:
				recursiveParsing(content,attr,target,results)
			'''				
			elif type(content) == NavigableString:
				if target in  content.get('class'):
					return tag
				else:
					return None
			'''
		

if __name__ == '__main__':
	page = open('./pages/pages','r').read().strip()
	html = urllib2.urlopen(page).read()
	tags = findTargetTag(html,'div','class','search-result natural-search-result biz-listing-large')
	print(len(tags))	
	for t in tags:
		print(t)
	'''
	crawler = yelp_crawler('data')
	crawler.crawl(page)					
	'''
