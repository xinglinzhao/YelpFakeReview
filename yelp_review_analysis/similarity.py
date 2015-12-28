#!/usr/bin/python

import numpy as np
import math
# eucludean distance
#1 means identical, 0 means is total different
def similarity_eu(p1,p2):
	sum_of_sq = 0.0
	common = False
	for k in p1:
		if k in p2:
			common = True
			break
	if not common:
		return 0.0
	sum_of_sq = sum([pow(p1[k] - p2[k],2) for k in p1 if k in p2])
	return 1.0/(sum_of_sq+1)

# pearsion correlation, 1 means identical, 0 means is total different
def similarity_pearson(p1,p2):
	common = set(set(p1.keys()).intersection(set(p2.keys())))
	# there is no common
	if len(common) <= 1:
		return 0.0
	n = len(common)
	# sum of each person
	sum1 = sum([p1[k] for k in common])
	sum2 = sum([p2[k] for k in common])

	# squre of sum for each person	
	sum1sq = sum([pow(p1[k],2) for k in common]) 
	sum2sq = sum([pow(p2[k],2) for k in common]) 
	
	# sum of cross product
	csum = sum([p1[k]*p2[k] for k in common])	
	# calculate the pearson correlation between two people
	top = csum - sum1*sum2/n
	bottom = math.sqrt((sum1sq - sum1*sum1/n)*(sum2sq - sum2*sum2/n))
	if bottom == 0:
		return 0.0	
	return top/bottom
# jaccard distance 
def similarity_jac(p1,p2):
	key1 = set(p1.keys())
	key2 = set(p2.keys())
	inter = key1.intersection(key2)
	union = key1.union(key2)
	if not union:
		return 0.0
	else:
		return float(len(inter))/len(union)	
# generalized jaccard distance
def similarity_gjac(p1,p2):
	key1 = set(p1.keys())
	key2 = set(p2.keys())
	union = key1.union(key2)
	if not union:
		return 0.0
	else:
		minsum = 0.0
		maxsum = 0.0
		for k in union:
			v1 = 0
			v2 = 0
			if k in key1:
				v1 = p1[k]
			if k in key2:
				v2 = p2[k]
			minsum += min(v1,v2)
			maxsum += max(v1,v2)	
		if maxsum == 0:
			return 0 
		return minsum/maxsum	
if __name__ == '__main__':
	p1 = {'1':4,'2':4,'4':4}
	p2 = {'1':2,'2':2,'4':2}
	print(similarity_eu(p1,p2),similarity_pearson(p1,p2),similarity_jac(p1,p2),similarity_gjac(p1,p2))

