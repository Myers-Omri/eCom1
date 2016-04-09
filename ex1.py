import csv
import cPickle as pickle



if __name__ == "__main__":
    res_f = open('an_results.dump', 'r')
    res = pickle.load(res_f)
    res_f.close()
    for u, s in res: #u is user , s is tuple (art_list, nn)
        print 'user:    ', u.id
        print 'nn:      ', s[1]
        print 'nn1:     ', u.get_num_of_friends_in_dist(1)
        print 'nn2:     ', u.get_num_of_friends_in_dist(2)
        print 'nn3:     ', u.get_num_of_friends_in_dist(3)
        print 'nn4:     ', u.get_num_of_friends_in_dist(4)
        ls = sorted(u.artist_stats.items(), key=lambda x: x[1])
        print "artist stats:"
        for a,nl in ls:
            print "     ", a, ":", nl


