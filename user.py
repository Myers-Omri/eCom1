__author__ = 'omrim'

import random




class user():

    def __init__(self, id,  artists={}):
        self.id = id

        self.artist_list = artists

        self.disks = {}
        for a in artists:
            self.disks[a] = 0
        self.num_of_friends = [0,0,0,0,0,0,0,0,0,0]
        self.artist_stats = {}
        for ast in artists:
            self.artist_stats[ast] = 0

    def add_disks(self, artists):
        for a in artists:
            self.disks[a] = 1

    def num_of_friends_listening(self, artist, friends_list):
        n=0
        for f in friends_list:
            n += f.disks[artist] #for every friend add the value of the disk {0,1}
        return n

    def calc_new_disk(self,friends_names, users, net_artists):
        disks_added = []
        friends_list = []
        for f in friends_names:
            friends_list.append(users[f])
        for a in self.disks:
            if a in net_artists and self.disks[a] == 0:
                r = random.random()
                nfl = self.num_of_friends_listening(a,friends_list)
                prob = float(nfl)/float(len(friends_list)) + float(self.artist_list[a]) / 2000.0
                if r < prob:
                    # self.disks[a] = 1
                    disks_added.append(a)
        return disks_added

    def get_num_of_friends_in_dist(self,n):
        if n > 9:
            n=9
        sum =0
        for i in range(n):
            sum+=self.num_of_friends[i]
        return sum












if __name__ == '__main__':
    print "User Modul"
