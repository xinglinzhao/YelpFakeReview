#!/usr/bin/python

from parse_business import loadBusiness
from operator import itemgetter
def countCities(business):
	res = {}
	for k,v in business.items():
		res.setdefault(v.get('city'),0)
		res[v.get('city')] += 1
	return sorted(res.items(), key = itemgetter(1),reverse=True)
def splitBusinessByCity(business,cities):
	res = {}
	for c in cities:
		res[c] = []
	res['others'] = []
	for k,v in business.items():

		other = True 
		for c in cities:
			if c.lower() in v.get('city').lower() :
				res[c].append(v)
				other = False		
				break
		if other:
			res['others'].append(v)
	return res


def outfile(prefix,business):
	for k,v in business.items():
		outhandler = open(prefix+'_'+''.join(k.split())+'.json','w')
		outhandler.write('\n'.join([e.__str__() for e in v]))
		outhandler.close()

def splitDrive():
	businessfile = 'yelp_academic_dataset_business.json'
	business = loadBusiness(businessfile)
	cities = countCities(business)
	city,freq = zip(*cities)
	print(cities)
	categories = city[0:13]
	print(categories)		
	outfilePre='final_business'
	split = splitBusinessByCity(business,categories)
	outfile(outfilePre,split)
if __name__ == '__main__':
	splitDrive()
