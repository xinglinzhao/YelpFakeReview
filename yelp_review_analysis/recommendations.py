#!/usr/bin/python
from similarity import similarity_eu,similarity_jac,similarity_pearson,similarity_gjac
from operator import itemgetter

# find the top similar person given a people using the predefined similarity function 
def topMatch(prefs,person,n=5,sim_func=similarity_gjac):
	# calculate all similar scores with other people
	scores = [(other,sim_func(prefs[person],prefs[other])) for other in prefs.keys() if other != person]
	# sort it in desending order
	scores.sort(key = itemgetter(1),reverse=True)
	
	return scores[0:n]
#recommend the business for the people using other matched people's taste
# also guess the rating for the people recommended

def recommendation_engine(prefs,person,threshold = 4,sim_func = similarity_gjac):
	# total rating score for those business that this person has not tried yet	
	totals = {}
	# total rating weighted by the similar scores between this person and other users 
	simSums = {}
	myprefs = prefs[person].keys()
	for other , pref in prefs.items():
		if other == person:
			continue
		sim_score = sim_func(prefs[person],pref)
		if sim_score <= 0:
			continue
		for item,rating in pref.items():
			if not item in myprefs:
				totals.setdefault(item,0.0)
				simSums.setdefault(item,0.0)
				totals[item] += rating*sim_score
				simSums[item] += sim_score
	recList = []
	for item,total in totals.items():
		score = total/simSums[item]
		if score >= threshold:
			recList.append((score,item))
	recList.sort(reverse=True)
	return recList	
	 
if __name__ == '__main__':
	import pickle
	prefs = pickle.load(open('preference_pick.txt','r'))
	person = prefs.keys()[10]
	print(topMatch(prefs,person))
	print(recommendation_engine(prefs,person))
	
	
