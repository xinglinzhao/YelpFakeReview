#!/usr/bin/python
import sys
from pysqlite2 import dbapi2 as sqlite
import urllib2
from bs4 import BeautifulSoup
from bs4.element import NavigableString,Comment,Tag
class yelp_crawler(object):
	def __init__(self,dbname):
		self.con = sqlite.connect(dbname)
	def __del__(self):
		self.con.close()
	def dbcommit(self):
		self.con.commit()
	def crawl(self,pages,depth=2):
		p = urllib2.urlopen(page)
		soup = BeautifulSoup(p.read())
#		structured = soup.prettify()
#		open('page.html','w').write(structured)
		divs = soup.find_all('div')
		target = "search-result natural-search-result biz-listing-large"
		for d in divs:
			part = self.recursiveParsing(d,target)
			if part:
				break
		print(part)
			
	def recursiveParsing(self,tag,target):
		
		if isinstance(tag,Comment):
			return None		
		elif isinstance(tag,NavigableString):
			if target in tag:
				return tag
			else:
				return None
		else:
			c = tag.get('class')
			if c:
				if target == ' '.join(c):
					return tag
			else:
				content = tag.contents
				if type(content) == list:
					for d in content:
						res =  self.recursiveParsing(d,target)
						if res:
							return res
				elif type(content) == NavigableString:
					if target in  content.get('class'):
						return tag
					else:
						return None
				else:
					return self.recursiveParsing(content,target)
				

if __name__ == '__main__':
	page = open('./pages/pages','r').read().strip()
	crawler = yelp_crawler('data')
	crawler.crawl(page)					
