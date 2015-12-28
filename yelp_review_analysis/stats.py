#!/usr/bin/python

import numpy as np

def variance(dictionary):
	res = {}
	for k,v in dictionary.items():
		res[k] = np.var(v)
	return res


if __name__ == '__main__':
	data = {'hello':[1,2,3],'world':[3,4,5]}
	print(variance(data)) 
