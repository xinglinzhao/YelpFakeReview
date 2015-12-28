#!/usr/bin/python
import json

class jsonIterator:
	def __init__(self,file):
		self.__file = file
		self.__handler = open(self.__file,'rU')
	def __iter__(self):
		return self
	def next(self):
		line = self.__handler.readline().strip()
		if line:
			return json.loads(line)
		else:
			raise StopIteration


if __name__ == '__main__':
	file = 'yelp_academic_dataset_business.json'
	itor = jsonIterator(file)
	n = 0
	for rec in itor: 
		print(rec)
		n += 1
		if n > 10:
			break

		
