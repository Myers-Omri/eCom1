import csv
import random

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



def main():
    net = Network() #Class where the data from files is stored

    artist_IDs = [70, 150, 989, 16326, 144882, 194647, 389445, 390392, 511147, 532992] #List of artists to choose from

    users = {} # Dictionary where user IDs are kept as keys
    for edge in net.edges:
        users[edge[0]] = True

    branch = []
    for user in users:
        """This for calculates the number of friend of each user"""
        neighbours = 0
        for edge in net.edges:
            if user in edge:
                neighbours += 1
        branch.append((user, neighbours/2))
    

    max_branch = sorted(branch, key=lambda x: x[1])[-5:] # First five users with the biggest number of friends
    users_to_print = map(lambda x: x[0], max_branch)

    
    for artist in artist_IDs[:6]: # output example
        with open('artist_' + str(artist), 'wb') as csvfile:
            csv.writer(csvfile).writerow(users_to_print)
    
if __name__ == "__main__":
    main()
