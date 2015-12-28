#!/usr/bin/python
from user import User
from user_generator import loadUsers
from transformGraph import adjList
# find those connected component for users
import pdb
# find the connected component for the users in the yelp data
# input a list of list , each element in the grand list contain all nodes that it connects to 
class unionFind(object):
	ids = []
	# find one nodes root
	@staticmethod	
	def findRoot(id):
		path = []
		while not id == unionFind.ids[id]:
			#path compression
			unionFind.ids[id] = unionFind.ids[unionFind.ids[id]]	
			id = unionFind.ids[id]
		return id
	# check if two nodes are in same components by checking their roots are same or not
	@staticmethod
	def checkConnected(p,q):
		return unionFind.findRoot(p) == unionFind.findRoot(q)
	# if they are not connected yet, 
	@staticmethod
	def unite(p,q):
		rootp = unionFind.findRoot(p)
		rootq = unionFind.findRoot(q)
		if rootp < rootq:
			unionFind.ids[rootq] = rootp
		else:
			unionFind.ids[rootp] = rootq	
	# find the connected component for a graph in  adjacent matrix  representation
	@staticmethod
	def identifyComponent(adjacentMat):
		#pdb.set_trace()
		unionFind.ids = range(len(adjacentMat))
		# go through each edge, connect them and rewind their parents into the same parents
		for idx in range(len(adjacentMat)):
			for l in adjacentMat[idx]:
				if not unionFind.checkConnected(idx,l):
					unionFind.unite(idx,l)
		# now in ids array, each position represent a node label, its value represents its parents
		# so to cluster those nodes by their parents, we just need to convert ids array into a dictionary, key = parents, value = list of its children
		res = {}
		for ind in range(len(unionFind.ids)):
			root = unionFind.findRoot(unionFind.ids[ind])
			if ind ==  root:
				res.setdefault(unionFind.ids[ind],[])
				res[ind].append(ind)
			else:
				res.setdefault(root,[])
				res[root].append(ind)
		return res
	
if __name__ == '__main__':
	'''
	userfile = 'user_full.json'
	users = loadUsers(userfile)
	
	mapping,graph = adjList(users)
	compo = unionFind.identifyComponent(graph)
	'''
	graph = [[1],[],[3],[1],[],[4]]	
	print(unionFind.identifyComponent(graph))
			
						
		
				
	
		
		
