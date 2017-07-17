import os
import argparse
import random
import csv

# argparse configurations
desc="Script for generating train/test dataset of MovieLensLatest(https://grouplens.org/datasets/movielens/) for libFM(http://libfm.org/) and libffm-regression(https://www.csie.ntu.edu.tw/~cjlin/libffm/)"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--prefix-train", type = str, default="train_", help="default='train_'")
parser.add_argument("--prefix-test" , type = str, default="test_" , help="default='test_'")
parser.add_argument("--dataset"     , metavar="DATA",type = str, default="ml-latest-small/",help="default='ml-latest-small/'" )
parser.add_argument("-o", "--output", metavar="DIR" ,type = str, default="output" , help="default='output/'")
parser.add_argument("-t", "--timestamp", action="store_true")
parser.add_argument("-g", "--genre", action="store_true")
parser.add_argument("--other", action="store_true")
parser.add_argument("-l","--last", action="store_true")
parser.add_argument("-f","--field-aware", action="store_true")
args = parser.parse_args()

output  = args.output
dataset = args.dataset
moviefile  = os.path.join(dataset,"movies.csv")
ratingfile = os.path.join(dataset,"ratings.csv")

# create output directory
if not os.path.exists(output):
    os.makedirs(output)

# read movie file
movie_to_genre_set = {}
all_genre = set()
all_movie = set()
with open(moviefile,"r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("header =",header)
    for row in reader:
        assert(len(row)==3)
        movie, _, genre = row
        genre = set(genre.split("|"))
        assert(len(genre)>0) # a movie at least one genre
        all_genre = all_genre.union(genre)
        all_movie.add(movie)
        movie_to_genre_set[movie] = genre 

# read rating file
data = []
with open(ratingfile,"r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("header =",header)
    for row in reader:
        assert(len(row)==4)
        data += [row]
        
# get miminum timestamp
minTime = min([ int(t) for _,_,_,t in data ])

# get all user
all_user = set( [ u for u,_,_,_ in data ] )
# user to id
user_to_id = { user:str(i) for i,user in enumerate(all_user) }
print("num of users =",len(user_to_id))

# genre to id
genre_to_id = { genre:str(i) for i,genre in enumerate(all_genre) }
print("genres =",genre_to_id)

# movie to id
movie_to_id = { movie:str(i) for i,movie in enumerate(all_movie) }
