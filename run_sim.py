__author__ = 'omrim'

import user
import networkx as nx
import csv
from sys import stdout
import cPickle as pickle
from random import random
from analytics import find_best
from datetime import datetime,time, timedelta



results_file = open('res_file.txt', 'w')

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
        with open('user_artists.csv', 'rb') as csvfile:
            all_artist_data = list(csv.reader(csvfile))
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

        # out_edges = out_edges_g.number_of_edges()
        # if out_edges == (len(users)*(len(users)-1)/2 - G.number_of_edges()):
        #     print "ok len is " ,out_edges
        # else:
        #     print "fail le is: ", out_edges
        #     print "instead of:", (len(users)*(len(users)-1)/2 - G.number_of_edges())
        #

    return G, f_edge_list



class Network:
    # artist_IDs = ['70', '150', '989', '16326', '144882', '194647', '389445', '390392', '511147', '532992'] #List of artists to choose from
    artist_IDs = ['150', '989',  '194647', '390392', '511147', '532992'] #List of artists to choose from

    """Class that reads the data from the files user_friends.csv and
    user_artists.csv into self.edges and self.user_artist_data,
    respectively. self.edges is a list of lists of size two that
    represent edges. user_artists.csv is a list of lists of size three
    [userID, artistID, times_was_heared]."""
    def __init__(self):
        with open('user_friends.csv', 'rb') as csvfile:
            self.edges = list(csv.reader(csvfile))
            print "edges done"
        with open('user_artists.csv', 'rb') as csvfile:
            all_artist_data = list(csv.reader(csvfile))
        self.user_artist_data = [x for x in all_artist_data if x[1] in Network.artist_IDs]
        print "user_artist_data done"
        Gg, Cg = create_graph()

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
        art_dic = {}
        for art_name in Network.artist_IDs:
            art_dic[art_name] = 0

        for  u ,a,l in self.user_artist_data:
            if u == str(name):
                art_dic[a] += int(l)
                # print name, a, l
        return art_dic

    def update_edges(self):
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
        self.graph.remove_edges_from(edges_to_add)
        return len(edges_to_add)

    def move_time(self, n=1):
        for i in range(n):
            updates = []
            for u in self.users:
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


def full_run(net):
    global results_file
    total_cds =0
    for epoch in range(6):
        csales, c_edges , cupdates = net.move_time()
        results_file.write( "In epoch {}: {} new connections,  Sold {} CDs \n".format(epoch, c_edges, csales))
        total_cds += csales
    results_file.write( "The total cds sales is: {}\n".format(total_cds))
    results_file.write( "The totals for every artist is:\n")
    for a in net.art_analisys.items():
         results_file.write(  "artist number {}: {}\n".format(a[0],a[1]))






if __name__ == '__main__':
    global results_file
    # Gg, Cg = create_graph('user_friends.csv')
    # Gg, Cg = create_graph()
    # print Gg.number_of_edges(), Cg.number_of_edges()
    # update_edes(Gg,Cg)
    # print Gg.number_of_edges(), Cg.number_of_edges()

    # net = Network()
    t1 = datetime.now()
    net = Network()
    res_f = open('net.dump', 'w')
    pickle.dump(net,res_f )
    res_f.close()
    # res_f = open('net.dump', 'r')
    # net = pickle.load(res_f)
    # res_f.close()
    best_users = list(find_best())
    b_list = []
    for uu in best_users:
        b_list.append(net.users[uu[0]])
    res_f = open('an_results.dump', 'r')
    res = pickle.load(res_f)
    res_f.close()
    user_list = [u[0] for u in res]

    nn1 = sorted(user_list, key=lambda x: x.num_of_friends[0])
    nn2 = sorted(user_list, key=lambda x: x.num_of_friends[1])
    nn3 = sorted(user_list, key=lambda x: x.num_of_friends[2])
    nn4 = sorted(user_list, key=lambda x: x.num_of_friends[3])
    nn0 = b_list
    stat_list = [nn0]#,nn1]#,nn2,nn3,nn4]

    artist_IDss = [ '150', '989',  '194647', '390392', '511147', '532992']

    for i,ul in enumerate(stat_list):
        results_file.write('********** run number {} *******\n'.format(i))
        res_f = open('net.dump', 'r')
        net = pickle.load(res_f)
        res_f.close()
        f_best = ul[:10]
        for artist in artist_IDss:
            ls = sorted(f_best, key=lambda x: x.artist_stats[artist], reverse=True)
            results_file.write("artist #{}:".format(artist))
            for ua in ls[:6]:
                ua.add_disks([artist])
                results_file.write(str(ua.id) + ",")
            results_file.write('\n')
        results_file.write('final results: \n')
        full_run(net)





    # full_run(net)
    t2 = datetime.now()
    print 'took {} times to run'.format((t2-t1))
    # run_sim(net,best_users)
    # lc = nx.load_centrality(net.graph)
    # res_l = open('load_centrality.dump', 'w')
    # pickle.dump(lc,res_l )
    # res_l.close()
    #
    # bc = nx.betweenness_centrality(net.graph)
    # res_b = open('betweenness_centrality.dump', 'w')
    # pickle.dump(lc,res_b )
    # res_b.close()


