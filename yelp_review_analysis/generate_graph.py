#!/usr/bin/python

import pickle
from user import User
def make_user_graph(data,hashtable,weight=None):
	graph = {} 
	total = 0
	for uid,u in data.items():
		for other in u.get('friends'):
			graph.setdefault(hashtable[uid],set())
			graph[hashtable[uid]].add(hashtable[other])
			total += 1
	print(total)
	return graph


def drive():
	users = pickle.load(open('user_pick.txt','r'))
	coded = pickle.load(open('coded_users.txt','r'))
	g = make_user_graph(users,coded)
	pickle.dump(g,open('user_graph.txt','w'))


if __name__ == '__main__':
	drive()	
