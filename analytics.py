__author__ = 'omrim'


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import csv


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


def get_lis_count(artist_IDs):
    net = Network() #Class where the data from files is stored
    listen_count = []
    for artist in artist_IDs:
        ini_count = []
        for l in net.user_artist_data[1:]:
            if int(l[1]) == artist:
                ini_count.append(int(l[2]))
        listen_count.append((str(artist),ini_count))
    return listen_count

def analyse():

    numDists = 10
    artist_IDs = [70, 150, 989, 16326, 144882, 194647, 389445, 390392, 511147, 532992] #List of artists to choose from

    # users = {} # Dictionary where user IDs are kept as keys
    # for edge in net.edges:
    #     users[edge[0]] = True
    #
    # friends_count = []
    # for user in users:
    #     """This for calculates the number of friend of each user"""
    #     neighbours = 0
    #     for edge in net.edges:
    #         if user in edge:
    #             neighbours += 1
    #     friends_count.append((user, neighbours/2))

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

    # Finally, add a basic legend
    plt.figtext(0.80, 0.08, str(500) + ' Random Numbers',
                backgroundcolor=boxColors[0], color='black', weight='roman',
                size='x-small')
    plt.figtext(0.80, 0.045, 'IID Bootstrap Resample',
                backgroundcolor=boxColors[1],
                color='white', weight='roman', size='x-small')
    plt.figtext(0.80, 0.015, '*', color='white', backgroundcolor='silver',
                weight='roman', size='medium')
    plt.figtext(0.815, 0.013, ' Average Value', color='black', weight='roman',
                size='x-small')

    plt.show()


    for al in listen_count:
        npar = np.array(al[1])
        print str(al[0]) + ':'

        print '     num of friends:' + str(npar.size)
        print '     min is:' + str(np.min(npar))
        print '     max is:' + str(np.max(npar))
        print '     std is:' + str(np.std(npar))
        print '     average is:' + str(np.average(npar))
        print '     median is:' + str(np.median(npar))







    # max_branch = sorted(friends_count, key=lambda x: x[1])[-5:] # First five users with the biggest number of friends
    # users_to_print = map(lambda x: x[0], max_branch)
    #

def print_artists(artist_IDs, users_to_print):
    for artist in artist_IDs[:6]:
        with open('artist_' + str(artist), 'wb') as csvfile:
            csv.writer(csvfile).writerow(users_to_print)


if __name__ == '__main__':

    analyse()