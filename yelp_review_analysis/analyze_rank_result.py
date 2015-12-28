#!/usr/bin/python

from json_generator import jsonIterator
from operator import itemgetter
from user import User

#find the top 10 user and bottom m users

def findUsers(file,top,bottom):
	users = []
	for u in jsonIterator(file):
		users.append((u,u.get('popularity')))
	users.sort(key=itemgetter(1))
	if top < len(users) and bottom < len(users):
		users = zip(*users)[0]
		topusers = users[len(users) - top:]
		bottomusers = users[:bottom]
	return (topusers,bottomusers)


if __name__ == '__main__':
	top = 10
	bottom = 10
	userfile = 'updated_user.json'
	topusers,bottomusers = findUsers(userfile,top,bottom)
	outfile = 'top_user.json'
	open(outfile,'w').write('\n'.join([e.__str__() for e in topusers]))
	outfile = 'bottom_user.json'
	open(outfile,'w').write('\n'.join([e.__str__() for e in bottomusers]))
