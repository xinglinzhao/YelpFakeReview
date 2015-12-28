#!/usr/bin/python

import numpy as np

import pickle
from user import User
from business import Business
from review import Review




def buildCountUserProduct(users,product,coded_user,coded_product):
	up = [ [] for k in users.keys()] 
	for bid,b in product.items():
		reviews = b.get('reviewers')
		for u,c in reviews.items():
			up[coded_user[u]].append((coded_product[bid],int(c)))
	return up


if __name__ == '__main__':
	users = pickle.load(open('user_pick.txt','r'))
	business = pickle.load(open('business_pick.txt','r'))
	coded_user = pickle.load(open('coded_users.txt','r'))
	coded_business = pickle.load(open('coded_business.txt','r'))
	mat = buildCountUserProduct(users,business,coded_user,coded_business)
		
	outfile = open('countUserProduct.csv','w')
	for row in mat:
		coded = [','.join([str(b),str(c)]) for b,c in row]
		outfile.write('|'.join(coded) + '\n')
	outfile.close()	
				
