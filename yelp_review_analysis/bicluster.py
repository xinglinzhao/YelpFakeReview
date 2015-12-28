#!/usr/bin/python

class bicluster(object):
	def __init__(self,id,left=None,right=None,distance=0.0):
		self.left = left
		self.right = right
		self.distance = distance
		self.id = id
	def getLeaves(self):
		if self.id < 0:
			return self.left.getLeaves() + self.right.getLeaves()
		else:
			return [self.id]


if __name__ == '__main__':
	leftleft = bicluster(0)
	leftright = bicluster(1)
	rightleft = bicluster(2)
	rightright = bicluster(3)
	right = bicluster(-3,rightleft,rightright)
	left = bicluster(-4,leftleft,leftright)
	root = bicluster(-5,left,right)
	print(root.getLeaves())
