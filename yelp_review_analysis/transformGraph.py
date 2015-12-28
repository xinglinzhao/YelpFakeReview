#!/usr/bin/python

from user import User
from user_generator import loadUsers

# transform the network links into adjacent link data structure for later usage
def adjList(users):
	ulabels = range(len(users))
	ukeys = users.keys()
	pairs = zip(ukeys,ulabels)
	mapping = {}
	graph = []
	for k,v in pairs:
		mapping[k] = v
		graph.append([])
	for k,v in users.items():
		for f in v.get('friends'):
			graph[mapping[k]].append(mapping[f])
	return (mapping,graph)



# drive for the transformation
def transformNet2AdjList(userfile):
	users = loadUsers(userfile)
	return adjList(users)
	
if __name__ == '__main__':
	userfilename = 'user_full.json'
	users = loadUsers(userfilename)
	mapping,graph = adjList(users)
	ind = -1 
	for v in graph:
		if len(v) > 10:
			break
		ind += 1
	validate = []
	key = users.keys()[ind]
	validate.append(key)
	validate += users[key].get('friends')
	for f in validate:
		print(mapping[f])
	print(ind,graph[ind])	
