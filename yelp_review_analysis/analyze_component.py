#!/usr/bin/python
from user import User
from user_generator import loadUsers
from identifyComponents import parseComponents,parseNodeLabels
import os


# given a components, find those users only point to other users but no users points to them
def findUnlinkedUser(users,component,mappings):
	res = set(map(lambda x: mappings[x],component))
	for i in component:
		for f in  users[mappings[i]].get('friends'):
			if f in res:
				res.remove(f)
	return list(res)
#given a components, find those users that has no friends, but is friend of other users
def findInlinkedUser(users,component,mapping):
	res = set(map(lambda x: mapping[x],component))
	for i in component:
		if len(users[mapping[i]].get('friends')) != 0 and mapping[i] in res:
			res.remove(mapping[i])
	return res

def findOnewayUsers(userfile,mapingfile,componentfile):
	users = loadUsers(userfile)
	mappings = parseNodeLabels(mapingfile)
	components = parseComponents(componentfile)
	maxlen = 0
	maxc = ''
	for k,v in components.items(): 	
		if len(v) > maxlen:
			maxlen = len(v)
			maxc = k
	maxComponent = components[maxc]
	outboundusers = findUnlinkedUser(users,maxComponent,mappings)
	inboundusers = findInlinkedUser(users,maxComponent,mappings)
	return (outboundusers,inboundusers) 

if __name__ == '__main__':
	userfile = 'user_full.json'
	mappfile = 'user_id_node.csv'
	userComponent = 'user_component.csv'
	outuser,inusers = findOnewayUsers(userfile,mappfile,userComponent)
	print(outuser,inusers)		
