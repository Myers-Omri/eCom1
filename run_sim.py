__author__ = 'omrim'

import user
import networkx as nx
import csv
from sys import stdout
import cPickle as pickle
from random import random




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
        reso = open('initial_graph.dump', 'r')
        G = pickle.load(reso)
        reso.close()
        f_edge_list = make_future_edges()
    else:
        with open(edges_file, 'rb') as csvfile:
            edges = list(csv.reader(csvfile))
        G = nx.Graph()
        users = {} # Dictionary where user IDs are kept as keys
        for edge in edges:
            users[edge[0]] = True
        for (s, t) in edges:
            G.add_edge(s, t)
        res_f = open('initial_graph.dump', 'w')
        pickle.dump(G,res_f )
        res_f.close()
        f_edge_list = make_future_edges(G,users)

        # out_edges = out_edges_g.number_of_edges()
        # if out_edges == (len(users)*(len(users)-1)/2 - G.number_of_edges()):
        #     print "ok len is " ,out_edges
        # else:
        #     print "fail le is: ", out_edges
        #     print "instead of:", (len(users)*(len(users)-1)/2 - G.number_of_edges())
        #

    return G, f_edge_list

def update_edes(G, Cg):
    P = 0.02
    edges_to_add = []
    for e in Cg.edges():
        l1 = set(G.neighbors(e[0])) #get all neighbors of s
        l2 = set(G.neighbors(e[1])) #get all neighbors of t
        lc = l1.intersection(l2)
        k = len(lc)
        prob = 1-pow((1-P), k)
        r = random()
        if r<prob:
            edges_to_add.append(e)
    G.add_edges_from(edges_to_add)
    Cg.remove_edges_from(edges_to_add)
    return len(edges_to_add)

class Network:
    """Class that reads the data from the files user_friends.csv and
    user_artists.csv into self.edges and self.user_artist_data,
    respectively. self.edges is a list of lists of size two that
    represent edges. user_artists.csv is a list of lists of size three
    [userID, artistID, times_was_heared]."""
    def __init__(self):
        with open('user_friends.csv', 'rb') as csvfile:
            self.edges = list(csv.reader(csvfile))
        with open('user_artists.csv', 'rb') as csvfile:
            self.user_artist_data = list(csv.reader(csvfile))
        Gg, Cg = create_graph()
        self.graph = Gg
        self.c_graph = Cg
        users = {}
        for edge in net.edges:
            name = edge[0]
            artists = get_artists() #TODO: implement
            users[name] = user.user(name, artists)
            

if __name__ == '__main__':
    # Gg, Cg = create_graph('user_friends.csv')
    Gg, Cg = create_graph()
    print Gg.number_of_edges(), Cg.number_of_edges()
    # update_edes(Gg,Cg)
    # print Gg.number_of_edges(), Cg.number_of_edges()

    net = Network()
    users = {} # Dictionary where user IDs are kept as keys
    for u in net.user_artist_data:

        users[u[0]] = True



