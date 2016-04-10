__author__ = 'omrim'


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import csv
import cPickle as pickle
from run_sim import Network, find_best
import networkx as nx
from sys import stdout
from datetime import datetime





def get_lis_count(artist_IDs):
    # res_f = open('net.dump', 'r')
    # net = pickle.load(res_f)
    # res_f.close()#Class where the data from files is stored
    net = Network(['70', '150', '989', '16326', '144882', '194647', '389445', '390392', '511147', '532992'])
    listen_count = []
    for artist in artist_IDs:
        ini_count = []
        for l in net.user_artist_data[1:]:
            if int(l[1]) == artist:
                ini_count.append(int(l[2]))
        listen_count.append((str(artist),ini_count))
    return listen_count


def analyse():

    '''
    this function collect the data about the artists and draw boxplots that illustrate the
    statistics info and make it easier to decide which user to chose our selction is based on the
    number of users that listen to the artist the average and median more than the actual number of
     times the songs are played.
    :return: Draw a boxplot with sd,avg,med
    '''

    numDists = 10
    artist_IDs = [70, 150, 989, 16326, 144882, 194647, 389445, 390392, 511147, 532992] #List of artists to choose from



    listen_count = get_lis_count(artist_IDs)

    artist_str = [s[0] for s in listen_count]
    num_of_plays = [np.array(s[1]) for s in listen_count]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('E, Var, SD of num of listeners for every artist')
    plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = plt.boxplot(num_of_plays, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title('A comparison of-E, Var, SD of num of listeners for every artist')
    ax1.set_xlabel('The Artist ID')
    ax1.set_ylabel('Num of time played')

    # Now fill the boxes with desired colors
    boxColors = ['darkkhaki', 'royalblue']
    numBoxes = numDists
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = list(zip(boxX, boxY))
        # Alternate between Dark Khaki and Royal Blue
        k = i % 2
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            plt.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        plt.plot([np.average(med.get_xdata())], [np.average(num_of_plays[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes + 0.5)
    top = 1000
    bottom = 0
    ax1.set_ylim(bottom, top)
    xtickNames = plt.setp(ax1, xticklabels=np.repeat(artist_str, 1))
    plt.setp(xtickNames, rotation=45, fontsize=8)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], top - (top*0.05), upperLabels[tick],
                 horizontalalignment='center', size='x-small', weight=weights[k],
                 color=boxColors[k])

    # Finally, a basic legend

    plt.figtext(0.80, 0.015, '*', color='white', backgroundcolor='silver',
                weight='roman', size='medium')
    plt.figtext(0.815, 0.013, ' Average Value', color='black', weight='roman',
                size='x-small')

    plt.show()

    ## print out some stats about the artists
    for al in listen_count:
        npar = np.array(al[1])
        print str(al[0]) + ':'

        print '     num of friends:' + str(npar.size)
        print '     min is:' + str(np.min(npar))
        print '     max is:' + str(np.max(npar))
        print '     std is:' + str(np.std(npar))
        print '     average is:' + str(np.average(npar))
        print '     median is:' + str(np.median(npar))




def print_artists(artist_IDs, users_to_print):
    for artist in artist_IDs[:6]:
        with open('artist_' + str(artist), 'wb') as csvfile:
            csv.writer(csvfile).writerow(users_to_print)




art_dict = {}
nn=1

def recursive_stat(uu, ur, netr,d, kr):
    '''
    recursively calculate the stats about a selected user.
    :param uu: user object
    :param ur: user name
    :param netr: net object
    :param d: the distance we analise
    :param kr: current level
    :return: modify global vars and the user list in net object
    '''
    global art_dict
    global nn

    if kr<=0:
        return
    for f in netr.graph.neighbors(ur):
        nn+=1
        uu.num_of_friends[(d- kr)] += 1
        u_artist_dictionary = netr.users[f].artist_list
        for a,l in u_artist_dictionary.items():
            tl = min(l,2000)
            tlf = float(tl) / 2000.0
            if a in art_dict:
                art_dict[a] += tlf*kr
        recursive_stat(uu, f,netr,d,kr-1)
    return



def get_stats(usr, nett, n=1):
    global art_dict
    global nn
    for a in nett.artist_IDs:
        art_dict[a] = 0
    nn=0
    k=n
    recursive_stat(nett.users[usr] ,usr, nett,k, k )
    for aaa, l  in art_dict.items():
        nett.users[usr].artist_stats[aaa]=l
    return (art_dict, nn)


if __name__ == '__main__':
    selection = raw_input("Analyse or Get stats? A-S")
    if selection == 'A':
        analyse()
    else:
        net = Network()
        user_dict = {}
        for u in net.graph.nodes():
            user_dict[u] = len(net.graph.neighbors(u))

        sorted_user_list = sorted(user_dict.items(), key= lambda x : x[1], reverse=True)
        top_30 = sorted_user_list[:30]

        t1 = datetime.now()
        results = []
        i=0
        '''for the useres with largest number of close friends make the statistics for the 4 level friends (all users that
        are in distance 4 from the root.
        '''
        for bu in top_30:
            print i
            stats = get_stats(bu[0], net,4)
            results.append(net.users[bu[0]])
            print "stats for user {}:". format(bu[0])
            print 'num of neigbhors:{}'.format(stats[1])
            for u in net.users[bu[0]].artist_stats:
                print 'artist {}: l- {} '.format(u,net.users[bu[0]].artist_stats[u])

            i+=1


        #save the results
        res_f = open('an_results_max_f.dump', 'w')
        pickle.dump(results,res_f )
        res_f.close()


        t2 = datetime.now()
        print "total time: {}".format((t2-t1))

