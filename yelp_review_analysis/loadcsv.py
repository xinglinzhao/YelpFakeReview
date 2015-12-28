#!/usr/bin/python
from operator import itemgetter
def loadcsv(file):
	res = {}
	for line in open(file,'r'):
		line = line.strip()
		rec = line.split(',')
		res[rec[0]] = float(rec[1])
	return res
def sort_tuple(l):
	l.sort(key=itemgetter(1))
def loaddata(file):
	d = loadcsv(file)
	l = d.items()
	sort_tuple(l)
	return l 
if __name__ == '__main__':
	res = loaddata('oursbusiness_reliability.csv')
	print(len(res))
