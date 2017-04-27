import cPickle as pickle
import os
from tfidf_based_feature import get_similarity
tfidf_dir = "./training/tfidf"
#
name = "Abby_Watkins"

file = os.path.join(tfidf_dir, name+".pkl")

words_dict = pickle.load(open(file, "r"))

rank_vec = words_dict["rank_vec"]
words_tfidf = words_dict["words_tfidf"]

# print len(words_tfidf), len(words_tfidf[0])
print words_tfidf[0:10]
# a = [1, 1, 0]
# b = [1, 1, 0]
# print get_similarity(a,b)

