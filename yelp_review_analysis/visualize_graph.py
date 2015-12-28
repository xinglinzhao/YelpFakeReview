#!/usr/bin/python

import pickle
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def make_graph(file):
	edges = pickle.load(open(file,'r'))
	graph = nx.DiGraph()
	for k,v in edges.items():
		graph.add_node(k)
		for o in v:
			graph.add_node(o)
			graph.add_edge(k,o)
	return (graph,edges)				
def component_graphs(graph,edges,directed=True):
	ugraph = graph.to_undirected()
	cc = nx.connected_components(ugraph)
	components = []
	for n in cc:
		graph = generate_component(edges,n,directed)
		components.append(graph)
	return components
def draw(outfile,graph):
	nx.draw(graph)
	plt.savefig(outfile,format='pdf')		
	plt.clf()
def generate_component(edges,node,directed):
	if directed:
		graph = nx.DiGraph()
	else:
		graph = nx.Graph()
	contained_node = set(node)
	for n in node:
		graph.add_node(n)
		if not n in edges:
			continue
		for o in edges[n]:
			if o in contained_node:
				graph.add_edge(n,o)
	return graph	

if __name__=='__main__':
	file = 'user_graph.txt'
	smallfile = PdfPages('small_components.pdf')
	bigfile = PdfPages('biggest_component.pdf')
	graph,edges = make_graph(file)
	compo = component_graphs(graph,edges,True)
	for c in compo[1:]:
		if len(c) > 1:
			draw(smallfile,c)	
	smallfile.close()
	draw(bigfile,compo[0])
	bigfile.close()		
