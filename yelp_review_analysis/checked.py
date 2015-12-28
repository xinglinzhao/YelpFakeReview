#!/usr/bin/python

if __name__ == '__main__':
	checked = set()
	for line in open('ids.txt','r'):
		if line.strip() in checked:
			print('duplicate id ' + line)
			break
		else:
			checked.add(line.strip())
