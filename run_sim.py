__author__ = 'omrim'

import user
import networkx as nx
import csv
from sys import stdout
import cPickle as pickle
from random import random
from networkr import Network
# from analytics import find_best
from datetime import datetime,time, timedelta
import copy as cp



results_file = open('res_file.txt', 'w')


def full_run(net, art_user):
    '''
    for a given network- (graph, users, artist list) simulate the run of 6 epochs.
    :param net: initialized Network object.
    :return: None
    '''
    global results_file
    for a_u, u_d in art_user.items():
        for ug in u_d:
            net.users[ug].disks[a_u] = 1

    total_cds =0
    for epoch in range(6):
        csales, c_edges , cupdates = net.move_time()
        print "In epoch {}: {} new connections,  Sold {} CDs \n".format(epoch, c_edges, csales)
        results_file.write( "In epoch {}: {} new connections,  Sold {} CDs \n".format(epoch, c_edges, csales))
        total_cds += csales
    results_file.write( "The total cds sales is: {}\n".format(total_cds))
    results_file.write( "The totals for every artist is:\n")
    for a in net.art_analisys.items():
         results_file.write(  "artist number {}: {}\n".format(a[0],a[1]))






if __name__ == '__main__':


    global results_file


    t1 = datetime.now()
    net = Network()


    res_f = open('an_results_max_f.dump', 'r')
    user_list = pickle.load(res_f)
    res_f.close()

    nn4 = sorted(user_list, key=lambda x: x.get_num_of_friends_in_dist(4), reverse=True)
    nn1 = sorted(user_list, key=lambda x: x.get_num_of_friends_in_dist(1), reverse=True)


    artist_IDss = [ '150', '989',  '194647', '390392', '511147', '532992']


    a_best = nn4[:25]
    s_best = nn1[:15]
    sett = set([x.id for x in a_best]).intersection(set([y.id for y in s_best]))
    # print [(z.get_num_of_friends_in_dist(4), z.get_num_of_friends_in_dist(1)) for z in f_best if z.id in sett]
    f_best = [u for u in user_list if u.id in sett]
    stat_list_id = [ui.id for ui in f_best]
    print "list of potential users:" , stat_list_id
    '''list of potential users: ['138760', '263144', '375845', '649628', '160451', '909244',
                                '386404', '939238', '468276', '209564', '837172', '965152', '756469']'''
    selects = {}
    for artist in artist_IDss:
        u_list = []
        ls = sorted(f_best, key=lambda x: x.artist_stats[artist], reverse=True)
        results_file.write("artist #{}:".format(artist))
        for ua in ls[:5]:
            u_list.append(ua.id)
            results_file.write(str(ua.id) + ",")
        results_file.write('\n')
        selects[artist] = []
        c_list = cp.copy(u_list)
        for a in c_list:
            selects[artist].append(a)

    print selects
    '''
    {
    532992: ['939238', '756469', '160451', '375845', '965152'],
    511147: ['939238', '160451', '375845', '386404', '649628'],
    150:    ['138760', '263144', '649628', '386404', '375845'],
    194647: ['263144', '939238', '649628', '386404', '160451'],
    390392: ['939238', '160451', '375845', '209564', '756469'],
    989:    ['138760', '263144', '386404', '649628', '939238']
        }
    '''
    net = Network(artist_IDss)
    results_file.write('final results: \n')
    full_run(net, selects)


    t2 = datetime.now()
    results_file.write( 'took {} min to run'.format((t2-t1)))
    results_file.close()


