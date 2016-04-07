__author__ = 'omrim'

import user
import networkx as nx
import csv
from sys import stdout
import cPickle as pickle





def make_future_edges(g=None,users=None):
    '''create a graph with all the edges that are not in the original graph
    iterate the list of the users and for every user adds all the edges that are not already in
    the original graph.

    Args:
        g: The original graph as we created it according to the given csv
        users: Dictionary of the users.
    Returns:
        f_f_edge_list: The Complement graph of g
    '''

    if not g :
        res = open('other_edges.dump', 'r')
        f_edge_list = pickle.load(res)
        res.close()
    else:
        f_edge_list = nx.Graph()
        i=0
        for u in users:
            for f in users:
                if (not f == u) and (not (f in g.neighbors(u))):
                    f_edge_list.add_edge(u, f)
            i+=1
            r = str(i) + "\r"
            stdout.write(r)

        res_f = open('other_edges.dump', 'w')
        pickle.dump(f_edge_list,res_f )
        res_f.close()

    return f_edge_list




def create_graph(edges_file = None):

    if not edges_file :
        reso = open('other_edges.dump', 'r')
        G = pickle.load(reso)
        reso.close()
        res = open('other_edges.dump', 'r')
        f_edge_list = pickle.load(res)
        res.close()

    with open(edges_file, 'rb') as csvfile:
        edges = list(csv.reader(csvfile))
    G = nx.Graph()
    users = {} # Dictionary where user IDs are kept as keys
    for edge in edges:
        users[edge[0]] = True
    for (s, t) in edges:
        G.add_edge(s, t)

    out_edges_g = make_future_edges(G,users)

    out_edges = out_edges_g.number_of_edges()
    if out_edges == (len(users)*(len(users)-1)/2 - G.number_of_edges()):
        print "ok len is " ,out_edges
    else:
        print "fail le is: ", out_edges
        print "instead of:", (len(users)*(len(users)-1)/2 - G.number_of_edges())
    return G



if __name__ == '__main__':
    Gg = create_graph('user_friends.csv')

    print Gg.number_of_edges(), Gg.number_of_nodes()



