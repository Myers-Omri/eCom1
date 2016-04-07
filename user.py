__author__ = 'omrim'

import random
class user():

    def __init__(self, id,  artists={},friends={}):
        self.id = id

        self.artist_list = artists
        self.friends_list = friends
        self.disks = {}
        for a in artists:
            self.disks[a] = 0




    def add_friends(self, friends ):
        if type(friends) == int:
            self.friends_list[friends.id] = friends
            return
        for f in friends:
            self.friends_list[f.id] = f
        return

    def add_disk(self, artist):
        self.disks[artist] = 1

    def num_of_friens_listening(self, arist):
        n=0
        for f in self.friends_list:
            n += self.friends_list.get(f).disks[arist] #for every friend add the value of the disk {0,1}
        return n

    def calc_new_disk(self):
        disks_added = []
        for a in self.disks:
            if self.disks[a] == 0:
                r = random.random() # make sure between 0,1
                nf = self.num_of_friens_listening(a)
                prob = float(nf)/float(len(self.friends_list)) + float(self.artist_list[a]) / 2000.0
                if r < prob:
                    self.disks[a] = 1
                    disks_added.append(a)
        return disks_added











if __name__ == '__main__':
    print "User Modul"
