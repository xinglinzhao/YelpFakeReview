#!/usr/bin/python

import os
import sys
from json_generator import jsonIterator
from operator import itemgetter 
from user import User
import resource
from parse_review import loadReviewByAuthor
from drawHistogram import drawHistogramBylogScale as drawHist
import math

#page ranking scoring function

def starsScore(values):
	total = 0
	for v in values:
		total += v/5
	return total	

# given the user file
# load the users information into a dictionary
def loadUsers(file):
	res = {}
	for user in jsonIterator(file):
		tmpu = User(user)
		res[tmpu.get('user_id')] = tmpu
	return res
# calculate the importance of each users given the popularity function and attributes of the user 
def pageRanking(iterations,users,func,attributes,initP=0.15,trans = 0.85):
	for k,v in users.items():
		values = [v.get(attr) for attr in attributes]
		v.set('popularity',initP*func(values))
	for i in range(iterations):
		for k,v in users.items():
			friends = v.get('friends')
			numFriends = len(friends)
			for f in friends:
				users[f].set('popularity',users[f].get('popularity') + trans*v.get('popularity')/numFriends)
		
# calculate the importance of each users given the popularity function and attributes of the user 
def pageRanking_user(iterations,users,initP=0.15,trans = 0.85):
	for k,v in users.items():
		v.set('popularity',1)
	for i in range(iterations):
		for k,v in users.items():
			friends = v.get('friends')
			numFriends = len(friends)
			for f in friends:
				users[f].set('popularity',users[f].get('popularity') + trans*v.get('popularity')/numFriends)
# find all connected components and its size	
def identifyComponents(users):
	components = []
	checked = set()
	for k,v in users.items():
		if not k in checked:
			dfs(k,users,checked,components,1)
	com = sorted(components,key=itemgetter(1))
	return com
# do depth-first-search on single node
# if this node is the last one to be visited in its connected component
# then it will be set as the root of this connected component 				
def dfs(user_id,users,checked,components,count):
	if user_id in checked:
		return
	checked.add(user_id)
	end = True
	for f in users[user_id].get('friends'):
		if not f in checked:
			dfs(f,users,checked,components,count+1)
		else:
			end = False
	if end:
		components.append((user_id,count))
def outputComponents(component,file):
	handler = open(file,'w')
	cont = []
	for root,count in component:
		cont.append('%s,%s\n'%(root,count))

	handler.write('\n'.join(cont))
	handler.close()		
# find those isolate users that are not friends of any other friends or does not have any friend
def findIsolateUsers(users):
	candidates = set(users.keys())
	for k,v in users.items():
		if len(v.get('friends')) > 0 and k in candidates:
			candidates.remove(k)
		for f in v.get('friends'):
			if f in candidates:
				candidates.remove(f)
	return candidates	
# check if the friends are mutually include each other
def isMutual(users):
	for k,v in users.items():
		for f in v.get('friends'):
			if not k in users[f].get('friends'):
				print(k,v.get('friends'))
				print(f,users[f].get('friends'))
				return False
	return True
# for each reviewer,  add its own review ids and the businessIDs that they write review for
def addReviewIDAndBusinessID(users,reviews):
	for k,v in users.items():
		myreviews = reviews[v.get('user_id')]
		reviewCount = int(v.get('review_count'))
		myreviewids = [(e.get('review_id'),e.get('business_id')) for e in myreviews]
		ids = zip(*myreviewids)
		v.set('myreviews',ids[0])
		businesslog = {}
		for bid in ids[1]:
			businesslog.setdefault(bid,0)
			businesslog[bid] += 1
		v.set('business_exp',businesslog)
# drive for updating the reviewid and business id 
def updateDrive(userfile,reviewfile,finalUserFile):
	reviews = loadReviewByAuthor(reviewfile)
	users = loadUsers(userfile)
	addReviewIDAndBusinessID(users,reviews)
	cont = [v.__str__() for v in users.values()]
	open(finalUserFile,'w').write('\n'.join(cont)) 
def normalized(userfile):
	users = loadUsers(userfile)
	maxScore= 0
	for k,v in users.items():
		if v.get('popularity') > maxScore:
			maxScore = v.get('popularity')
	popularityScores = [v.get('popularity')/maxScore for v in users.values()]
	bin = 100	
	filename = 'popularity_score_hist_loglog.pdf'
	drawHist(popularityScores,bin,(0,1),filename)		
def comparePopularity(a):
	return a.get('popularity')

# find the indegree and oudegree of the given users
def findIndegreeAndOutdegree(users,u):
	indegree = 0
	outdegree = 0
	for k,v in users.items():
		if u in map(str,v.get('friends')):
			indegree += 1
		if u == k:
			outdegree = len(v.get('friends'))
	Return (indegree,outdegree)

# match the number of review_count in the users record against the review number in the review records
def review_countMatch(users,reviews):
	total_review = 0
	for k,v in users.items():
		total_review += int(v.get('review_count'))
	review_record = len(open(reviews,'r').read().split('\n'))
	return (total_review,review_record,total_review-review_record)	

	
	
if  __name__ == '__main__':
	
	resource.setrlimit(resource.RLIMIT_STACK,(2**29,-1))
	sys.setrecursionlimit(10**6)
	
	'''
	updatedUserFile = 'final_user.json'
	iterations = 20
	users = loadUsers(updatedUserFile)		
	pageRanking_user(iterations,users,initP=0.15,trans = 0.85)
	userList = users.values()
	sortedv = sorted(userList,key = comparePopularity,reverse=True)
	cont = [v.__str__() for v in sortedv]
	userfile = 'user_full.json'
	open(userfile,'w').write('\n'.join(cont))
	#print(isMutual(users))
	isolatedUsers = findIsolateUsers(users)
	isolatedfile = 'isolatedUsers.csv'
	with open(isolatedfile,'w') as handler:
		handler.write('\n'.join(list(isolatedUsers)))
	#components = identifyComponents(users)
	#outfile = 'component_info.csv'
	#outputComponents(components,outfile)	
	finalUserfile = 'final_user.json'
	#normalized(updatedUserFile)
	reviewfile = 'yelp_academic_dataset_review.json'
	updateDrive(updatedUserFile,reviewfile,finalUserfile)
	'''
	userfile = 'user_full.json'
	users = loadUsers(userfile)
	review = 'yelp_academic_dataset_review.json'
	print(review_countMatch(users,review))



