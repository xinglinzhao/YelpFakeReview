#!/usr/bin/python
from bicluster import bicluster
from distance import *
import pickle
from multiprocessing import Process
def calculate_distance(prefs,ids,start,outfile,distance):
	pair_distance = {}
	length = len(prefs)
	handler = open(outfile,'w')
	for i in range(start,length):
		j = i + 1
		while j < length:
			score =distance(prefs[ids[i]],prefs[ids[j]])
			if score < 1: 
				pair_distance[(i,j)] = score
			j+=1
		for k,v in pair_distance.items():
			handler.write(','.join([str(k[0]),str(k[1]),str(v)]) + ',')
		pair_distance = {}
	handler.close()

def parallel_calculation(prefs,ids,outprefix,n = 15,distance=distance_gjac):
	bucketsz = len(prefs)/n
	starts = []
	for i in range(n):
		starts.append(i*bucketsz)
	prcs = []
	for s in starts:
		p = Process(target=calculate_distance,args=(prefs,ids,s,outprefix+'_'+str(s),distance))
		prcs.append(p)
		p.start()
	for p in prcs:
		p.join()	

def cluster_distance(cl1,cl2,pairScore):
	leaves1 = cl1.getLeaves()
	leaves2 = cl2.getLeaves()

	score = 0.0
	if not leaves1 or not leaves2:
		return score
	for id1 in leaves1:
		for id2 in leaves2:
			if id1 < id2:
				if (id1,id2) in pairScore:
					score += pairScore[(id1,id2)]
			else:
				if (id2,id1) in pairScore:
					score += pairScore[(id2,id1)] 
	return score/(len(leaves1)*len(leaves2))			



# build the cluster tree using the hirarchical clustering method
def hcluster(prefs,pairScore,tid,distance):
	distance = {}
	currentclustid = -1
	# initialize the clust with each node as a cluster
	clust = [bicluster(tid[item]) for item in prefs.keys()]
	# stop until there is only one cluster left	
	while len(clust) > 1:
		lowestpair = (0,1)
		closest = distance(clust[0],clust[1],pairScore)
		# find the closest cluster in this nested loop (O(n**2))
		for i in range(len(clust)):
			for j in range(i+1,len(clust)):
				if (clust[i].id,clust[j].id) not in distance:
					distance[(clust[i].id,clust[j].id)] = distance(clust[i],clust[j],pairScore)
				d = distance[(clust[i].id,clust[j].id)]
				if d < closest:
					closest = d
					lowestpair = (i,j)
		# create the new cluster using the two closest clusters found
		newcluster = bicluster(currentclustid,left=clust[lowestpair[0]],right=clust[lowestpair[1]],distance=closest)
		currentclustid -= 1
		del clust[lowestpair[0]]
		del clust[lowestpair[1]]
		clust.append(newcluster)
	return clust[0]
def writeTree(root,outfile):
	if root:
		outfile.write('%s,%s,%s,%s\n'%(root.id,root.left.id,root.right.id,root.distance))
		writeTree(root.left,outfile)
		writeTree(root.right,outfile)

def loadTree(infile,prefs,tid):
	tree = {} 
	root = None
	for line in open(infile,'r'):
		c = bicluster(*(line.strip().split(',')))
		tree[c.id] = c
	for cid,c in tree:
		leftid = int(c.left)
		if leftid < 0:
			c.left = tree[int(c.left)]
		else:
			c.left = None
		c.right = tree[int(c.right)]	
	
	return root				
def drive(prefs,pairScore,tid,outfile,distance=cluster_distance):
	root = hcluster(prefs,pairScore,tid,distance)
	handler = open(outfile,'w')
	writeTree(root,handler)
	handler.close()
if __name__ == '__main__':
	ids = pickle.load(open('coded_business.txt','r'))
	tids = {}
	for k,v in ids.items():
		tids[v] = k	
	prefs = pickle.load(open('business_preference_pick.txt','r'))
	parallel_calculation(prefs,tids,'business_pair_distance',15)
