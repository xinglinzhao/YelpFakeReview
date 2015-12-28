#!/usr/bin/python

from union_find import unionFind
from transformGraph import adjList
from user import User
from user_generator import loadUsers

# find all connected components for the users's social network
def identifyComponents(userfile):
	users = loadUsers(userfile)
	mapping,graph = adjList(users)
	components = unionFind.identifyComponent(graph)
	return (mapping,components)
# output the components into two files
# 1 is dictionary of the user_id -- node number 
# 2 is the components it self in the node number notation
def outputComponents(mapping,components,name2label,componentsfile):
	tuples = mapping.items()
	open(name2label,'w').write('\n'.join(map(lambda x: '%s,%s'%(x[0],x[1]),tuples)))
	tuples = map(lambda x: '%s,%s'%(x[0],','.join(map(str,x[1]))),components.items())
	open(componentsfile,'w').write('\n'.join(tuples))
def parseComponents(file):
	res = {}
	for line in open(file,'r'):
		rec = line.rstrip().split(',')
		res[rec[0]] = rec[1:]
	return res
def parseNodeLabels(file):
	res = {}
	for line in open(file,'r'):
		rec = line.strip().split(',')
		res[str(rec[1])] = rec[0]
	return res	
if __name__ == '__main__':
	userfile = 'user_full.json'
	mapping,components = identifyComponents(userfile)
	print(len(components))
	name2label = 'user_id_node.csv'
	componentfile = 'user_component.csv'
	outputComponents(mapping,components,name2label,componentfile)
	
		
	
