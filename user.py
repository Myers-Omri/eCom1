__author__ = 'omrim'

import random




class user():

    def __init__(self, id,  artists={}):
        self.id = id

        self.artist_list = artists

        self.disks = {}
        for a in artists:
            self.disks[a] = 0






    def add_disks(self, artists):
        for a in artists:
            self.disks[a] = 1

    def num_of_friens_listening(self, artist, friends_list):
        n=0
        for f in friends_list:
            n += friends_list.get(f).disks[artist] #for every friend add the value of the disk {0,1}
        return n

    def calc_new_disk(self,friends_list):
        disks_added = []
        for a in self.disks:
            if self.disks[a] == 0:
                r = random.random() # make sure between 0,1
                nf = self.num_of_friens_listening(a,friends_list)
                prob = float(nf)/float(len(friends_list)) + float(self.artist_list[a]) / 2000.0
                if r < prob:
                    self.disks[a] = 1
                    disks_added.append(a)
        return disks_added











if __name__ == '__main__':
    print "User Modul"
