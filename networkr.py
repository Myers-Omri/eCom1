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




def create_graph(edges = None):
    '''create graph with all the edges that are in the list edges (which is constructed)
    from the csv file we received as input.

    Args:
        edges: list of lists in length 2 [source, target]
    Returns:
        G: a networkx graph data structure
        f_edge_list: The Complement graph of G
    '''
    if not edges:
        reso = open('initial_graph.dump', 'r')
        G = pickle.load(reso)
        reso.close()
        f_edge_list = make_future_edges()
    else:

        with open('user_artists.csv', 'rb') as csvfile:
            all_artist_data = list(csv.reader(csvfile))[1:]
        G = nx.Graph()
        users = {} # Dictionary where user IDs are kept as keys
        for edge in edges:
            users[edge[0]] = True
        nodes_to_add = []
        for u in all_artist_data:
            if not u[0] in users:
                users[u[0]] = True
                nodes_to_add.append(u[0])

        for (s, t) in edges:
            G.add_edge(s, t)
        G.add_nodes_from(nodes_to_add)
        res_f = open('initial_graph.dump', 'w')
        pickle.dump(G,res_f )
        res_f.close()
        f_edge_list = make_future_edges(G,users)


    return G, f_edge_list



class Network:
    # artist_IDs = ['70', '150', '989', '16326', '144882', '194647', '389445', '390392', '511147', '532992'] #List of artists to choose from
    # artist_IDs = ['150', '989',  '194647', '390392', '511147', '532992'] #List of artists to choose from

    """Class that reads the data from the files user_friends.csv and
    user_artists.csv into self.edges and self.user_artist_data,
    respectively. self.edges is a list of lists of size two that
    represent edges. user_artists.csv is a list of lists of size three
    [userID, artistID, times_was_heared]."""
    def __init__(self, my_artists=['150', '989',  '194647', '390392', '511147', '532992']):
        self.artist_IDs = my_artists
        with open('user_friends.csv', 'rb') as csvfile:
            self.edges = list(csv.reader(csvfile))[1:]
            print "edges done"
        with open('user_artists.csv', 'rb') as csvfile:
            all_artist_data = list(csv.reader(csvfile))[1:]
        self.user_artist_data = [x for x in all_artist_data if x[1] in self.artist_IDs]
        print "user_artist_data done"
        Gg, Cg = create_graph(self.edges)

        self.graph = Gg
        print "graph done"
        self.c_graph = Cg
        print "c_graph done"
        t_users = {}
        for user_n in Gg.nodes():
            name = user_n
            artists = self.get_artists(name) #TODO: implement
            t_users[name] = user.user(name, artists)
        self.users = t_users
        print "users done"
        self.cds_sold = 0
        self.art_analisys = {}
        for aa in self.artist_IDs:
            self.art_analisys[aa] = 0

    def get_artists(self, name):
        '''calculate how many time the users listened to the artist
        :param name: name of the user
        :return: dictionary {'artist_ID' : number of time listened}
        '''
        art_dic = {}
        for art_name in self.artist_IDs:
            art_dic[art_name] = 0

        for  u ,a,l in self.user_artist_data:
            if u == str(name):
                art_dic[a] += int(l)
                # print name, a, l
        return art_dic

    def update_edges(self):
        '''
        this function iterarte over the complement graph and check for every edge
        if we need to add it or not according to the probability and how many common friends.
        change the actual graph (Network.graph)
        :return: the number of edges that we added
        '''
        P = 0.02
        edges_to_add = []
        for e in self.c_graph.edges():
            l1 = set(self.graph.neighbors(e[0])) #get all neighbors of s
            l2 = set(self.graph.neighbors(e[1])) #get all neighbors of t
            lc = l1.intersection(l2)
            k = len(lc)
            prob = 1-pow((1-P), k)
            r = random()
            if r < prob:
                edges_to_add.append(e)
        self.graph.add_edges_from(edges_to_add)
        self.c_graph.remove_edges_from(edges_to_add)
        return len(edges_to_add)

    def move_time(self, n=1):
        '''
        clculate a time lap of the system calculate the new friendships and the CDs that users buy.
        the function only update the network at the end of the epoch.
        :param n: number of epochs to run
        :return: tuple of (num of CDs, num of edges, list of updates for the network.)
        '''
        for i in range(n):
            updates = []
            j = 0
            for u in self.users:
                j += 1
                r = str(j) + " \r"
                stdout.write(r)
                cur_friends = self.graph.neighbors(u)
                new_disks_names = self.users[u].calc_new_disk(cur_friends,self.users, self.artist_IDs)
                if len(new_disks_names) > 0:
                    updates.append((u,new_disks_names))
                    for d in new_disks_names:
                        self.art_analisys[d] += 1


            e_added = self.update_edges()
            # print e_added, "edges was added"
            tmp_sold=0
            for us,ds in updates:
                tmp_sold += len(ds)
                self.users[us].add_disks(ds)
                # print "user {} bought the following CDs".format(us), ds
            self.cds_sold += tmp_sold

            return tmp_sold, e_added, updates







if __name__ == '__main__':

    nc = Network()



